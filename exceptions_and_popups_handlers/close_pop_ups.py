from selenium.webdriver.common.by import By


class ClosePopUps:
    def __init__(self, driver):
        self.driver = driver

    def close_cookies_tracking_permission_window(self):
        try:
            personalize_my_choices = self.driver.find_element(By.ID, 'onetrust-pc-btn-handler')
            personalize_my_choices.click()
            reject_all = self.driver.find_element(by=By.CLASS_NAME, value='ot-pc-refuse-all-handler')
            reject_all.click()
        except Exception as e:
            print(e, "-" * 30, "\nAlready closed the cookies tab once before\n\n")

    # TODO: Create the relevant function to handle this kind of pop-ups windows
    def close_app_offers_windows(self):
        pass
