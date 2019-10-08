import requests
import re
import lxml
from bs4 import BeautifulSoup


url='https://www.pixiv.net/setting_user.php'
req2 = requests.get(url).text
bs = BeautifulSoup(req2, 'lxml').find('div',class_="settingContent")
print(bs.prettify())


