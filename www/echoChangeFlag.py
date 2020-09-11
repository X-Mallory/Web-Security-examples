# -*- coding:utf-8 -*-
import os


flag = raw_input('please input new flag:')
os.system('echo ' + flag + ' > flag.txt')
