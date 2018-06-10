"""
1. python -m pip install selenium
   python -m pip install bs4
2. refer to https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/
3. chromedriver.exe can be downloaded in https://sites.google.com/a/chromium.org/chromedriver/downloads
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import threading



class Login(object):
    def __init__(self,*args,**argv):
        self.id = argv["id"]
        self.password = argv["password"]
        self.driver = None
        
    def connect(self):
        # if you want to use headless chrome, enable below comments
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        #options.add_argument('window-size=1920x1080')
        #options.add_argument("disable-gpu")    
    
        self.driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=options)
        self.driver.implicitly_wait(2)
        self.driver.get('https://www.ppomppu.co.kr/zboard/login.php')
        self.driver.find_element_by_name('user_id').send_keys(self.id)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="zb_login"]/ul/a/li').click()
        
    def disconnect(self):
        self.driver.close()
        
class RemoveComment(threading.Thread, Login):
    def __init__(self, *args, **argv):
        threading.Thread.__init__(self) 
        Login.__init__(self,*argv, **argv)
        self.links = argv["links"]  # links is list of dict(link, desc)
        self.value = argv["value"]
        
    def run(self):
        super().connect()
        for link in self.links:
            """ link[0] = link, link[1] = desc """
            starttime = time.time()
            self._ModifyComment(link, value = self.value)
            print("%s %s : %f s" % (link[0],link[1],time.time()-starttime))
            
    def _ModifyComment(self, link, value = "pung"):
        if link[1] == value:
            print("%s %s Already is changed" % (link[0], link[1]))
            return
            
        self.driver.get(link[0])
        a = re.compile(r"cno=\d+")
        comment_num = a.search(link[0]).group().replace("cno=","")
        
        # click the modify button
        try:
            self.driver.find_element_by_xpath('//*[@id="comment_%s"]/div[1]/table/tbody/tr/td[6]/a' % comment_num).click()
        except:
            # QnA query
            self.driver.find_element_by_xpath('//*[@id="ex3"]/div[3]/div[1]/a').click()
            self.driver.find_element_by_xpath('//*[@id="comment_%s"]/div[1]/table/tbody/tr/td[6]/a' % comment_num).click()
            
        self.driver.find_element_by_xpath('//*[@id="memo"]').clear()
        self.driver.find_element_by_xpath('//*[@id="memo"]').send_keys(value)    
        # click the complete button
        self.driver.find_element_by_xpath('//*[@id="comment_write_form"]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td[2]/input[1]').click()

class RemovePost(threading.Thread, Login):
    def __init__(self, *args, **argv):
        threading.Thread.__init__(self) 
        Login.__init__(self,*argv, **argv)
        self.links = argv["links"]  # links is list of dict(link, desc)
        self.value = argv["value"]
        
    def run(self):
        super().connect()
        for link in self.links:
            """ link[0] = link, link[1] = desc """
            starttime = time.time()
            self._ModifyPost(link, value = self.value)
            print("%s %s : %f s" % (link[0],link[1],time.time()-starttime))    
            
    def _ModifyPost(self, link, value = "pung"):     
        if link[1] == value:
            print("%s %s Already is changed" % (link[0], link[1]))
            return
    
        self.driver.get(link[0])
        # click the modify button
        try:
            self.driver.find_element_by_xpath('//*[@id="revolution_main_table"]/tbody/tr[1]/td/a[1]/font').click()                                              
        except: # other warning message occurs, handle to exception
            self.driver.find_element_by_xpath('//*[@id="ex3"]/div[3]/div[1]/a').click()
            self.driver.find_element_by_xpath('//*[@id="revolution_main_table"]/tbody/tr[1]/td/a[1]/font').click()        
            
        # modify subject
        self.driver.find_element_by_xpath('//*[@id="divSubject"]/td[2]/input').clear()    
        self.driver.find_element_by_xpath('//*[@id="divSubject"]/td[2]/input').send_keys(value)    

        
        # modify body
        remain = '/div[6]/div[2]'
        remain2 = '/div[2]/textarea'
        xpath = ''
        for ii in range(10,13):
            xpath = '/html/body/div[6]/div[2]/div[4]/div/form/table/tbody/tr/td/table[2]/tbody/tr[%d]/td[2]/div[3]' % (ii)
            try:
                self.driver.find_element_by_xpath(xpath+remain)
                break
            except:
                continue        
        
        self.driver.find_element_by_xpath(xpath+remain).click()    
        self.driver.find_element_by_xpath(xpath+remain2).clear()    
        self.driver.find_element_by_xpath(xpath+remain2).send_keys(value)    

        self.driver.find_element_by_xpath('//*[@id="ok_button"]').click()
    
class ParseHistory(Login):
    def __init__(self, *args, **argv):
        Login.__init__(self,*argv, **argv)

    def __parseHtml(self, f):
        s = BeautifulSoup(f, 'html.parser')
        s = s.select(".left")
        l = list()
        for ii in s:        
            l += (ii.select('a[href^="http://www.ppomppu.co.kr/zboard/view"]'))

        out = dict()
        for o in l:
            if(o.get_text() != ""):
                out.update({o.get("href") : o.get_text()})
        return out
        
    def find_post_path(self,start, end):
        """ search your post history page """
        out = dict()
        for pageNum in range(start, end):
            self.driver.get('http://www.ppomppu.co.kr/myinfo/member_my_write_list.php?page=%d&search_type=subject&keyword=' % pageNum)
            html = self.driver.page_source
            out.update(self.__parseHtml(html))
        return list(out.items())

    def find_comment_path(self,start, end):
        """ search your comment history page """
        out = dict()
        for pageNum in range(start,end):                    
            self.driver.get('http://www.ppomppu.co.kr/myinfo/member_my_comment_list.php?page=%d&search_type=memo&keyword=' % pageNum)
            html = self.driver.page_source
            out.update(self.__parseHtml(html))
        return list(out.items())
        
if __name__ == '__main__':
    your_id = "mmysun88"
    your_password = "gnswkd88**"        
            
    # get your comment / post history
    parser = ParseHistory(id=your_id,password=your_password)
    parser.connect()    # login
    postLinks = parser.find_post_path(2,10)  # input the page range removed (http://www.ppomppu.co.kr/myinfo/member_my_comment_list.php?page=1&search_type=memo&keyword=) 
    commentLinks = parser.find_comment_path(2,10)    # input the page range removed (http://www.ppomppu.co.kr/myinfo/member_my_write_list.php?page=1&search_type=subject&keyword=) 
    parser.disconnect() # logout end close chrome

    postLinksLen = len(postLinks)   # divide the post history for using threading
    commentLinksLen = len(commentLinks)

    print(postLinks)
    print(commentLinks)

    # ready to remove
    th = list()
    th.append(RemovePost(links=postLinks[:int(postLinksLen/2)], value="bye22",id=your_id,password=your_password))
    th.append(RemoveComment(links=commentLinks[:int(commentLinksLen/2)], value="bye22",id=your_id,password=your_password))
    th.append(RemovePost(links=postLinks[int(postLinksLen/2):], value="bye22",id=your_id,password=your_password))
    th.append(RemoveComment(links=commentLinks[int(commentLinksLen/2):], value="bye22",id=your_id,password=your_password))


    for ii in th:
        ii.start()
    for ii in th:
        ii.join()