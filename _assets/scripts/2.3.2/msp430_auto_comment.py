# coding:utf-8
"""
 *@Projet  IOT security wiki
 *@Desc    msp430 auto comment script
 *@Url     www.iot-security.wiki
"""
from idaapi import *

file = open("msp430g2553.h",'r')
lines = file.readlines()
funcs = Functions()
for f in funcs:
	for i in FuncItems(f):
		try:
			if idc.GetOpnd(i,0)[0]=='&':
				for line in lines:
					if line.find(idc.GetOpnd(i,0)[1:].replace('h','',1)) != -1:
						line.expandtabs()
						words = line.split(' ')
						MakeComm(i,words[1][:-1])
						break
			if idc.GetOpnd(i,1)[0]=='&':
				for line in lines:
					if line.find(idc.GetOpnd(i,1)[1:].replace('h','',1)) != -1:
						line.expandtabs()
						words = line.split(' ')
						MakeComm(i,words[1][:-1])
						break
		except :
			continue
