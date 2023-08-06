from __future__ import print_function
from os.path import join,getsize
import os,sys,time,random,gc,datetime,io,csv,copy
import email,smtplib,xlrd,xlwt,xlutils,xdrlib,time,xlsxwriter
import base64,json,logging,threading,optparse,functools
import appium,selenium,decimal,math,pdb,turtle
import torch,torchvision,pathlib
import urllib3 as ul3
import requests as rqs
import bs4,cv2,folium
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.stats import norm
from turtle import *

# 异常的结构
def expt(a,b):
    import traceback
    try:
        excTest(a,b)
    except ValueError as e1:
        print('捕获的异常是:',e1) #捕获异常语句
    except ZeroDivisionError as e2:
        traceback.print_exc()
    except SyntaxError as e3:
        with open("D:/MyFiles/tmp55/3.txt",'w') as f:
            traceback.print_exc(file=f)  # 将捕获的异常写到f文件中
    except BaseException as e:
        print('捕获的异常是:',e)  #应该是先子类异常再到父类异常
    else:
        pass   # 如果不发生异常则继续执行该语句
    finally:
        pass   # 无论是否发生异常，该句都会执行，通常用作释放资源
        try:   # 多重try语句的嵌套
            pass
        except BaseException as e:
            print('捕获的异常是:', e)  # 局部变量不能传到该层之外
        finally:
            pass
    return "e"  # 一般return语句不放在try语句中，否则容易出先各种未知的错误
def excTest(a,b):
    # 传入异常检测语句的语句块，可以随意定义各种运算
    return a/b
    pass

# 自定义异常类

class AgeError(Exception):

    def __init__(self,errorinfo): # 构造器
        Exception.__init__(self) # 调用父类的构造方法
        self.errorinfo=errorinfo
    def __str__(self):
        return str(self.errorinfo)+"年龄错误!,应该在0-150岁之间"

if __name__ == '__main__':
    #expt(5, 10)
    age=int(input('输入你的年龄:'))
    if age<0 or age>150:
        raise AgeError(age)
    else:
        print('正常的年龄:',age)