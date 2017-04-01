import os
import sys
import re

	
def scrape(message):
	message = re.sub(r"(`[A-Za-z])", "", message)
	message = message.replace("`", "")
	return message



class Graphics:
	def __init__(self):
		self.last_chatbuffer = {}
		self.chatbuffer = {}
		self.inbuffer = ''
		pass
	
	def render(self, buff, channel, user):
		self.last_chatbuffer = self.chatbuffer
		self.chatbuffer = buff
		if str(self.last_chatbuffer) != str(self.chatbuffer):
			for i in self.chatbuffer:
				if i['channel'] == channel:
					print("{} // {}".format(i['t'],i['from_user']))
					print( scrape( i['msg']) )
					print("")
			print("{}@{}".format(user, channel))

	def wait_input(self):
		self.inbuffer = input()
		return self.inbuffer
