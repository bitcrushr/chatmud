#from curses import wrapper
import chatapi
import graphics
import os
import sys
from pathlib import Path
import time
import threading
def main():
	Api = None
	saved = False
	
	token_file = Path("./token.dat")
	
	os.system("clear")

	if token_file.is_file():
		saved = True
		token_file = open('token.dat')
		resp = token_file.read()
		Api = chatapi.API(resp)
		Api.login()
	else:
		resp = input("Enter your chat_pass: ")
		Api = chatapi.API(resp)
		Api.login()
		if Api.token:
			token_file  = open('token.dat', 'w+')
			token_file.write(Api.token)
		else:
			print("Invalid token...")
			sys.exit(1)
	
	
	print("Logged in with {}".format(Api.token))
	
	resp_u = input('Starting user: ')
	resp_c = input('Starting channel: ')
	
	Api.set_username(resp_u)
	username = resp_u
	
	channel = resp_c
	
	messages = Api.poll_messages()
	
	
	Gui = graphics.Graphics()
	

	### repeater function needs to be defined here in order to have variable access (I think?)
	class Threader( threading.Thread ):
		def run(self):
			while running:
				messages = Api.poll_messages()
				Gui.render(messages, channel, username)
				time.sleep(2)

	###
	running = True
	Threader().start()
	###
	
	while running:
		uin = Gui.wait_input()
		if uin == "/quit":
			running = False
		elif "/user " in uin:
			Api.set_username(uin[6:])
			username = uin[6:]
		elif "/channel " in uin:
			channel = uin[9:]
		else:
			Api.send_chat_to_channel(channel, uin)

main()
