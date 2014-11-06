#-*-coding:utf8-*-

#下载盗墓笔记小说
#2014-10-14
#ZJL

from bs4 import BeautifulSoup
import requests
import re
import os



#打开网页将所需的URL读取出来放进一个列表中
r = requests.get('http://www.nanpaisanshu.org/').content  #打开要读取的网页
content=BeautifulSoup(r).findAll('a',href=re.compile(r'\Ahttp://www.nanpaisanshu.org/[a-z]+\Z')) #在网页中找到需要的信息

sc = str(content) #转换为string类型

lists=[]
lists = sc.split(',')   
lists = list(set(lists)) #删除列表中重复信息

lisy=[]


for line in lists:
    p=line.split('"')[1]  #按 " 分割，取出需要的信息写进数组
    lisy.append(p)        #这里已经拥有需要的url
    #print p
#print lisy


#把读取到的URL遍历打开，将所有网页保存到html文件中

s = os.getcwd()#当前路径

d = os.sep  #系统分隔符

namef='aaa' #文件加名称

#b = os.path.exists( s+d+namef) #判断是存在

f=os.path.exists(s+d+namef) #判断是存在

if f==False:
    os.mkdir(s+d+namef)  #如果文件夹不存在就新建一个
else:
    print u'已经存在'+namef

filenm = s+d+namef+d    #路径

i=1
for line in lisy:
    r = requests.get(line)   #遍历打开所有url
    print r.content
    print '\n'
    tfile=open(filenm+'neirong'+str(i)+'.html','w')
    i=i+1
    tfile.write(r.content) #将网页内容写入文件

#将URL文件中的符合要求的URL读取出来写进一个txt文件中
for i in range(1,len(lisy)+1):
    fp = open(filenm+'neirong'+str(i)+'.html', "r")
    of = open(filenm+'neirong'+str(i)+'.txt','w')  
    content = fp.read()   #将文件内容读取

    p=re.compile(r'http://www\.nanpaisanshu\.org/.*?\.html') #正则匹配
    
    #print p.findall(content)

    #print type(p.findall(content))

    for line in p.findall(content):  
        #print line+'\n'
        #if line !='http://www.nanpaisanshu.org/9701.html':
        of.write(line+'\n')  #将匹配到的文件写入另一个文件中
        #else:
            #continue

        #of.write(str(p.findall(content)))

#关闭文件
of.close()
fp.close()
tfile.close()


#将txt

for i in range(1,len(lisy)+1):
    ot=open(filenm+'neirong'+str(i)+'.txt','r')
    if os.path.exists(filenm+'quanbu'+str(i)+'.txt'):
        print "已经存在"+filenm+'quanbu'+str(i)+'.txt'+'会先删除再创建'
        os.remove(filenm+'quanbu'+str(i)+'.txt')
        outfile=open(filenm+'quanbu'+str(i)+'.txt','a+')

    else:
        print "新建"+filenm+'quanbu'+str(i)+'.txt'
        outfile=open(filenm+'quanbu'+str(i)+'.txt','a+')


    
    li=[]
    for line in ot:
        line = line.replace('\n','')
        li.append(line)   #将url文件中的数据放进列表中

    li = sorted(li)  #给列表排序

    for line in li:
    #print line
        #line = line.replace('\n','')
        r = requests.get(line).content  #遍历打开所有url
        title=BeautifulSoup(r).find("div",{'class':"post_title"}).h2   #取出标题
        content=BeautifulSoup(r).findAll("div",{'class':"post_entry"}) #取出内容
        sti=str(title).replace('<h2>','').replace('</h2>','')  #处理标题，只保留文字

        #处理内容，只保留文字
        scon = str(content).replace('<p>','  ').replace('</p>','  ').replace('<br/>','\n')
        #print str(urllist)
        scon = re.sub("<.*>", "", scon)
        scon = re.sub("(.*?);","",scon) 
        #scon = scon.strip()
        scon = '\n'.join(scon.split())

        print scon
        outfile.write(sti+'\n'+scon) #将标题和内容写进文件中
    #i=i+1
    #print 
#print urllist

print '=========================下载结束======================='


#关闭文件
outfile.close()
ot.close()



#取出指定文件夹下的所有文件名
targetDir=s+d+namef
for line in os.listdir(targetDir):

    p=re.compile(r'neirong[0-9]{1}') #用正则匹配
    if p.match(line)!=None:
        print "需要删除的文件"+s+d+namef+d+line+'!!'
        os.remove(s+d+namef+d+line)  #匹配成功就删除这个文件，os.remove()中需要完整路径
    else:
        print '保留文件！'
        continue  


