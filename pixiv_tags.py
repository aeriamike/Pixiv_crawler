#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import csv
import random

'''
source = requests.get('https://web.archive.org/web/20160614144700/https://www.pixiv.net/tags.php').text
soup = BeautifulSoup(source, 'lxml').find('ul')
print(soup.prettify())
'''

import requests
import re
import http.cookiejar
from bs4 import BeautifulSoup
from PIL import Image


class PixivSpider(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
             'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=69845158'}
        self.session.headers = self.headers
        self.session.cookies = http.cookiejar.LWPCookieJar(filename='cookies')
        try:
            # load cookie
            self.session.cookies.load(filename='cookies', ignore_discard=True)
        except:
            print('error: cookies cannot be loaded')

        self.params ={
            'lang': 'en',
            'source': 'pc',
            'view_type': 'page',
            'ref': 'wwwtop_accounts_index'
        }
        self.datas = {
            'pixiv_id': '',
            'password': '',
            'captcha': '',
            'g_reaptcha_response': '',
            'post_key': '',
            'source': 'pc',
            'ref': 'wwwtop_accounts_indes',
            'return_to': 'https://www.pixiv.net/'
            }

    def get_postkey(self):
        login_url = 'https://accounts.pixiv.net/login' # go to login url
        
        res = self.session.get(login_url, params=self.params)
        
        pattern = re.compile(r'name="post_key" value="(.*?)">')
        r = pattern.findall(res.text)
        self.datas['post_key'] = r[0]

    def already_login(self):
        # check if the user is logged in
        url = 'https://www.pixiv.net/setting_user.php'
        login_code = self.session.get(url, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def login(self, account, password):
        post_url = 'https://accounts.pixiv.net/api/login?lang=en' # processing account
  
        self.get_postkey()
        self.datas['pixiv_id'] = account
        self.datas['password'] = password
    
        result = self.session.post(post_url, data=self.datas)
        print(result.json())
        # use cookie to remain logged in the future
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        return self
        
    def image (self):
        '''
        url2 = 'https://www.pixiv.net/bookmark.php?type=reg_user'
        #referer = 'https://www.pixiv.net/ranking.php?mode=oversea&date=20180729'
        req2 = requests.get(url2, headers=self.session.headers, cookies=self.session.cookies).text
        print(req2)
        print("am i here?"+'\n')
        bs = BeautifulSoup(req2, 'lxml').find('div',class_='members')
        
        print(bs.prettify())
        '''
        '''
        source = requests.get('https://www.pixiv.net/tags.php').text
        soup = BeautifulSoup(source, 'lxml')
        for a in soup.find('div', class_='column-content'):
            print(a.prettify())
        '''
        date = ['201401','201402','201403','201404','201405','201406'
                ,'201407','201408','201409','201410','201411','201412',
                '201501','201502','201503','201504','201505','201506',
                '201507','201508','201509','201510','201511','201512',
                '201601','201602','201603','201604','201605','201606',
                '201607','201608','201609','201610','201611','201612',
                '201701','201702','201703','201704','201705','201706',
                '201707','201708','201709','201710','201711','201712',
                '201801','201802','201803','201804','201805','201806',
                '201807','201808','201809','201810','201811','201812',
                '201901','201902','201903','201904','201905','201906',]
        taglist = []
        countlist = []
        datalist = []
        
        i = 1
        for i in range(1,len(date)):

            source = requests.get('https://web.archive.org/web/' + date[i] +'01/http://www.pixiv.net/tags.php').text
            soup = BeautifulSoup(source, 'lxml')
            #for access in soup.find('div', class_='column-content'):
                #print(access.prettify())
                #print(access)
            #print('the date is ' + date[i])
            
            num = 0
            #for access in soup.find_all('a',class_='tag-name icon-text'):
            for access in soup.find_all('li'):
                if num < 10:
                    
                    tag = access.find('a',class_='tag-name icon-text')
                    count = access.find('span',class_='count-badge')
                    datenow =  date[i][:4]+"-"+date[i][4:] 
                    try:
                        print(tag.string)
                        print(count.string)
                        print(datenow)
                        
                        #print(count.string)
                        #print(access.prettify())
                        
                        num = num+1
                        taglist.append(tag.string)
                        countlist.append(count.string)
                        datalist.append(datenow)
        
                    
                    except AttributeError:
                        pass;

                   
                else:
                    break;

        #print (taglist)
        #print (countlist)
        #print (datalist)
       

        thefile = open("pixiv_tag.txt",'w')
        for item in taglist:
            thefile.write("%s\n" %item)
        thefile = open("pixiv_count.txt",'w')
        for item in countlist:
            thefile.write("%s\n" %item)

        thefile = open("pixiv_date.txt",'w')
        for item in datalist:
            thefile.write("%s\n" %item)

        thefile2 = open("pixiv_tagresult3.txt",'w')
        thefile2.write("name,type,value,date\n")
        ii = 0
        for ii in range(0,len(taglist)):
            thefile2.write("%s," %(taglist[ii]))
            radi = random.choice("vwxyz")
            thefile2.write(radi+",")
            thefile2.write("%s,%s\n" %(countlist[ii],datalist[ii]))
            
        '''
        with open("pixiv_tag.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(taglist)
       '''
        
       # print(bs.prettify())

if __name__ == "__main__":
    spider = PixivSpider()
    if spider.already_login():
        print('The user is already logged in')

        
    else:
        print('Pixiv Crawler - check out tags top 10 ranking\n')
        account = input('Enter your username\n> ')
        password = input('Enter your password\n> ')
        spider.login(account, password)
    spider.image()

   

