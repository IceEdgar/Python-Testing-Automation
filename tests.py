import requests
from testpage import OperationHelper
import pytest
import logging
import yaml
import time
from checkers import checkout

with open("testdata.yaml", encoding='utf-8') as f:
    testdata = yaml.safe_load(f)
name = testdata.get("login")
pswd = testdata.get("password")
title = testdata.get("title")
description = testdata.get("description")
content = testdata.get("content")
user = testdata.get("username")
email = testdata.get("user_email")
contact = testdata.get("content_contact")
addr_post = testdata.get("address_post")
url_post = testdata.get("url_post")
url_user = testdata.get("url_user")
not_me_title = testdata.get("not_me_title")


S = requests.Session()


def test_step1(browsser):
    logging.info("Test1 Starting")
    testpage = OperationHelper(browsser)
    testpage.go_to_site()
    testpage.enter_login("test")
    testpage.enter_pass("test")
    testpage.click_login_button()
    assert testpage.get_error_text() == "401", "Test FAILED!"


def test_step2(browsser):
    logging.info("Test2 Starting")
    testpage = OperationHelper(browsser)
    testpage.go_to_site()
    testpage.enter_login(name)
    testpage.enter_pass(pswd)
    testpage.click_login_button()
    assert testpage.get_user_text() == f"Hello, {name}", "Test FAILED!"


def test_step3(browsser):
    logging.info("Test3 Stsrting")
    testpage = OperationHelper(browsser)
    testpage.click_about_btn()
    time.sleep(3)
    assert testpage.get_about_text() == "About Page", "Test FAILED!"


def test_step4(browsser):
    logging.info("Test4 Stsrting")
    testpage = OperationHelper(browsser)
    testpage.click_about_btn()
    time.sleep(2)
    assert testpage.get_font_size() == "32px", "Test FAILED!"


def test_step5(browsser):
    logging.info("Test5 Stsrting")
    testpage = OperationHelper(browsser)
    testpage.click_home_btn()
    time.sleep(2)
    testpage.click_new_post_btn()
    testpage.enter_title(title)
    testpage.enter_description(description)
    testpage.enter_content(content)
    testpage.click_save_btn()
    time.sleep(2)
    assert testpage.get_res_text() == title, "Test FAILED!"


def test_step6(browsser):
    logging.info("Test6 Contact_us Starting")
    testpage = OperationHelper(browsser)
    testpage.click_contact_link()
    testpage.enter_contact_name(user)
    testpage.enter_contact_email(email)
    testpage.enter_contact_content(contact)
    testpage.click_contact_send_btn()
    assert testpage.get_allert_message() == "Form successfully submitted", "Test FAILED!"


def test_step88(login):
    logging.info("Test8 create post started")
    res = S.get(url=url_user, headers={'X-Auth-Token': login}).json()
    assert res['username'] == testdata['login']


def test_step7(login):
    logging.info("Test7 check not me post started")
    res = S.get(url=url_post, headers={'X-Auth-Token': login}, params={'owner': 'notMe'}).json()['data']
    logging.debug(f"get request return: {res}")
    result_title = [i['title'] for i in res]
    assert not_me_title in result_title, 'Пост с заданным заголовком не найден'
    

def test_step8(login):
    logging.info("Test8 create post started")
    url = addr_post
    headers = {'X-Auth-Token': login}
    d = {'title': title, 'description': description, 'content': content}
    res = S.post(url, headers=headers, data=d)
    logging.debug(f"Response is {str(res)}")
    assert str(res) == '<Response [200]>', "Новый пост не создан"


def test_step9(login, get_description):
    logging.info("Test9 check description started")
    url = url_post
    headers = {'X-Auth-Token': login}
    data_json = S.get(url=url, headers=headers).json()['data']
    logging.debug(f"get request return: {data_json}")
    res = [i['description'] for i in data_json]
    assert get_description in res, 'test_step7 FAIL'


def test_send_email(email_sender):
    assert email_sender['To'] == 'sorata05@mail.ru'
    

def test_vulnerability():
    result = checkout('nikto -h https://test-stand.gb.ru/ -ssl -Tuning 4', '0 error(s)')
    assert result


if __name__ == "__main__":
    pytest.main(["-vv"])