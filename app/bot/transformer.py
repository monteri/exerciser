class SlackApiTransformer:
    def __init__(self, payload):
        self.payload = payload
        self.values = {}
        self.callback_id = None
        self.metadata = None
        self.view = {}
        self.user_name = None
        self.user_username = None
        self.type = None
        self.action = None
        self.action_id = None
        self.value = None
        self.user_id = None
        self.trigger_id = None
        self.parse_payload()

    def parse_payload(self):
        try:
            self.type = self.payload.get('type')
            self.action = self.payload.get('actions', [{}])[0]
            self.action_id = self.action.get('action_id')
            self.value = self.action.get('value')
            self.user_id = self.payload['user']['id']
            self.user_username = self.payload['user']['username']
            self.user_name = self.payload['user']['name']
            self.trigger_id = self.payload.get('trigger_id')
            self.view = self.payload.get('view', {})
            self.metadata = self.view.get('private_metadata')
            self.callback_id = self.view.get('callback_id')
            self.values = self.view.get('state', {}).get('values', {})
        except TypeError as e:
            print(f"Button callback hook couldn't decode response: {e}")
