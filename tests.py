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


class TestUI:

    def test_check_error_messages(self, browsser):
        logging.info("Check Error messages started")
        testpage = OperationHelper(browsser)
        testpage.go_to_site()
        testpage.enter_login("test")
        testpage.enter_pass("test")
        testpage.click_login_button()
        assert testpage.get_error_text() == "401", "Test FAILED!"

    def test_check_login(self, browsser):
        logging.info("Check login started")
        testpage = OperationHelper(browsser)
        testpage.go_to_site()
        testpage.enter_login(name)
        testpage.enter_pass(pswd)
        testpage.click_login_button()
        assert testpage.get_user_text() == f"Hello, {name}", "Test FAILED!"

    def test_check_about_page(self, browsser):
        logging.info("Check About page started")
        testpage = OperationHelper(browsser)
        testpage.click_about_btn()
        time.sleep(3)
        assert testpage.get_about_text() == "About Page", "Test FAILED!"

    def test_check_header_font(self, browsser):
        logging.info("Check header font started")
        testpage = OperationHelper(browsser)
        testpage.click_about_btn()
        time.sleep(2)
        assert testpage.get_font_size() == "32px", "Test FAILED!"

    def test_create_new_post(self, browsser):
        logging.info("Create new post started")
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

    def test_step_check_contact_us(self, browsser):
        logging.info("Check Contact us started")
        testpage = OperationHelper(browsser)
        testpage.click_contact_link()
        testpage.enter_contact_name(user)
        testpage.enter_contact_email(email)
        testpage.enter_contact_content(contact)
        testpage.click_contact_send_btn()
        assert testpage.get_allert_message() == "Form successfully submitted", "Test FAILED!"


class TestAPI:

    def test_check_username(self, login):
        logging.info("Check username started")
        res = S.get(url=url_user, headers={'X-Auth-Token': login}).json()
        assert res['username'] == testdata['login']

    def test_check_not_my_post(self, login):
        logging.info("Check not my post started")
        res = S.get(url=url_post, headers={'X-Auth-Token': login}, params={'owner': 'notMe'}).json()['data']
        logging.debug(f"get request return: {res}")
        result_title = [i['title'] for i in res]
        assert not_me_title in result_title, 'Пост с заданным заголовком не найден'

    def test_create_post(self, login):
        logging.info("Create post started")
        url = addr_post
        headers = {'X-Auth-Token': login}
        d = {'title': title, 'description': description, 'content': content}
        res = S.post(url, headers=headers, data=d)
        logging.debug(f"Response is {str(res)}")
        assert str(res) == '<Response [200]>', "Новый пост не создан"

    def test_check_description(self, login, get_description):
        logging.info("Check description started")
        url = url_post
        headers = {'X-Auth-Token': login}
        data_json = S.get(url=url, headers=headers).json()['data']
        logging.debug(f"get request return: {data_json}")
        res = [i['description'] for i in data_json]
        assert get_description in res, 'test_step7 FAIL'

    def test_vulnerability_check(self):
        logging.info("Vulnerability check started")
        result = checkout('nikto -h https://test-stand.gb.ru/ -ssl -Tuning 4', '0 error(s)')
        assert result

    def test_send_email(self, email_sender):
        assert email_sender['To'] == 'sorata05@mail.ru'

    if __name__ == "__main__":
        pytest.main(["-vv"])