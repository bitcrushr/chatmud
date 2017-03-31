import curses

class Graphics:
	def __init__(self, stdscr):
		curses.use_default_colors()
		#init
		self.stdscr = stdscr
		self.userlist = []
		self.channels = []
		self.inputbuffer = []
		self.linebuffer = []
		self.chatbuffer = []
		#curses h , w , y , x
		userlist_hwyx = (2, curses.COLS, 0,0)
		channels_hwyx = (curses.LINES, 8, 3, 0)
		
		chatbuffer_hwyx = (curses.LINES - 4, curses.COLS - 8, 3, 9)
		
		chatline_yx = (curses.LINES - 1, 9)
		
		self.win_userlist = stdscr.derwin(*userlist_hwyx)
		self.win_channels = stdscr.derwin(*channels1_hwyx)
		self.win_chatbuffer = stdscr.derwin(*chatbuffer_hwyx)
		self.win_chatline = stdscr.derwin(*chatline_yx)
		
		self.redraw_ui()
	
	def resize(self):
		u_h, u_w = self.win_channel.getmaxyx()
		h, w = self.stdscr.getmaxyx()
		
		self.win_userlist.mvwin(0,0)
		self.win_userlist.resize(2, w)
		
		self.win_channels.resize(h-2, 8)
		
		self.win_chatbuffer.resize(h - 5, w - 8)
		
		self.win_chatline.mvwin(h - 1, 9)
		self.win_chatline.resize(1, w - 8)
		
		self.linebuffer = []
		for msg in self.chatbuffer:
			self._linebuffer_add(msg)
		
		self.redraw_ui()
	
	def redraw_ui(self):
		h, w = self.stdscr.getmaxyx()
		u_h, u_w = self.win_userlist.getmaxyx()
		self.stdscr.clear()
		self.strscr.vline(2, u_w + 1, "|", h)
		self.stdscr.vline(2, 0, "|", h)
		self.stdscr.hline(2, 0, "-", w)
		self.stdscr.hline(h-3, 8, "-", w)
		self.stdscr.refresh()

		self.redraw_userlist()
		self.redraw_channels()
		self.redraw_chatbuffer()
		self.redraw_chatline()

	def redraw_chatline(self):
		h, w = self.stdscr.getmaxyx()
		self.win_chatline.clear()
		start = len(self.inputbuffer) - w + 8
		self.win_chatline.addstr(0,0, self.inputbuffer[start:])
		self.win_chatline.refresh()
	
	def redraw_channels(self):
		self.win_channels.clear()
		h, w = self.win_channels.getmaxyx()
		for i, name in enumerate(self.channels):
			if i >= h:
				break
			self.win_channels.addstr(i, 0, name[:w -1])
		self.win_channels.refresh()
	
	def redraw_userlist(self):
		self.win_userlist.clear()
		h, w = self.win_userlist.getmaxyx()
		self.win_userlist.addstr(0, 0, self.userlist[0])
		self.win_userlist.addstr(0, self.userlist[0].len, self.userlist[1])
		self.win_userlist.refresh()
	
	def redraw_chatbuffer(self):
		self.win_chatbuffer.clear()
		h, w = self.win_chatbuffer.getmaxyx()
		


