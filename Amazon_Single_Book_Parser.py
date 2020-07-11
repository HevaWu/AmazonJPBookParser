from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json

class Amazon_Single_Book_Parser(object):
    def __init__(self, book):
        super().__init__()
        self.link = book['link']
        self.bookInfo = {}

    def parse(self, driver):
        try:
            self._parse(driver)
            return self.bookInfo["id"], self.bookInfo["similarBookList"]
        except Exception as e:
            print("Parsing Book Failed: ", self.link, e)

    def _parse(self, driver):
        driver.get(self.link)
        time.sleep(3)
        # html_page = self.driver.page_source
        # items = BeautifulSoup(html_page, 'html.parser')

        self.bookInfo["title"] = self._parseTitle(driver)
        self.bookInfo["editorialReviews"] = self._parseEditorialReviews(driver)
        self.bookInfo["ISBN-10"] = self._parseISBN10(driver)
        self.bookInfo["ISBN-13"] = self._parseISBN13(driver)
        self.bookInfo["category"] = self._parseCategory(driver)
        self.bookInfo["author-intro"] = self._parseAuthorIntro(driver)
        self.bookInfo["rate"] = self._parseRate(driver)
        self.bookInfo["reviewedPerson"] = self._parseReviewedPerson(driver)
        self.bookInfo["publisher"] = self._parsePublisher(driver)
        self.bookInfo["writer"] = self._parseWriter(driver)
        self.bookInfo["id"] = self.bookInfo["ISBN-13"]
        self.bookInfo["tags"] = self._parseTags(driver)
        self.bookInfo["similarBookList"] = self._parseSimilarBookList(driver)

    def _parseTitle(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="title"]').text
        except Exception as e:
            print("Parsing Book Title Failed: ", self.link, e)
            return ""

    def _parseISBN10(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li[4]').text.split(':', 1)[1].strip()
        except Exception as e:
            print("Parsing Book ISBN-10 Failed: ", self.link, e)
            return ""

    def _parseISBN13(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li[5]').text.split(':', 1)[1].strip().replace('-', '')
        except Exception as e:
            print("Parsing Book ISBN-13 Failed: ", self.link, e)
            return ""

    def _parseCategory(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="SalesRank"]/ul/li/span[2]/a').text
        except Exception as e:
            print("Parsing Book Category Failed: ", self.link, e)
            return ""

    def _parseRate(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span').text.split('の', 1)[1]
        except Exception as e:
            print("Parsing Book Rate Failed: ", self.link, e)
            return ""

    def _parseReviewedPerson(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span').text.split(' ', 1)[1]
        except Exception as e:
            print("Parsing Book ReviewedPerson Failed: ", self.link, e)
            return ""

    def _parsePublisher(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li[2]').text.split(':', 1)[1].strip().split('(', 1)[0].strip()
        except Exception as e:
            print("Parsing Book Publisher Failed: ", self.link, e)
            return ""

    def _parseTags(self, driver):
        try:
            tags = []
            _tags = driver.find_elements_by_class_name('cr-lighthouse-term')
            for _tag in _tags:
                tag = _tag.text
                if tag != '':
                    tags.append(tag)
            return tags
        except Exception as e:
            print("Parsing Book Tags Failed: ", self.link, e)
            return []

    def _parseAuthorIntro(self, driver):
        try:
            ele = driver.find_element_by_xpath('//*[@id="editorialReviews_feature_div"]/div[2]/div/div[2]')
            return ele.text
        except Exception as e:
            try:
                ele = driver.find_element_by_xpath('//*[@id="editorialReviews_feature_div"]/div[2]/div[2]')
                return ele.text
            except Exception as e:
                print("Parsing Book AuthorInfo Failed: ", self.link, e)
                return ""

    def _parseEditorialReviews(self, driver):
        try:
            ele = driver.find_element_by_xpath('//*[@id="editorialReviews_feature_div"]/div[2]/div/div[1]')
            return ele.text
        except Exception as e:
            try:
                ele = driver.find_element_by_xpath('//*[@id="editorialReviews_feature_div"]/div[2]/div[1]')
                return ele.text
            except Exception as e:
                print("Parsing Book EditorialReviews Failed: ", self.link, e)
                return ""

    def _parseWriter(self, driver):
        try:
            return driver.find_element_by_xpath('//*[@id="bylineInfo"]/span/span[1]/a[1]').text.replace(' ', '')
        except Exception as e:
            try:
                return driver.find_element_by_xpath('//*[@id="bylineInfo"]/span/a').text.replace(' ', '')
            except Exception as e:
                print("Parsing Book Writer Failed: ", self.link, e)
                return ""

    def _parseSimilarBookList(self, driver):
        _similarBooklink = set()
        _failIndex = 0
        while True:
            time.sleep(3)
            try:
                _similarBookList = []
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#desktop-dp-sims_ReadingSimilarities-sims-feature li')))
                _similarBookList = driver.find_elements_by_css_selector('#desktop-dp-sims_ReadingSimilarities-sims-feature li')
                isReaded = False
                print(_similarBookList)
                _currentPageBookLink = set()
                for _book in _similarBookList:
                    time.sleep(1)
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-section.a-spacing-none.p13n-asin a')))
                    link = _book.find_element_by_css_selector('.a-section.a-spacing-none.p13n-asin a').get_attribute('href')
                    if link in _similarBooklink:
                        isReaded = True
                        break
                    _currentPageBookLink.add(link)
                if isReaded:
                    break
                _similarBooklink.update(_currentPageBookLink)
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, 1400);")

                headereElement = driver.find_element_by_xpath('//*[@id="a-autoid-12"]')
                actions = ActionChains(driver)
                actions.move_to_element(headereElement).perform()
                next_btn = driver.find_element_by_xpath('//*[@id="a-autoid-12"]')
                next_btn.click()
                print("==============")
            except Exception as e:
                print("Parsing Book Similar Book Failed: ", self.link, e)
                if _failIndex < 1:
                    driver.get(self.link)
                    _failIndex += 1
                else:
                    break

        return self._parseCurrentPageSimilarBookList(driver, _similarBooklink)

    def _parseCurrentPageSimilarBookList(self, driver,currentPageBookLink):
        try:
            print("=== Start Parsing Page Similar Book List", currentPageBookLink)
            similarBookList = []
            for link in currentPageBookLink:
                book = {}
                time.sleep(2)
                driver.get(link)
                book["ISBN-13"] = driver.find_element_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li[5]').text.split(':', 1)[1].strip().replace('-', '')
                book["link"] = link
                similarBookList.append(book)
            return similarBookList
        except Exception as e:
            print("Parsing Book Similar Book List Failed: ", self.link, e)
            return []

    def writeBookInfoIntoFile(self, _bookId):
        with open(f'./books/{_bookId}.json', 'w', encoding='utf8') as f:
            json.dump(self.bookInfo, f, ensure_ascii=False)

    def getSimilarBookList(self, bookList):
        _similarBookList = []
        for book in bookList:
            _similarBookList.append(book["link"])
        return _similarBookList
