import json
import os

import webhook_listener
from loguru import logger
import requests

from rocketchat_bot_app_bridge.definitions.application import IBackendRequest, IToBackendButtonClick, EventType, \
    IFromBackendRequestSendMessage
from rocketchat_bot_app_bridge.definitions.message import IMessage
from rocketchat_bot_app_bridge.definitions.user import IUser


class BotBackendController(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BotBackendController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.bots = {}
        self.app_endpoint = os.getenv('APP_ENDPOINT', None)
        self.webhooks = webhook_listener.Listener(
            port=os.getenv('BOT_PORT', 3228),
            handlers={
                "POST": self.handle_POST,
            },
        )

    def handle_POST(self, request, *args, **kwargs):
        body = request.body.read(int(request.headers["Content-Length"]))
        logger.debug(
            "Received request:\n"
            + "Method: {}\n".format(request.method)
            + "Headers: {}\n".format(request.headers)
            + "Args (url path): {}\n".format(args)
            + "Keyword Args (url parameters): {}\n".format(kwargs)
            + "Body: {}".format(
                body
                if int(request.headers.get("Content-Length", 0)) > 0
                else ""
            )
        )
        from_app_data: IBackendRequest = json.loads(body)
        event = from_app_data['event']
        bot = from_app_data['bot']
        payload = from_app_data['payload']

        if event == 'new_message':
            self.dispatch_new_message(payload, bot)
        elif event == 'button_click':
            self.dispatch_button_click(payload, bot)

    def run(self):
        logger.info(f'Running webhook server')
        self.webhooks.start()
        logger.info(f'Listen on http://{self.webhooks.host}:{self.webhooks.port}/ copy this(or service ip for '
                    f'kubernetes) to RocketChat app settings')

    def register_bot(self, instance, bot_username=None):
        logger.info(f'Registered bot {bot_username}')
        self.bots[bot_username] = instance

    def dispatch_button_click(self, payload: IToBackendButtonClick, bot: IUser):
        bot = self._select_context_bot(bot)

        handler = bot.button_handler_by_action.get(payload['action'], None)
        if not handler:
            for group_name, callback in bot.button_group_handler_by_startsw.items():
                if payload['action'].startswith(group_name):
                    handler = callback
                    break

        if not handler:
            logger.error(f"Bot {bot.username} does not have button/group handler for action {payload['action']}")
            return

        handler(payload['action'], payload['user'], payload['message'])

    def dispatch_new_message(self, payload: IMessage, bot: IUser):
        bot = self._select_context_bot(bot)

        for regex, callback in bot.hears_by_regexp.items():
            matches = regex.search(payload["text"])
            if matches:
                callback(payload, **matches.groupdict())
                return
                break

        handler = bot.callback_by_event.get('new_message', None)
        if not handler:
            logger.error(f"Bot {bot.username} does not have new_message/hear handler")
            return

        handler(payload)

    def _select_context_bot(self, bot: IUser):
        if bot['type'] == 'app':
            try:
                return self.bots['self_app']
            except KeyError:
                logger.error(f"Failed select default bot")
        else:
            try:
                return self.bots[bot['username']]
            except KeyError:
                logger.error(f"Failed dispatch new message for {bot['username']} please create instance for them")

        return

    def send_event_to_app(self, *args, instance=None, event_type: EventType, payload: IFromBackendRequestSendMessage):
        data = {
            'event': event_type,
            'bot': IUser(username=instance.username),
            'payload': payload
        }
        result = requests.post(
            self.app_endpoint,
            json=data)
        logger.debug(result)
