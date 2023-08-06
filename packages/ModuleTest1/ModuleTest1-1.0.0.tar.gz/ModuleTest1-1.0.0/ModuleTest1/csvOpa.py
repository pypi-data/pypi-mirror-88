import csv,os,sys,time,random,pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile,tarfile

class randGener():
    """
    生成随机字典
    """
    ks=['徐达','常遇春','蓝玉','刘基','李善长','李文忠','沐英']
    vs=[i*2-8 for i in range(47,54) ]

    def __init__(self,Keys=ks,Values=vs):
        self.__keys=Keys
        self.__values=Values
        # print('请注意元素个数需一致')

    def ch(self):
        if not isinstance(self.__values,list) or not isinstance(self.__keys,list):
            print('初始化数据有误，请输入列表参数')
            return False
        else:
            if len(self.__keys)!=len(self.__values):
                print('元素个数有误，请重新输入')
                for i in range(len(self.__keys)):
                    print(self.__keys[i],end=" ")
                print()
                for j in range(len(self.__values)):
                    print(self.__values[j],end=" ")
                return False
            else:
                print('初始化成功')
                return True

    @property
    def keys(self):
        return self.__keys

    @property
    def values(self):
        return self.__values

    @keys.setter
    def keys(self,newkeys):
        self.__keys=newkeys

    @values.setter
    def values(self,newvalues):
        self.__values=newvalues

    def gener(self):
        if self.ch():
            dit={}
            for i in range(len(self.__keys)):
                dit[self.__keys[i]]=self.__values[-1-i]
            return dit
        else:
            print('请重新输入数据')

class operCsvWithCsv():
    """


    """
    import os,sys,csv,pathlib
    """
    简单内容
    """
    br='HOMEPATH'
    rp=os.getenv(br)

    def __init__(self,fn,path=None):
        self.__fn = fn
        if path is None:
            path=''.join(['C:',peraCsv.rp])
            #path=os.chdir('c:/')
        self.__path = path

    def judge(self):
        """
        前期数据准备
        :return:
        """
        fn = self.__fn
        path=self.man()
        isFile = True
        pathobj = pathlib.Path(path)
        # print('pathobj:',pathobj)
        print('*'*30,'文件信息','*'*30)
        if not pathobj.is_dir():
            os.mkdir(path)
        if not (pathobj/fn).is_file():
            # print(pathobj/fn)
            # print((pathobj/"fn").is_file())
            # print('fn:',fn,'path:',path)
            isFile=False
            if fn.split('.')[-1] != 'csv':
                print('%r文件格式有误，请从新输入' %fn)
            else:
                an='是'
                print('是否新建:%r' % an)
        else:
            an='否'
            print('是否新建:%r' % an)
        print('路径:%r' %path)
        print('文件名:%r' %fn)
        print('*' * 30, '文件信息', '*' * 30)

    # @property
    # def path(self):
    #     return self.__path
    # @property
    # def fn(self):
    #     return self.__fn
    # @path.setter
    # def path(self,path):
    #     self.__path=path
    # @fn.setter
    # def fn(self,fn):
    #     self.__fn=fn

    def man(self):
        """
        前期数据准备
        :return:
        """
        path=self.__path
        path=path.replace('\\', '/', path.count('\\'))
        path=path.replace('\\\\','/',path.count('\\\\'))
        if path[-1]!='/':
            path=''.join([path,'/'])
        return path

    def csvRead(self):
        self.judge()
        path=self.man()
        fn=path+self.__fn
        if os.path.exists(fn):
            with open(fn,'r') as f:
                r_csv=csv.reader(f)
                for i in r_csv:
                    print(i)
        else:
            print('\n不存在该文件')

    def csvWrite(self):
        print('按行录入,元素之间用逗号隔开(键入~stop退出录入,键入~next换行):')
        b=True
        l1=[] # 文件信息
        l2=[] # 行信息
        m=n=0
        while b:
            row=input('请输入数据:\n')
            if row=='~stop':
                print('退出输入')
                # print('m:',m,'n:',n)
                # print('前l1:\n', l1)
                # print('前l2:\n', l2)
                if m!=n or m==0:
                    l1.append(l2)
                    # print('后l1:\n', l1)
                    # print('后l2:\n', l2)
                break
            elif row=='~next':
                l1.append(l2)
                l2=[]
                n+=1
                print('l1:\n',l1)
            else:
                l2.append(row)
                print('l2:\n',l2)
            m+=1
        print(l1)
        self.cw(l1)

    def cw(self,list):
        self.judge()
        path=self.man()
        n=self.__fn
        print(path)
        fn=path+self.__fn
        with open(fn,'a+',newline='') as f:
            w_csv=csv.writer(f)
            for i in range(len(list)):
                # print(len(list[i]),type(list[i]),type(list[i][0]),type(list[i][1]))
                # 未完成，存在csvWrite输入完毕，调用cw函数时传参list[i]的长度不为1的情况，即不输入~next时，
                # 立即输入数据时，会让数组长度大于1，并且
                print(list[i])
                if len(list[i])==1:
                    a=list[i][0]
                else:
                    a=list[i][0]
                # print('a:\n',a,type(a))
                a=a.replace('，',',',a.count('，'))
                # print('new a:',a)
                b=a.split(',')
                # print('b:\n',b)
                w_csv.writerow(b)
                #w_csv.writerow(list)
        print('录入完成')
        # 打开所在路径
        #path="d:/MyFiles/tmp"
        p=''
        lp=path.split('/')
        for i in lp:
            if i=='':
                lp.remove('')
        # print(lp)
        for i in range(len(lp)-1):
            p=''.join([p,lp[i],'/'])
        # print(p)
        # print(lp[-1])
        os.chdir(p)
        # print(os.getcwd())
        os.system('explorer /select,".\\%s"' %(lp[-1]+'\\'+n) )

class operCsvWithPD():
    """
    未完成
    """
    def __init__(self,path,filename):
        self.__path=path
        self.__fn=filename

    def gf(self):
        path=self.__path
        fn=self.__fn
        if fn.split('.')[-1]!='csv':
            print('文件名有误，请输入扩展名为csv的文件')
            if not os.path.exists(path):
                os.makedirs(path)
        npath=pathlib.Path(path)
        return npath,fn

    @property
    def path(self):
        return self.__path
    @property
    def fn(self):
        return self.__fn
    @path.setter
    def path(self,newpath):
        self.__path=newpath
    @fn.setter
    def fn(self,newfn):
        self.__fn=newfn

    def rcvs(self):
        path,fn=self.gf()
        df=pd.read_csv(path)




if __name__ == '__main__':
    # path=r'D:/Myfiles/tmp/'
    # fn='abc..csv'
    # fn1='练习.csv'
    # fn2='test2.csv'
    # fn3='mm.csv'
    # fn4='tt2.csv'
    # c1=peraCsvWithCsv(fn4,path)
    # c1.csvRead()
    # c1.csvWrite()
    # c1.csvRead()
    keys=['name','id','years','salary']
    d1=['张量','001','5','13000','add']
    rg1=randGener()
    d1=rg1.gener()
    for k,v in d1.items():
        print(k,v)




