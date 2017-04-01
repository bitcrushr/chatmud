import requests
import json
import time

class API:
    def __init__(self, token):
        self.token = token
        self.usernames = {}
        self.username = ''
        self.last_username = ''
        self.channels = []
        self.last_poll = 0
        self.ready = False
        self.chatbuffer = []


    def send_request(self, method, params):
        return requests.post('https://www.hackmud.com/mobile/{}.json'.format(method),
                headers = {'Content-Type': 'application/json'},
                json = params)

    def login(self):
        if len(self.token) > 6:
            return self.get_usernames()
        else:
            res = self.send_request('get_token', { 'pass' : self.token } ).json()
            self.token = res['chat_token']
            return self.get_usernames()

    def get_usernames(self):
        res = self.send_request('account_data', { 'chat_token' : self.token }  ).json()
        self.usernames = res['users']
        self.ready = True
        return res['users'].keys()

    def get_fullinfo(self):
        res = self.send_request('account_data', { 'chat_token' : self.token }  ).json()
        self.usernames = res['users']
        return res['users']

    def set_username(self, username):
        channels = self.usernames[username]
        if len(channels):
            self.last_username = self.username
            self.username = username
            self.channels = channels
            return self.channels

    def poll_messages(self):
        if len(self.username) and self.ready:
            res = self.send_request('chats', { 'chat_token' : self.token , 'usernames' : [self.username] } ).json()
            try:
                self.last_poll = time.time()
                self.chatbuffer = res['chats'][self.username]
            except:
                pass
            resp = reversed( self.chatbuffer )
            return resp

    def poll_history(self, channel):
        if len(self.username) and self.ready:
            res = self.send_request('chats', { 'chat_token' : self.token , 'usernames' : [self.username], 'after' : self.last_poll} ).json()
            self.chatbuffer = {}
            try:
                self.last_poll = time.time()
                self.chatbuffer = res['chats'][self.username]
            except:
                pass
            try:
                resp = reversed( self.chatbuffer )
            except:
                resp = {}
            return resp
            
    def send_chat_to_user(self, username, msg):
        return self.send_request('create_chat',  { 'chat_token' : self.token, 'username' : self.username, 'tell' : username, 'msg' : msg} ).json()

    def send_chat_to_channel(self, channel, msg):
        self.send_request('create_chat',  { 'chat_token' : self.token, 'username' : self.username, 'channel' : channel, 'msg' : msg} ).json()
