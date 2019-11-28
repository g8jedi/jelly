from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

import time


class TestSignupPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver')

    def tearDown(self):
        self.browser.close()

    def test_signup_page(self):
        self.browser.get(self.live_server_url)
        time.sleep(20)