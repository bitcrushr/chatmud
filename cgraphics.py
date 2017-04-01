import curses
import re

def scrape(message):
	message = re.sub(r"(`[A-Za-z])", "", message)
	message = message.replace("`", "")
	return message

class Graphics():
	def __init__(self, stdscr):
		self.stdscr = stdscr
		self.chatbuffer = {}
		self.inputbuffer = ""
		self.linebuffer = []
		self.helpindex = 0
		self.regindex = 0
		self.channel = ''
		self.user = ''

		self.chatbox_hwyx = (curses.LINES - 3, curses.COLS, 0, 0)
		pos = curses.LINES-1
		self.inputbox_hwyx = (3, curses.COLS, curses.LINES - 3, 0)
		
		self.win_chatbox = stdscr.derwin(*self.chatbox_hwyx)
		self.win_inputbox = stdscr.derwin(*self.inputbox_hwyx)
		
		self.resize()

	def inject_chat(self, msg):
		
		self.linebuffer.append(msg)
		self.render_chatbox()
	
	def resize(self):
		h, w = self.stdscr.getmaxyx()
		try:
			self.win_chatbox.mvwin(0,0)
			self.win_chatbox.resize(h-3, w)
		except:
			pass

		try:
			self.win_inputbox.mvwin(h-3, 0)
			self.win_inputbox.resize(3, w)
		except:
			pass

		self.render()

	def render(self):
		h, w = self.stdscr.getmaxyx()
		self.stdscr.clear()
		self.stdscr.refresh()
		self.render_chatbox()
		self.render_inputbox()

	def put_buffer(self, buff):
		if buff != {}:
			for i in buff:
				if 'channel' in i:
					if i['channel'] == self.channel:
						self.linebuffer.append( "{} // {} :".format(i['t'], i['from_user']) )
						thinglist = i['msg'].splitlines()
						for i in thinglist:
							if i:
								self.linebuffer.append( scrape( i ) )
							if len(i) > curses.COLS:
								iterator = int(len(i) / curses.COLS)
								while iterator > 0:
									self.linebuffer.append( "" )
									iterator -= 1
						self.linebuffer.append( "" )
		
		self.render_chatbox()

	def switch_channel_user(self, channel, user):
		self.user = user
		self.channel = channel
		self.regindex = 0
		self.render()
	
	def render_chatbox(self):
		self.win_chatbox.clear()
		h, w = self.win_chatbox.getmaxyx()
		j = len(self.linebuffer) - h
		if j < 0:
			j = 0
		for i in range(min(h, len(self.linebuffer))):
			try:
				self.win_chatbox.addstr(i, 0, self.linebuffer[j])
			except:
				self.inject_chat("")
			j += 1
			self.win_chatbox.refresh()
		self.stdscr.refresh()
	
	def render_inputbox(self):
		h, w = self.win_inputbox.getmaxyx()
		self.win_inputbox.clear()
		string = "{} @ {} : {}".format(self.user, self.channel, self.inputbuffer)
		if len(string) > w - 5:
			start = len(string) - w + 5
			string = string[start:]
		self.win_inputbox.addstr(1, 0, string)
		self.win_inputbox.refresh()
		


	def prompt(self, msg):
		self.inputbuffer = msg
		self.render_inputbox()
		res = self.wait_input()
		res = res[len(msg):]
		return res

	def wait_input(self, prompt=""):
		self.inputbuffer = prompt
		self.stdscr.refresh()
		self.render_inputbox()
		self.win_inputbox.cursyncup()
		last = -1
		while last != ord('\n'):
			last = self.stdscr.getch()
			if last == ord('\n'):
				tmp = self.inputbuffer
				self.inputbuffer = ""
				self.render_inputbox()
				self.win_inputbox.cursyncup()
				return tmp[len(prompt):]
			elif last == curses.KEY_BACKSPACE or last == 127:
				if len(self.inputbuffer) > len(prompt):
					self.inputbuffer = self.inputbuffer[:-1]
					self.render_inputbox()
			elif last == curses.KEY_RESIZE:
				self.resize()
			elif 32 <= last <= 126:
				self.inputbuffer += chr(last)
				self.render_inputbox()
	def kill(self):
		curses.echo()
		curses.nocbreak()
		self.stdscr.keypad(0)
		curses.endwin()
