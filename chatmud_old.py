#!/usr/bin/python

#imports

import sys
import os

import curses
import apimud

#vars

window = curses.initscr()
key = ''

users=[]

stop=False

#functions

def main():
	
	while stop == False:
		return
	return

def setchannel():
	return

def setuser():
	return

def init():
	curses.noecho() # for killing uinput
	curses.cbreak()
	window.keypad(True)
	curses.use_default_colors()
	window.clear()
	
	maxes = window.getmaxyx()
	my = maxes[0]
	mx = maxes[1]
	
	

def exit():
	curses.nocbreak()
	window.keypad(False)
	curses.echo() # for getting unput back
	curses.endwin()
	sys.exit()

def render():
	return

def worker():
	
	while stop == False:
		return
	return

init()
main()
exit()
