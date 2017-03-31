import chatapi
import os
import sys
import re

def scrape(message):
	message = re.sub(r"(`[A-Za-z])", "", message)
	message = message.replace("`", "")
	return message

def main():
	os.system("clear")
	print("Enter your token pls:")
	print("6s28ukxCergAanzjTgXw")
	resp = "6s28ukxCergAanzjTgXw"
	Api = chatapi.API(resp)
	if Api.login():
		print("Logged in with {}".format(Api.token))
	Api.set_username("ratiasu")
	Api.send_chat_to_channel("0234", "nuutest")
	messages = Api.poll_messages()
	for i in messages:
		print("{} // {}".format(i['t'],i['from_user']))
		print(scrape(i['msg']))

main()
