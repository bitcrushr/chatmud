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
	Gui.inject_chat("Initializing...")
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
	
	fullinfo = Api.get_fullinfo()
	usernames = fullinfo.keys()

	Gui.inject_chat("Logged in with {}".format(Api.token))
	
	Gui.inject_chat("Available usernames")
	for i in usernames:
		Gui.inject_chat(i)
	
	valid = False
	while valid == False:
		resp_u = Gui.wait_input('Starting user: ')
		if resp_u in usernames:
			valid = True
		else:
			Gui.inject_chat("Invalid username.")
			valid = False

	channels = fullinfo[resp_u].keys()
	
	Gui.inject_chat("Channels for {}".format(resp_u))
	for i in channels:
		Gui.inject_chat("- {}".format(i))
	
	valid = False
	while valid == False:
		resp_c = Gui.wait_input('Starting channel: ')
		if resp_c in channels:
			valid = True
		else:
			Gui.inject_chat("Invalid channel.")
			valid = False

	Api.set_username(resp_u)
	username = resp_u
	
	channel = resp_c
	

	Gui.inject_chat("Joining...")
	Gui.switch_channel_user(channel, username)
	Gui.resize()
	messages = Api.poll_messages()
	
	
	

	### repeater function needs to be defined here in order to have variable access (I think?)
	class Threader( threading.Thread ):
		def run(self):
			messages = Api.poll_messages()
			Gui.put_buffer(messages)
			Gui.render_chatbox()
			time.sleep(baud)
			while running:
				messages = Api.poll_history(channel)
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
	
	debug_file = open("debug.kek", "w+")

	while running:
		uin = Gui.wait_input()
		if uin == "/quit":
			running = False
		elif "/user" in uin:
			if uin[6:] in usernames:
				username = uin[6:]
				Api.set_username(username)
				Gui.switch_channel_user(channel, username)
				Gui.inject_chat("User set to {}".format(username))
				channels = fullinfo[username].keys()
			else:
				Gui.inject_chat("Invalid username. Avaliable: ")
				for i in usernames:
					Gui.inject_chat(i)
			Gui.inject_chat("")
		elif "/channel" in uin:
			if uin[9:] in channels:
				Gui.switch_channel_user(uin[9:], username)
				Gui.inject_chat("Channel set to {}".format(uin[9:]))
				channel = uin[9:]
			else:
				Gui.inject_chat("You're not in {}".format(uin[9:]))
				Gui.inject_chat("Available channels for {}".format(username))
				for i in channels:
					Gui.inject_chat("- {}".format(i))
			Gui.inject_chat("")
		elif "/baud" in uin:
			try:
				baud = int(uin[6:])
			except:
				Gui.inject_chat("Bad polling rate : {}".format(uin))
			Gui.inject_chat("polling rate set to {}".format(baud))
			Gui.inject_chat("")
		elif "/help" in uin:
			Gui.inject_chat("/user <user>          : Switch to user")
			Gui.inject_chat("/channel <channel>    : Switch to channel")
			Gui.inject_chat("/baud <int>           : Set polling rate to <int>, default is 3")
			Gui.inject_chat("/quit                 : Exit")
			Gui.inject_chat("")
		elif "/debug" in uin:
			#Gui.inject_chat("{}".format(Api.get_fullinfo()))
			Gui.inject_chat("debug info:")
			Gui.inject_chat("")
		elif "/who" in uin:
			Gui.inject_chat(str(fullinfo[username][channel]))
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
