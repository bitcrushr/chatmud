from curses import wrapper
import cgraphics
import chatapi
import os
import sys
from pathlib import Path
import time
import threading

def main(stdscr):
	stdscr.clear()
	Api = None
	saved = False
	baud = 3
	
	Gui = cgraphics.Graphics(stdscr)
	token_file = Path("./token.dat")
	if token_file.is_file():
		saved = True
		token_file = open('token.dat')
		resp = token_file.read()
		Api = chatapi.API(resp)
		Api.login()
	else:
		resp = Gui.wait_input("Enter your chat_pass: ")
		Api = chatapi.API(resp)
		Api.login()
		if Api.token:
			token_file  = open('token.dat', 'w+')
			token_file.write(Api.token)
		else:
			Gui.inject_chat("Invalid token...")
			sys.exit(1)
	
	
	Gui.inject_chat("Logged in with {}".format(Api.token))
	
	resp_u = Gui.wait_input('Starting user: ')
	resp_c = Gui.wait_input('Starting channel: ')
	
	Api.set_username(resp_u)
	username = resp_u
	
	channel = resp_c
	
	Gui.switch_channel_user(channel, username)
	Gui.resize()
	messages = Api.poll_messages()
	
	
	

	### repeater function needs to be defined here in order to have variable access (I think?)
	class Threader( threading.Thread ):
		def run(self):
			while running:
				messages = Api.poll_messages()
				print(messages)
				Gui.put_buffer(messages)
				Gui.render_chatbox()
				time.sleep(baud)
			os._exit(1)

	###
	
	def zend(channel, msg):
		Api.send_chat_to_channel(channel, msg)
	
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
			Gui.switch_channel_user(channel, username)
			Gui.inject_chat("User set to {}".format(username))
		elif "/channel " in uin:
			channel = uin[9:]
			Gui.switch_channel_user(channel, username)
			Gui.inject_chat("Channel set to {}".format(channel))
		elif "/baud " in uin:
			try:
				baud = int(uin[6:])
			except:
				Gui.inject_chat("Bad polling rate : {}".format(uin))
			Gui.inject_chat("polling rate set to {}".format(baud))
		else:
			message_thread = threading.Thread(target=zend, args=[channel, uin])
			message_thread.start()
			pass
	sys.exit()
wrapper(main)
"""
try:
	wrapper(main)
except:
	print("Program exited unexpectedly.")
"""
