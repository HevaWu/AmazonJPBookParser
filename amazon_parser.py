from Amazon_Single_Book_Parser import Amazon_Single_Book_Parser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import pymongo
import json
import time

# options = webdriver.ChromeOptions()
# options.add_argument('--incognito')
# options.add_argument('--headless')
# options.add_argument('--disable-extensions')
# options.add_argument('start-maximized')
# options.add_argument('disable-infobars')

cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
driver = webdriver.Firefox(capabilities=cap, executable_path='/usr/local/bin/geckodriver')

def main():
    bookList = [
        {'ISBN-13': '9784488028022', 'link': 'https://www.amazon.co.jp/gp/product/4488028020/ref=s9_acss_bw_cg_honya01_1a1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784591160022', 'link': 'https://www.amazon.co.jp/gp/product/4591160025/ref=s9_acss_bw_cg_honya01_3a1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784065137598', 'link': 'https://www.amazon.co.jp/gp/product/4065137594/ref=s9_acss_bw_cg_honya01_5a1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784104654024', 'link': 'https://www.amazon.co.jp/gp/product/4104654027/ref=s9_acss_bw_cg_honya01_5b1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784163910413', 'link': 'https://www.amazon.co.jp/gp/product/4163910417/ref=s9_acss_bw_cg_honya01_5c1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784065170946', 'link': 'https://www.amazon.co.jp/gp/product/406517094X/ref=s9_acss_bw_cg_honya01_5d1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784163910543', 'link': 'https://www.amazon.co.jp/gp/product/4163910549/ref=s9_acss_bw_cg_honya01_6a1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784575242089', 'link': 'https://www.amazon.co.jp/%E3%83%A0%E3%82%B2%E3%83%B3%E3%81%AEi-%E4%B8%8A-%E7%9F%A5%E5%BF%B5-%E5%AE%9F%E5%B8%8C%E4%BA%BA/dp/457524208X/ref=sr_1_2?dchild=1&m=AN1VRQENFRJN5&pf_rd_i=3421457051&pf_rd_m=A3P5ROKL5A1OLE&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1594259054&s=books&sr=1-2'},
        {'ISBN-13': '9784758413398', 'link': 'https://www.amazon.co.jp/gp/product/4758413398/ref=s9_acss_bw_cg_honya01_6c1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'},
        {'ISBN-13': '9784575241662', 'link': 'https://www.amazon.co.jp/gp/product/4575241660/ref=s9_acss_bw_cg_honya01_6d1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-4&pf_rd_r=MFFVP4F6VK6DGGCHJCZB&pf_rd_t=101&pf_rd_p=998c432c-5da6-405e-97ce-80a4c40be067&pf_rd_i=3421457051'}
    ]

    index = 1
    while index < 3:
        _similarList = []
        for book in bookList:
            print(book['ISBN-13'])
            try:
                id = book['ISBN-13']
                with open(f'./books/{id}.json', 'r', encoding='utf8') as f:
                    data = json.load(f)
                bookList.extend(data["similarBookList"])
                continue
            except Exception as e:
                print("* Start parsing: ", book)
                singleParser = Amazon_Single_Book_Parser(book)
                _bookId, _similarBookList = singleParser.parse(driver)
                time.sleep(10)
                singleParser.writeBookInfoIntoFile(_bookId)
                print("* Parsing finished.", _bookId)
                _save_to_mongoDB(_bookId)
                bookList.extend(_similarBookList)
        print("===================")
        print("Book List", bookList)
        index += 1

def save_to_mongoDB(idList):
    for id in idList:
        _save_to_mongoDB(id)

def _save_to_mongoDB(id):
    print("** Start Saving: ", id)
    myclient = pymongo.MongoClient("mongodb://10.231.184.114:27017/")
    mydb = myclient["book"]
    mycol = mydb["book"]

    myquery = { "_id": id }

    try:
        with open(f'./books/{id}.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    except Exception as e:
        print("Saving Failed: ", e)
        return

    _newValues = {
         "_id": data["ISBN-13"],
         "title": data["title"],
         "publisher": data["publisher"],
         "writer": data["writer"],
         "editorialReviews": data["editorialReviews"],
         "ISBN-10": data["ISBN-10"],
         "category": data["category"],
         "rate": data["rate"],
         "reviewedPerson": data["reviewedPerson"],
         "similarBookList": data["similarBookList"],
         "tags": data["tags"],
         "author_intro": data["author-intro"]
        }

    try:
        mycol.insert_one(_newValues)
    except Exception as e:
        newValues = { "$set": _newValues }
        mycol.update_one(myquery, newValues)
    print("** Finish Saving: ", id)

if __name__ == "__main__":
    # save_to_mongoDB(["9784758413398"])
    main()