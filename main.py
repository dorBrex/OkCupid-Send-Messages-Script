import random
import time
from urllib import request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from personal_info import username, passwd, DEFAULT_LINES, OPENING_LINES, CACHE_FOLDER
from utils import TEN_USERS, THREE_SECONDS, TEN_SECONDS, TWENTY_SECONDS, LOGIN_PAGE, \
    WHO_YOU_LIKED_PAGE


class ScrapeOkCupidApp:
    def __init__(self):

        options = Options()
        # "--user-data-dir=C:\\Users\\user_name\\Desktop\\UserData" - an empty folder to be used for caching the login
        #  takes about 100 mb of storage
        options.add_argument(CACHE_FOLDER)
        options.add_argument("--start-maximized")
        options.page_load_strategy = 'normal'
        self.driver = webdriver.Chrome(options=options)
        self._name = ''
        self._age = ''
        self._location = ''
        self._all_targets = []
        self.last_user = ''
        self.number_of_times_seen_this_user = 1

    def _open_default_chrome(self):
        pass

    def open_application(self):
        # Requests the specific site
        self.driver.get(LOGIN_PAGE)
        # Let the site load
        self.driver.implicitly_wait(THREE_SECONDS)

    def login(self):
        email = self.driver.find_element_by_id('username')
        email.send_keys(username)
        self.driver.implicitly_wait(THREE_SECONDS)

        password = self.driver.find_element_by_id('password')
        password.send_keys(passwd)
        self.driver.implicitly_wait(THREE_SECONDS)

        login_button = self.driver.find_element_by_class_name('login-actions-button')
        login_button.click()
        self.driver.implicitly_wait(TEN_SECONDS)

        # This is the only manual functionality in the whole script. You ask for an sms code and pass it manually.
        # Wait enough for the script-runner to enter the code from the smartphone's message
        time.sleep(TWENTY_SECONDS)

    def navigate_to_liked_users_webpage(self):
        self.driver.get(WHO_YOU_LIKED_PAGE)
        time.sleep(THREE_SECONDS)
        # self.driver.fullscreen_window()

    def close_cookies_tracking_permission_window(self):
        try:
            personalize_my_choices = self.driver.find_element_by_id('onetrust-pc-btn-handler')
            personalize_my_choices.click()
            reject_all = self.driver.find_element_by_class_name('ot-pc-refuse-all-handler')
            reject_all.click()
        except Exception as e:
            print(e, "\nAlready closed the cookies tab once before")

    # TODO: Create the relevant function to handle this kind of pop-ups windows
    def close_app_offers_windows(self):
        pass

    def send_messages_logic(self, number_of_users_to_contact: int = TEN_USERS, message: list = DEFAULT_LINES):
        last_user_checked: str = ''
        self.close_conversation_box_covering_screen()
        for _ in range(number_of_users_to_contact):
            try:
                self.close_conversation_box_covering_screen()
                self._choose_user_from_queue()
                # try:
                # Last_user_checked = self.driver.find_element_by_class_name
                # ('zHDa90dJPT_1Hh4peCYg profile-content-blank profile-content-blank--wide')
                self._print_identity_parameters()

                if self.repeating_the_same_user(self._name.text):
                    return

                self._open_messaging_box()
                if self._is_inbox_full():
                    self._pass_user()
                    continue

                self._write_line(message)
                self._send_message()

                # It's possible to save users' parameters over here on local folder for later-on processing

            except Exception as e:
                print(e)
                self._exception_handling()
                self.close_conversation_box_covering_screen()
                continue

            # Return to the main page of 'users you already liked"
            self.navigate_to_liked_users_webpage()
        print("==========================\nFinished running the script")
        [print(f"{count}. {user}") for count, user in enumerate(self._all_targets)]

        print("==========================\nFinished running the script")

    def _save_users_profile_picture(self):
        profile_image_xpath = self.driver.find_element_by_xpath(
            '//*[@id="main_content"]/div[3]/div/div/div[1]/div/img[1]')
        name = self.driver.find_element_by_class_name('profile-basics-username-text')
        age = self.driver.find_element_by_class_name('profile-basics-asl-age')
        location = self.driver.find_element_by_class_name('profile-basics-asl-location')
        generate_random_id = self._generate_id()
        downloaded_image = profile_image_xpath.get_attribute('src')

        # Saves the picture locally in the project's folder
        request.urlretrieve(downloaded_image, f"{name}{generate_random_id}.jpeg")
        print("Finished copying user's data")

    def _take_screenshot(self):
        users_name = self.driver.find_element_by_class_name('profile-basics-username-text')
        generated_id = self._generate_id()
        self.driver.save_screenshot(f"{users_name}_screenshot_{generated_id}.png")

    @staticmethod
    def _generate_id():
        #  Adding a generated number in case we get 2 users with the same name
        return str(random.randint(1, 100))

    def _choose_user_from_queue(self):
        # Choose the first user in queue (the last one you liked on the application)
        choose_entity = self.driver.find_element_by_class_name('userrow-bucket-card-link-container')
        choose_entity.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _open_messaging_box(self):
        # Open message box of specific user
        message_box = self.driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[1]/div[3]/div/div/div[3]/div/button[2]')
        message_box.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _is_inbox_full(self):
        try:
            inbox_is_full = self.driver.find_element_by_class_name('BxLIffwavFC1udtULr_8')
        except Exception as e:
            print(e)
            inbox_is_full = self.driver.find_element_by_class_name(
                'messenger-banner') or self.driver.find_element_by_class_name('messenger-composer')
        if "has a full inbox" in inbox_is_full.text:
            users_name = self.driver.find_element_by_class_name('profile-basics-username-text')
            print(f"{users_name.text}'s inbox is full, you cannot send her/him any more messages.")
            return True

    def _pass_user(self):
        print(f"\nThe script is deleting this user from the liked_users collection.")
        close_conversation = self.driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[1]/div[1]/div[2]/div/div[1]/div/button[1]')
        close_conversation.click()
        delete_liked_user = self.driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[1]/div[3]/div/div/div[3]/div/button[1]/div')
        delete_liked_user.click()

    def _write_line(self, message: list[str]):
        #  Write an opening line to start the chat
        introduce_yourself = self.driver.find_element_by_class_name('BxLIffwavFC1udtULr_8')
        introduce_yourself.send_keys(random.choice(message))
        self.driver.implicitly_wait(THREE_SECONDS)

    def _send_message(self):
        send_hello = self.driver.find_element_by_class_name('pnbgZN7izvYY_0kDp1Rk')
        send_hello.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _exception_handling(self):
        self.driver.get('https://www.okcupid.com/who-you-like?cf=likesIncoming')

    def logged_in(self):
        if self.driver.find_element_by_class_name('profile-button-details'):
            print("You are already logged in")
            return True

    def _avoid_deleted_accounts_error(self):
        if self.driver.find_element_by_class_name():
            self._choose_next_user_from_queue()

    def _choose_next_user_from_queue(self):
        next_user = self.driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[1]/div[2]/div/main/div/div/div/div[2]/div[1]/div[2]')
        next_user.click()

    def _print_identity_parameters(self):
        self._name = self.driver.find_element_by_class_name('profile-basics-username-text')
        self._age = self.driver.find_element_by_class_name('profile-basics-asl-age')
        self._location = self.driver.find_element_by_class_name('profile-basics-asl-location')
        print(f"NAME: {self._name.text};\nAGE: {self._age.text};\nLOCATION: {self._location.text};\n")
        self._all_targets.append([self._name.text, self._age.text, self._location.text])

    def close_conversation_box_covering_screen(self):
        try:
            last_user_talk_to_pop_up_messenger = self.driver.find_element_by_xpath(
                '/html/body/div[1]/main/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[1]/button/i')
            last_user_talk_to_pop_up_messenger.click()
            # closed the chat and now can go on
        except:
            pass

    def repeating_the_same_user(self, current_user):
        if not self.last_user:
            self.last_user = current_user
            return False
        if self.last_user == current_user:
            self.number_of_times_seen_this_user += 1
            if self.number_of_times_seen_this_user >= 3:
                print(f"\nYOU TRIED TO CONTACT {current_user} MORE THAN 3 TIMES ALREADY !\n exiting the script")
                return True
        else:
            self.last_user = current_user
        return False


def main():
    run_script = ScrapeOkCupidApp()
    run_script.open_application()
    time.sleep(3)
    # if not run_script.logged_in():
    #     run_script.login()
    run_script.navigate_to_liked_users_webpage()
    # run_script.close_cookies_tracking_permission_window()
    run_script.send_messages_logic(number_of_users_to_contact=50, message=OPENING_LINES)


if __name__ == '__main__':
    main()
