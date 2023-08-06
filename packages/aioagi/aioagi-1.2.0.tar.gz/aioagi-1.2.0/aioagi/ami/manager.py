import asyncio
import traceback
from collections import defaultdict
from collections import deque
import re
import fnmatch
from . protocol import AMIProtocol
from . action import AMIAction
from . message import AMIMessage
from ..log import agi_ami_logger


class AMIManager:
    """Main object:

    .. code-block:: python

        >>> manager = AMIManager(
        ...    host='127.0.0.1',
        ...    port=5038,
        ...    ssl=False,
        ...    encoding='utf8')
    """

    def __init__(self, app, title, **config):
        self.app = app
        self.title = title
        self.config = dict(
            {
                'host': '127.0.0.1',
                'port': 5038,
                'events': 'on',
                'ssl': False,
                'encoding': 'utf8',
                'ping_delay': 10,
                'reconnect_delay': 0.5,
                'protocol_factory': lambda: AMIProtocol(self),
                'save_stream': None,
                'loop': None,
                'forgetable_actions': ('ping', 'login'),
            }, **config)

        self.loop = None
        self.callbacks = defaultdict(list)
        self.patterns = []

        self.protocol = None
        self.transport = None

        self.closed = False
        self.connected = False
        self.authenticated = False
        self.authentication_cond = asyncio.Condition()

        self.awaiting_actions = deque()
        self.forgetable_actions = self.config['forgetable_actions']

        self.pinger = None
        self.authenticator = None
        self.ping_delay = float(self.config['ping_delay'])
        self.reconnect_delay = float(self.config['reconnect_delay'])
        self.register_event('FullyBooted', self.send_awaiting_actions)

    async def connect(self):
        """
        Connect to the Asterisk server.
        """
        if self.loop is None:  # pragma: no cover
            self.loop = asyncio.get_event_loop()

        while not self.connected:
            agi_ami_logger.debug(f'{self.title}: Try to connect')
            try:
                self.transport, self.protocol = await self.loop.create_connection(
                    self.config['protocol_factory'],
                    self.config['host'], self.config['port'],
                    ssl=self.config['ssl']
                )

            except OSError:  # pragma: no cover
                agi_ami_logger.exception(
                    f'{self.title}: Not able to connect, try again for {self.reconnect_delay} second(s).')

                if self.reconnect_delay:
                    await asyncio.sleep(self.reconnect_delay)

            else:
                agi_ami_logger.debug(f'{self.title}: Manager connected')
                self.connected = True
                self.authenticator = asyncio.ensure_future(self.authenticate())
                try:
                    await self.authenticator
                except asyncio.CancelledError:
                    raise
                except Exception:
                    agi_ami_logger.error(f'{self.title}: Login error\n{traceback.format_exc()}')
                    if self.reconnect_delay:
                        await asyncio.sleep(self.reconnect_delay)

    async def authenticate(self):
        agi_ami_logger.debug(f'{self.title}: Login to Asterisk')
        async with self.authentication_cond:
            agi_ami_logger.debug(f'{self.title}: Enter to authentication_cond')
            if 'username' in self.config:
                message = await self.send_action(
                    AMIAction({
                        'Action': 'Login',
                        'Username': self.config['username'],
                        'Secret': self.config['secret'],
                        'Events': self.config['events']
                    })
                )
                agi_ami_logger.debug(f'{self.title}: Login result `{message}`')
                if message.success:
                    self.authenticated = True

            else:
                agi_ami_logger.warning(f'{self.title}: Username not in config file')

            if self.authenticated:
                agi_ami_logger.info(f'{self.title}: Asterisk connection is authenticated')
                self.authentication_cond.notify_all()
                self.pinger = asyncio.ensure_future(self.ping())

            else:
                agi_ami_logger.info(f'{self.title}: Asterisk connection is NOT authenticated!')
                self.close()

            self.authenticator = None

    async def ping(self):  # pragma: no cover
        while True:
            agi_ami_logger.debug(f'{self.title}: Ping connection')
            try:
                result = await self.protocol.send(AMIAction({'Action': 'Ping'}))
            except asyncio.CancelledError:
                raise
            except Exception:
                agi_ami_logger.error(f'{self.title}: Ping error\n{traceback.format_exc()}')
                await asyncio.sleep(1)
            else:
                agi_ami_logger.debug(f'{self.title}: Ping result `{result}`')
                await asyncio.sleep(self.ping_delay)

    async def close(self):
        """Close the connection"""
        self.closed = True
        self.connected = self.authenticated = False

        if self.pinger:
            self.pinger.cancel()
            try:
                await self.pinger
            except asyncio.CancelledError:
                agi_ami_logger.debug(f'{self.title}: Pinger canceled')
            finally:
                self.pinger = None

        self.protocol = None

        self.transport.close()
        self.transport = None

    def connection_lost(self, exc):
        self.connected = self.authenticated = False

        agi_ami_logger.info(f'{self.title}: Asterisk connection lost!')
        exc and agi_ami_logger.warning(exc)

        if self.authenticator:
            self.authenticator.cancel()
            self.authenticator = None

        if self.pinger:
            self.pinger.cancel()
            self.pinger = None

        if not self.closed:
            self.store_actions()
            agi_ami_logger.info(f'{self.title}: Try to connect again')
            asyncio.ensure_future(self.connect())

    def store_actions(self):
        if self.protocol and self.protocol.responses:
            uuids = set()

            for action_id in list(self.protocol.responses.keys()):
                action = self.protocol.responses.pop(action_id)
                uuids.add(action.id)

                if action.future.done():  # pragma: no cover
                    continue

                elif action.responses:
                    # If at least one response was receive from asterisk we don't queue it again
                    action.future.set_result(action.responses)

                elif action['Action'].lower() in self.forgetable_actions:
                    action.future.cancel()

                else:
                    agi_ami_logger.info(
                        '{title}: Adding action "{action}" to awaiting list: {data}'.format(
                            title=self.title,
                            action=action['Action'].lower(),
                            data=str(action),
                        )
                    )
                    self.awaiting_actions.append(action)

    async def send_awaiting_actions(self, *_):
        agi_ami_logger.info(f'{self.title}: Sending awaiting actions')
        while self.awaiting_actions:
            action = self.awaiting_actions.popleft()
            if action['action'].lower() not in self.forgetable_actions:
                if not action.future.done():
                    asyncio.ensure_future(self.send_action(action))

    async def send_action(self, action: AMIAction, **kwargs) -> AMIMessage:
        """Send an :class:`~panoramisk.actions.Action` to the server:

        :param action: an Action or dict with action name and parameters to
                       send
        :type action: AMIAction or dict or Command
        :return: a Future that will receive the response
        :rtype: asyncio.Future

        :Example:

        To retrieve answer in a coroutine::

            manager = Manager()
            resp = yield from manager.send_action({'Action': 'Status'})

        With a callback::

            manager = Manager()
            future = manager.send_action({'Action': 'Status'})
            future.add_done_callback(handle_status_response)

        See https://wiki.asterisk.org/wiki/display/AST/AMI+Actions for
        more information on actions
        """
        action.update(kwargs)

        if not self.connected or not self.authenticated and action.get('Action') != 'Login':
            async with self.authentication_cond:
                await self.authentication_cond.wait()

        return await self.protocol.send(action)

    def send_command(self, command, as_list=False):
        """Send a :class:`~panoramisk.actions.Command` to the server::

            manager = Manager()
            resp = manager.send_command('http show status')

        Return a response :class:`~panoramisk.message.Message`.
        See https://wiki.asterisk.org/wiki/display/AST/ManagerAction_Command
        """
        return self.send_action(AMIAction(
            {'Action': 'Command', 'Command': command},
            as_list=as_list,
        ))

    def send_agi_command(self, channel, command, as_list=False):
        """Send a :class:`~panoramisk.actions.Command` to the server:

        :param channel: Channel name where to launch command.
               Ex: 'SIP/000000-00000a53'
        :type channel: String
        :param command: command to launch. Ex: 'GET VARIABLE async_agi_server'
        :type command: String
        :param as_list: If True, the action Future will retrieve all responses
        :type as_list: boolean
        :return: a Future that will receive the response
        :rtype: asyncio.Future

        :Example:

        ::

            manager = Manager()
            resp = manager.send_agi_command('SIP/000000-00000a53',
                                            'GET VARIABLE async_agi_server')


        Return a response :class:`~panoramisk.message.Message`.
        See https://wiki.asterisk.org/wiki/display/AST/Asterisk+11+ManagerAction_AGI
        """
        return self.send_action(AMIAction(
            {'Action': 'AGI', 'Channel': channel, 'Command': command},
            as_list=as_list,
        ))

    def register_event(self, pattern, callback=None):
        """register an event. See :class:`~panoramisk.message.Message`:

        .. code-block:: python

            >>> def callback(manager, event):
            ...     print(manager, event)
            >>> manager = AMIManager()
            >>> manager.register_event('Meetme*', callback)
            <function callback at 0x...>

        You can also use the manager as a decorator:

        .. code-block:: python

            >>> manager = AMIManager()
            >>> @manager.register_event('Meetme*')
            ... def callback(manager, event):
            ...     print(manager, event)
        """
        def _register_event(callback):
            if not self.callbacks[pattern]:
                self.patterns.append((pattern, re.compile(fnmatch.translate(pattern))))
            self.callbacks[pattern].append(callback)
            return callback
        if callback is not None:
            return _register_event(callback)
        else:
            return _register_event

    def dispatch(self, message: AMIMessage):
        matches = []
        for pattern, regexp in self.patterns:
            match = regexp.match(message['Event'])
            if match is not None:
                matches.append(pattern)
                for callback in self.callbacks[pattern]:
                    ret = callback(self, message)
                    if (asyncio.iscoroutine(ret) or
                            isinstance(ret, asyncio.Future)):
                        asyncio.ensure_future(ret, loop=self.loop)
        return matches
