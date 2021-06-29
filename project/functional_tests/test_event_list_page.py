from selenium import webdriver
from event.models import Event
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestEventListPage(StaticLiveServerTestCase):

    def setUp(self):
        # webdriver options
        options = webdriver.ChromeOptions()
        # change browser lanaguage as it defaults to Portuguese
        options.add_experimental_option(
            'prefs', {'intl.accept_languages': 'en,en_US'})

        self.browser = webdriver.Chrome(
            'functional_tests/driver.exe', chrome_options=options)

        options = webdriver.ChromeOptions()
        return super().setUp()

    def tearDown(self):
        self.browser.close()
        return super().tearDown()

    def test_there_are_no_events_to_list(self):
        self.browser.get(self.live_server_url)

        # User requests page for first time
        container = self.browser.find_element_by_class_name('col-md-8')
        self.assertEquals(
            container.find_element_by_tag_name('h2').text,
            'There are no events to display...'
        )
