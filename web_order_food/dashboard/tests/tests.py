from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User

# from dashboard.tests.utils import MockData
import configparser

config = configparser.ConfigParser()
config.read('./test.ini')
# print(config)
# def setup_driver():
#     driver_path = config.get('selenium', 'driver_path')
#     brave_path = config.get('selenium', 'brave_path')

#     option = webdriver.ChromeOptions()
#     option.binary_location = brave_path

#     browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

#     return browser

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser=User.objects.create_superuser(username='test_admin', is_superuser=True, password='123' )
        cls.superuser.save()
        cls.selenium = webdriver.Edge(config.get('selenium', 'driver_path'))
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.close()
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        from selenium.webdriver.support.wait import WebDriverWait
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_field = self.selenium.find_element_by_css_selector('form input[name="username"]')
        password_field = self.selenium.find_element_by_css_selector('form input[name="password"]')
        username_field.send_keys('test_admin')
        password_field.send_keys('123')

        submit = self.selenium.find_element_by_css_selector('form input[type="submit"]')
        submit.click()
        timeout = 5
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/dashboard/'))
        WebDriverWait(self.selenium, timeout).until(
        lambda driver: driver.find_element_by_xpath('//*[@id="user-tools"]/a[1]'))
        self.assertEqual(self.selenium.find_elements_by_xpath('//*[@id="user-tools"]/a[1]').get_text(), 'View site')
        WebDriverWait(self.selenium, timeout).until(
        lambda driver: driver.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/nav/div[1]/a/span'))
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/nav/div[1]/a/span').get_text(), 'Báo cáo')