#!C:/Python27/python.exe
'''
Thanks to kbknapp for the shell menu script. I based this program
on his shell console menu program.

For any questions on the program please feel free to hit me up
at joejoejoey13@gmail.com. Thanks and take care.
'''
from __future__ import print_function

# Vendored Deps
import consolemenu

app_title = '{}\n###  Reg Helper  ###\n{}'.format('#'*20, '#'*20)
cm = consolemenu.ConsoleMenu('menu', title=app_title)
cm.start()
