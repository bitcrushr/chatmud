import requests
import json

class API:
    def __init__(self, token):
        self.baud_active = 1
        self.baud_inactive = 5

        self.token = token
        self.usernames = {}
        self.username = ''
        self.channels = []
        self.last_poll = 0
        self.ready = False
        self.handled_messages = {}


    def send_request(self, method, params):
        return requests.post('https://www.hackmud.com/mobile/{}.json'.format(method),
                headers = {'Content-Type': 'application/json'},
                json = params)

    def login(self):
        if token.len > 6:
            return self.get_usernames()
        else:
            res = self.send_request('get_token', json.dumps( { 'pass' : this.token } ) ).json()
            self.token = res['chat_token']
            return self.get_usernames()

    def get_usernames(self):
        res = self.send_request('account_data', json.dumps( { 'chat_token' : this.token } ) ).json()
        self.usernames = res['users']
        self.ready = True
        return res['users'].keys()

    def set_username(self, username):
        channels = this.usernames[username]
        if channels.len:
            self.handled_messages = {}
            self.last_poll = 0
            self,username = username
            self.channels = channels
            return self.channels

    def poll_messages(self):
        if self.username.len && self.ready:
            
        return

    def send_chat_to_user(self):
        return

    def send_chat_to_channel(self):
        return
