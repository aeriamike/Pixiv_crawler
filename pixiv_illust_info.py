import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
'''
class Pixiv():

    def __init__(self, search, page):
        self.search = search
        self.page = page
        self.result = set()
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}

    @property
    def cookies(self):
        with open("cookies.txt", 'r') as f:
            _cookies = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                _cookies[k] = v
            print("success 1?"+'\n')
            return _cookies

    def run(self):
         url = 'https://www.pixiv.net/ranking.php?mode=oversea&date=20180729'
         req = requests.get(url, headers=self.headers, cookies=self.cookies).text
         bs = BeautifulSoup(req, 'lxml').find('div', class_="ranking-items-container")
         #print(bs.prettify() + '\n')
         #print("success 2?"+'\n')

         for b in bs.find_all('section', class_="ranking-item"):
            #print(b.prettify())
             print(b['data-rank'])
             print(b['data-title'])
             print(b['data-user-name'])
             
             href = b.find('a', href=True, class_="work _work ")
             #print(href)

             div = b.find('div', class_ = "_one-click-bookmark js-click-trackable ")
             picref = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+div['data-click-label']
             print(picref)
             print(div['data-type'])
             print('\n')

            

if __name__ == "__main__":
    spider = Pixiv("summer", 2)
    spider.run()
'''


'''
url2 = 'https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=69830967&page=0'
referer = 'https://www.pixiv.net/member_illust.php?mode=manga&illust_id=69830967'
req = requests.get(url2).text

#original image format
#'https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=69830967&page=0'

bs2 = BeautifulSoup(req, 'lxml')

for a_image in bs2.findAll('body'):
    print (a_image.prettify())
   
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
            # 加载cookie
            self.session.cookies.load(filename='cookies', ignore_discard=True)
        except:
            print('cookies不能加载')

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
        login_url = 'https://accounts.pixiv.net/login' # 登陆的URL
        # 获取登录页面
        res = self.session.get(login_url, params=self.params)
        # 获取post_key
        pattern = re.compile(r'name="post_key" value="(.*?)">')
        r = pattern.findall(res.text)
        self.datas['post_key'] = r[0]

    def already_login(self):
        # 请求用户配置界面，来判断是否登录
        url = 'https://www.pixiv.net/setting_user.php'
        login_code = self.session.get(url, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def login(self, account, password):
        post_url = 'https://accounts.pixiv.net/api/login?lang=en' # 提交POST请求的URL
        # 设置postkey
        self.get_postkey()
        self.datas['pixiv_id'] = account
        self.datas['password'] = password
        # 发送post请求模拟登录
        result = self.session.post(post_url, data=self.datas)
        print(result.json())
        # 储存cookies
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        return self
        
    def image (self):
        
        url2 = 'https://www.pixiv.net/ranking.php?mode=oversea&date=20190729'
        referer = 'https://www.pixiv.net/ranking.php?mode=oversea&date=20190729'
        req2 = requests.get(url2, headers=self.session.headers, cookies=self.session.cookies).text
        soup = BeautifulSoup(req2, 'lxml')
        print(soup.prettify())
        
        #print("am i here?"+'\n')
        #bs = BeautifulSoup(req2, 'lxml').find('')
        for link in soup.find_all('span'):
            print(link)
        
            
    
        
        
        url2 = 'https://i.pximg.net/img-original/img/2019/07/24/01/17/33/75880135_p0.jpg'
        #referer = 'https://www.pixiv.net/ranking.php?mode=oversea&date=20180729'
        req2 = requests.get(url2, headers=self.session.headers, cookies=self.session.cookies).text
        reso = requests.get(url2, headers=self.session.headers, cookies=self.session.cookies)
        print("am i here?"+'\n')
        #bs = BeautifulSoup(req2, 'lxml').find('body')
        image = Image.open(io.BytesIO(reso.content))
        f = open('testimage.jpg','wb')
        f.write(requests.get(url2, headers=self.session.headers, cookies=self.session.cookies).content)
        f.close
        
        
       
        
       # print(bs.prettify())

if __name__ == "__main__":
    spider = PixivSpider()
    if spider.already_login():
        print('用户已经登录')

        
    else:

        account = input('请输入用户名\n> ')
        password = input('请输入密码\n> ')
        spider.login(account, password)
    spider.image()

   
