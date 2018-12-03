from njupt import Zhengfang

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        NoAlertPresentException,
                                        UnexpectedAlertPresentException,
                                        NoSuchFrameException,
                                        StaleElementReferenceException)
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains

import time
import config

accounts = config.getConfig("dada.conf", "account")
webdriverpath = config.getConfig("data.conf","config")[0][1]

class CzfAccount(Zhengfang):
    def __init__(self, account=None, password=None):
        super(CzfAccount, self).__init__()
        if account and password :
            self.account = account
            self.password = password
            self.login(account=self.account,password=self.password)
            self.cookiesDict = self.cookies
            self.firstTime = True

    def visitIndex(self,url):
        '''
        test
        :param url: API接口需要访问的URL,首页
        :return: NONE
        '''

        headers = {
            'Host': 'jwxt.njupt.edu.cn',
            'Origin': 'http://jwxt.njupt.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        html = self.get(url=url,headers=headers)
        print(html.text)


    def useSelenium(self,url):
        '''
        NONE
        :param url: NJUPT南邮正方首页
        :return: NONE
        '''
        self.driver = webdriver.Chrome(
            executable_path=webdriverpath)
        self.driver.implicitly_wait(1.5)  # 等待3秒还没有找到元素 。则抛出异常。
        self.driver.get('http://jwxt.njupt.edu.cn/default2.aspx')
        "技术提示：必须首先加载网站，这样Selenium 才能知道cookie 属于哪个网站，即使加载网站的行为对我们没任何用处"
        for key,value in self.cookiesDict.items():  #增加Cookie
            tmp = {
                'name':key,
                'value':value}
            self.driver.add_cookie(
                tmp
            )

        self.driver.get(url)
        self.driver.maximize_window()
        try:    # 处理完善信息的弹窗
            alert = self.driver.switch_to.alert
        except NoAlertPresentException:
            pass
        else:
            alert.accept()
        time.sleep(1)
        try:
            self.judgenav = self.driver.find_element_by_xpath('//*[@id="headDiv"]/ul[@class="nav"]/li[3]')
        except NoSuchElementException:
            print("接口未开放")
            return
        else:
            self.CompleteTest()

    def CompleteTest(self):
        '''
        循环遍历教学评价里的每一个li标签
        :return: NONE
        '''
        for i in range(1,50):        #==>NoSuchElementException
            try:
                action = ActionChains(self.driver)  # 第二组动作，需要重新申请
                navli = self.judgenav.find_element_by_xpath('ul/li[{}]'.format(i))
                action.move_to_element(self.judgenav).move_to_element(navli).click().perform() #点击学科
                time.sleep(0.5)   #必须等待一会,不然无法检测到弹弹窗

                try:  # 处理点击学科时出现的弹窗
                    alert = self.driver.switch_to.alert
                except NoAlertPresentException or UnexpectedAlertPresentException:
                    pass
                else:
                    alert.accept()
                    
                self.singlePagejudge()

            except NoSuchElementException as e:
                print("全部已完成选择,10秒后将提交")
                print(e)
                for t in range(10):
                    time.sleep(1)
                    print("{}s...".format(10-t))
                self.submitJudge()
            except StaleElementReferenceException:
                print("全部评价已经完成")

    def singlePagejudge(self):
        '''
        教学评价里的每一个li标签中各个学科的具体评价页面的操作
        :return: NONE
        '''
        try:
            self.driver.switch_to.frame('zhuti')
        except NoSuchFrameException:
            return

        try:
            # for y in range(1, 5):       #多位老师,使用不了.需要优化
            #     if y < 3:  # 前两个是大写JS
            #         judgewidget = self.driver.find_element_by_xpath(
            #             '//select[@id="DataGrid1__ctl{}_JS{}"]'.format(x, y))
            #     else:  # 后面的是大写JS
            #         judgewidget = self.driver.find_element_by_xpath(
            #             '//select[@id="DataGrid1__ctl{}_js{}"]'.format(x, y))
            for x in range(2, 30):
                judgewidget = self.driver.find_element_by_xpath(
                        '//select[@id="DataGrid1__ctl{}_JS1"]'.format(x))
                if x == 7:
                    Select(judgewidget).select_by_index(2)  # 勉强满意
                else:
                    Select(judgewidget).select_by_index(1)  # 完全认同
                time.sleep(0.05)
        except NoSuchElementException:      #全部选项已经填完
            print("当前页已完成")
            self.driver.find_element_by_xpath('//*[@id="Button1"]').click()  # 按下保存按钮

            time.sleep(0.3)
            try:  # 处理第二次所有评价都完成后的   "所有评价已完成，现在可以提交！"弹窗
                alert = self.driver.switch_to.alert
            except NoAlertPresentException or UnexpectedAlertPresentException:
                pass
            else:
                alert.accept()

            time.sleep(0.5)
            self.driver.switch_to.parent_frame()    # 完成一个页面后,要切回主frame

    def submitJudge(self):
        '''
        页面保留在最后一个完成的学科评价上,由于会切换为parent_frame,此时只需要再切换为zhuti,然后点击提交就行了
        :return: NONE
        '''
        try:
            self.driver.switch_to.frame('zhuti')
        except NoSuchFrameException:
            return
        submitBtn = self.driver.find_element_by_xpath('//*[@id="Button2"]')
        submitBtn.click()                # 提交
        
        time.sleep(1)
        try:  # 处理提交后"提交完成"的弹窗
            alert = self.driver.switch_to.alert
        except NoAlertPresentException or UnexpectedAlertPresentException:
            pass
        else:
            alert.accept()

        self.driver.switch_to.parent_frame()

        if self.firstTime == True:
            time.sleep(1)
            self.CompleteTest()
            self.firstTime = False


if __name__ == "__main__":
    for account in accounts:
        UID , PWD = account
        zf = CzfAccount(UID, PWD)
        print("登录成功")
        zf.useSelenium('http://jwxt.njupt.edu.cn/xs_main.aspx?xh={}#a'.format(UID))

