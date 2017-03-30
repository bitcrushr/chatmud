#!/usr/bin/python

#imports

import sys
import os

import curses
import apimud

window = curses.initscr()
key = ''

#functions

def main():
	return

def setchannel():
	return

def init():
	curses.noecho()
	curses.cbreak()
	window.keypad(True)
	window.clear()
	

def exit():
	curses.nocbreak()
	window.keypad(False)
	curses.echo()
	curses.endwin()
	
	sys.exit()

init()
main()
exit()
