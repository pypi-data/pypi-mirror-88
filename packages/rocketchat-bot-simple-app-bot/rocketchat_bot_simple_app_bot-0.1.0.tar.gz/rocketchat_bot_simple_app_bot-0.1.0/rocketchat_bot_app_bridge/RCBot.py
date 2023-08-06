import re
from typing import List

from rocketchat_bot_app_bridge.BotBackendController import BotBackendController
from rocketchat_bot_app_bridge.definitions.application import IButton
from rocketchat_bot_app_bridge.definitions.message import IMessage


class RCBot:
    def __init__(self,
                 account_username='self_app',
                 app_endpoint: str = None,
                 port: int = None,
                 controller=BotBackendController()):
        self.username = account_username
        self.callback_by_event = {}
        self.button_handler_by_action = {}
        self.button_group_handler_by_startsw = {}
        self.hears_by_regexp = {}
        self._controller = controller

        # only before run first bot instance
        if app_endpoint:
            self._controller.app_endpoint = app_endpoint
        if port:
            self._controller.webhooks.port = port

    def run(self):
        self._controller.register_bot(instance=self, bot_username=self.username)
        self._controller.run()

    def send(self, message: IMessage, buttons: List[IButton] = []):
        payload = {
            'message': message,
            'buttons': buttons,
        }
        self._controller.send_event_to_app(instance=self, payload=payload, event_type='message_from_backend')

    def on_new_message(self, fn):
        self.callback_by_event['new_message'] = fn

        return fn

    def hear(self, pattern):
        s = self
        regex = re.compile(pattern, flags=re.IGNORECASE)

        def wrapper(fn):
            s.hears_by_regexp[regex] = fn
            return fn

        return wrapper

    def on_button_click(self, action='', startswith=''):
        """
        Use one of params to create handler for button action name or
        for group of buttons with prefix
        :param action:
        :param startswith:
        :return:
        """
        s = self

        def wrapper(fn):
            if action:
                s.button_handler_by_action[action] = fn
            elif startswith:
                s.button_group_handler_by_startsw[startswith] = fn
            return fn

        return wrapper
