import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.personal_info import CACHE_FOLDER
from utils.utils import THREE_SECONDS, WHO_YOU_LIKED_PAGE


class ScrapeOkCupidApp:
    def __init__(self, initialized_driver=None):
        options = Options()
        # "--user-data-dir=C:\\Users\\user_name\\Desktop\\UserData" - an empty folder to be used for caching the scrape_okcupid
        #  takes about 100 mb of storage
        options.add_argument(CACHE_FOLDER)
        options.add_argument("--start-maximized")
        options.page_load_strategy = 'normal'
        self.driver = initialized_driver if initialized_driver else webdriver.Chrome(options=options)

    def open_application(self):
        # Requests the specific site
        # self.driver.get(LOGIN_PAGE)
        self.driver.get('https://www.okcupid.com/home')
        # Let the site load
        self.driver.implicitly_wait(THREE_SECONDS)

    def navigate_to_liked_users_webpage(self):
        self.driver.get(WHO_YOU_LIKED_PAGE)
        time.sleep(THREE_SECONDS)
        # self.driver.fullscreen_window()

    def shared_drive(self):
        return self.driver

