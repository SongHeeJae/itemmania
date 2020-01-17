from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import datetime
import math

class WriteInfo: # 글 작성 정보
    def __init__(self, start, end, title, description, count):
        self.start = start # 분할 시 최소 액수
        self.end = end # 분할 시 최대 액수
        self.title = title # 글 제목
        self.description = description # 글 내용
        self.count = int(count) # 작성할 글 개수
        pass

class ServerPrice: # 서버별 글 작성 정보
    def __init__(self, server, price, char_name) :
        self.server = server
        self.price = price
        self.char_name = char_name
        pass

class Itemmania:

    def __init__(self, user_id, user_password, write_info) :
        self.list = {}

        # 서버 목록 초기화
        self.list['엘리시움'] = "javascript:fnSearchSelect('138','메이플스토리','9942','엘리시움','3',this)"
        self.list['오로라'] = "javascript:fnSearchSelect('138','메이플스토리','11187','오로라','3',this)"
        self.list['이노시스'] = "javascript:fnSearchSelect('138','메이플스토리','8901','이노시스','3',this)"
        self.list['RED'] = "javascript:fnSearchSelect('138','메이플스토리','9238','RED','3',this)"
        self.list['제니스'] = "javascript:fnSearchSelect('138','메이플스토리','662','제니스','3',this)"
        self.list['아케인'] = "javascript:fnSearchSelect('138','메이플스토리','13208','아케인','3',this)"
        self.list['노바'] = "javascript:fnSearchSelect('138','메이플스토리','14218','노바','3',this)"
        self.list['루나'] = "javascript:fnSearchSelect('138','메이플스토리','10102','루나','3',this)"
        self.list['유니온'] = "javascript:fnSearchSelect('138','메이플스토리','8990','유니온','3',this)"
        self.list['베라'] = "javascript:fnSearchSelect('138','메이플스토리','658','베라','3',this)"
        self.list['스카니아'] = "javascript:fnSearchSelect('138','메이플스토리','660','스카니아','3',this)"
        self.list['크로아'] = "javascript:fnSearchSelect('138','메이플스토리','664','크로아','3',this)"
        self.my_list = [] # 구매 등록할 서버 리스트
        self.user_id = user_id
        self.user_password = user_password
        self.write_info = write_info
        pass

    def add_list(self, server, price, char) : # 구매 등록 서버 하나 추가
        self.my_list.append(ServerPrice(server, price, char))
        pass


    def login(self) : # 로그인
        self.driver = webdriver.Chrome('chromedriver.exe')
     
        self.driver.implicitly_wait(3)  # 대기

        self.driver.get('https://www.itemmania.com/portal/user/p_login_form.html')
        self.driver.implicitly_wait(3)

        self.popup()

        self.driver.find_element_by_id('user_id').send_keys(self.user_id)
        self.driver.find_element_by_id('user_password').send_keys(self.user_password)
        self.driver.execute_script('login_security()')
        sleep(3)

        pass

    def popup(self):
        handle = self.driver.window_handles

        # 팝업창 처리
        if len(handle) > 1:
                self.driver.switch_to.window(handle[1])
                self.driver.close()

        self.driver.switch_to.window(handle[0])
        

    def write_buy(self) : # 구매 등록글 작성

        count = 0
        while count < self.write_info.count :

            first = datetime.datetime.now()

            for ml in self.my_list :
                self.write_buy_post(ml)

            end = datetime.datetime.now()

            self.wait_delay(first, end)

            count += 1

        pass

    def write_buy_post(self, ml) :

        self.driver.get('http://www.itemmania.com/buy/?type=general')
        self.driver.implicitly_wait(3)

        self.driver.execute_script(self.list[ml.server])
        sleep(1)
        self.driver.find_element(By.XPATH, '//input[@value="division"]').click()
        sleep(0.5)
        self.driver.find_element(By.XPATH, '//input[@value="억"]').click()
        sleep(0.5)
        self.driver.find_element_by_id('user_quantity_min').send_keys(self.write_info.start)
        sleep(0.3)
        self.driver.find_element_by_id('user_quantity_max').send_keys(self.write_info.end)
        sleep(0.3)
        self.driver.find_element_by_id('user_division_unit').send_keys('1')
        sleep(0.3)
        self.driver.find_element_by_id('user_division_price').send_keys(ml.price)
        sleep(0.3)
        self.driver.find_element_by_id('user_character').send_keys(ml.char_name)
        sleep(0.3)
        self.driver.execute_script('document.getElementById("user_title").value = "' + self.write_info.title + '"')
        sleep(0.3)
        self.driver.find_element(By.XPATH, '//input[@value="1" and @class="g_radio"]').click()
        sleep(0.3)
        self.driver.execute_script('document.getElementById("user_text").value = "' + self.write_info.description + '"')
        sleep(0.3)

        self.driver.find_element_by_id('ok_btn').click()
        sleep(2)

        self.driver.find_element(By.XPATH, '//img[@alt="확인"]').click()
        sleep(1)
        self.driver.find_element(By.XPATH, '//img[@src="http://img3.itemmania.com/new_images/btn/btn_pop_ok_g.gif"]').click()
  
        sleep(3)

        pass

    def update(self) : # 재등록
        self.driver.get('http://www.itemmania.com/myroom/buy/buy_regist.html')

        num = self.driver.execute_script('return document.getElementsByClassName("regist_result f_green2")[0].innerHTML')
        num = num[:-1]
        num = math.ceil(int(num)/10)

        update_list = {}

        # 재등록 목록 서버별로 수집
        for n in range(1, num + 1) :
            self.driver.get('http://www.itemmania.com/myroom/buy/buy_regist.html?page=' + str(n))
            self.driver.implicitly_wait(3)
            table = self.driver.find_element(By.XPATH, '//table[@class="g_green_table tb_list"]')
            elem = table.find_elements(By.XPATH, '(//tr[position()>1])')

            for e in elem:
                server = e.find_element_by_tag_name("td").text.split('\n')[-1]
                value = e.find_element_by_tag_name("input").get_attribute('value')
                if update_list.get(server) == None:
                    update_list[server] = []
                update_list[server].append(value)
        
        max = -1 # 정렬하여 오래된 것부터 재등록 수행
        for k in update_list.keys():
                update_list[k].sort()
                max = len(update_list[k]) > max and len(update_list[k]) or max

        for i in range(max):
            first = datetime.datetime.now()
            for k in update_list.keys():
                try:
                    self.driver.execute_script('reInsert("' + update_list[k][i] + '")')
                    Alert(self.driver).accept()
                    sleep(1)
                    Alert(self.driver).accept()
                    sleep(3)
                except IndexError:
                    pass
                except Exception: # 팝업 오류
                    self.driver.get('http://www.itemmania.com/myroom/buy/buy_regist.html')
                    self.driver.implicitly_wait(3)
                    self.popup()
                    print('오류.. refresh')
                    pass

            end = datetime.datetime.now()
            
            self.wait_delay(first, end)

        pass

    def wait_delay(self, first, end) : # 재등록 딜레이 대기
        wait = (end-first).seconds
        if wait < 20 :
            sleep(20 - wait)
        pass


if __name__ == '__main__':

    title = "제목입력하세요"
    description = "글 내용 입력하세요 줄바꿈하려면 \\n"

    # 최소구매액, 최대구매액, 제목, 내용, 등록개수
    wi = WriteInfo('2', '300', title, description, '8')


    id = ['아이디1', '아이디2']
    pw = ['비밀번호1', '비밀번호2']

    for i in range(2) :
        im = Itemmania(id[i], pw[i], wi)
        im.login()
        im.update()


    # 재등록은 아래 방식

    """

    # 서버, 가격, 캐릭터명 추가
    im.add_list('서버명', '가격', '캐릭터명')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    im.add_list('', '', '')
    
    im.write_buy() # 글 작성 시작
    
    """
    
    
    
