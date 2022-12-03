import time
from utils.utils import THREE_SECONDS, TEN_SECONDS, TWENTY_SECONDS, By, THIRTY
from utils.personal_info import username, passwd


class Login:
    def __init__(self, driver):
        self.driver = driver

    # TODO: make sure we are using the relevant web browser
    def _open_default_chrome(self):
        pass

    def login(self):
        email = self.driver.find_element(By.ID, 'username')
        email.send_keys(username)
        self.driver.implicitly_wait(THREE_SECONDS)

        password = self.driver.find_element(By.ID, 'password')
        password.send_keys(passwd)
        self.driver.implicitly_wait(THREE_SECONDS)

        login_button = self.driver.find_element(by=By.CLASS_NAME, value='main_logic-actions-button')
        login_button.click()
        self.driver.implicitly_wait(TEN_SECONDS)

        # This is the only manual functionality in the whole script. You'll be asked to insert sms code.
        # Wait enough for the script-runner to enter the code from the smartphone's message
        # time.sleep(TWENTY_SECONDS) - return this line if needed

    def logged_in(self):
        try:
            if self.driver.find_element(by=By.CLASS_NAME, value='profile-button-details'):
                print("You are already logged in")
                return True
        except Exception as e:
            print(e)
            print("-" * THIRTY, "\nCouldn't figure out if you are already loggen in - probably not!")
