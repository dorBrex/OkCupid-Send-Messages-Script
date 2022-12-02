import random
from utils.utils import THREE_SECONDS, TEN_USERS, By
from utils.personal_info import OPENING_LINE
from data_extractor.data_collector import UserInfo
from scrape_okcupid.main_okcupid_logics import ScrapeOkCupidApp
from .config_reader import config


class ContactUser:

    def __init__(self, driver):
        self.driver = driver
        self.user_info = UserInfo(self.driver)
        self.main_logic = ScrapeOkCupidApp(self.driver)

    def send_messages_logic(self, number_of_users_to_contact: int = TEN_USERS, message: list = OPENING_LINE):
        last_user_checked: str = ''
        self.close_conversation_box_covering_screen()
        for _ in range(number_of_users_to_contact):
            try:
                self.close_conversation_box_covering_screen()
                self._choose_user_from_queue()
                # try:
                # Last_user_checked = self.driver.find_element_by_class_name
                # ('zHDa90dJPT_1Hh4peCYg profile-content-blank profile-content-blank--wide')
                current_user_parameters = self.user_info.collect_user_info()
                self.user_info.print_identity_parameters(current_user_parameters)

                if self.repeating_the_same_user(current_user_parameters['name']):
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
                self.main_logic.navigate_to_liked_users_webpage()
                self.close_conversation_box_covering_screen()
                continue

            # Return to the main page of users you already liked
            self.main_logic.navigate_to_liked_users_webpage()
        print("-" * 30, "\nFinished running the script")
        [print(f"{count}. {user}") for count, user in enumerate(self.user_info.all_targets)]

        print("-" * 30, "\nFinished running the script")

    def _choose_user_from_queue(self):
        # Choose the first user in queue (the last one you liked on the application)
        choose_entity = self.driver.find_element(by=By.CLASS_NAME, value=config['choose_from_queue'])
        choose_entity.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _open_messaging_box(self):
        # Open message box of specific user
        message_box = self.driver.find_element(by=By.XPATH, value=config['message_box'])
        message_box.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _is_inbox_full(self):
        try:
            inbox_is_full = self.driver.find_element(by=By.CLASS_NAME, value=config['inbox_is_full'])
        except Exception as e:
            print(e)
            inbox_is_full = self.driver.find_element(by=By.CLASS_NAME, value='messenger-banner') \
                            or self.driver.find_element(by=By.CLASS_NAME, value='messenger-composer')

        if "has a full inbox" in inbox_is_full.text:
            users_name = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-username-text')
            print(f"{users_name.text}'s inbox is full, you cannot send her/him any more messages.")
            return True

    def _pass_user(self):
        print(f"\nThe script is deleting this user from the liked_users collection.")
        self.close_conversation_box_covering_screen()
        delete_liked_user = self.driver.find_element(by=By.XPATH, value=config['delete_liked_user'])
        delete_liked_user.click()

    def _write_line(self, message: list[str]):
        #  Write an opening line to start the chat
        introduce_yourself = self.driver.find_element(by=By.CLASS_NAME, value='BxLIffwavFC1udtULr_8')
        introduce_yourself.send_keys(random.choice(message))
        self.driver.implicitly_wait(THREE_SECONDS)

    def _send_message(self):
        send_hello = self.driver.find_element(by=By.CLASS_NAME, value='pnbgZN7izvYY_0kDp1Rk')
        send_hello.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def close_conversation_box_covering_screen(self):
        try:
            last_user_talk_to_pop_up_messenger = self.driver.find_element(
                by=By.XPATH, value=config['close_open_conversation'])
            last_user_talk_to_pop_up_messenger.click()
            # closed the chat and now can go on
        except Exception as e:
            last_user_talk_to_pop_up_messenger = self.driver.find_element(
                by=By.XPATH, value=config['close_finished_conversation'])
            last_user_talk_to_pop_up_messenger.click()

    def repeating_the_same_user(self, current_user):
        if not self.user_info.last_user:
            self.user_info.last_user = current_user
            return False
        if self.user_info.last_user == current_user:
            self.user_info.same_user_counter += 1
            if self.user_info.same_user_counter >= 3:
                print(f"\nYOU TRIED TO CONTACT {current_user} MORE THAN 3 TIMES ALREADY !\n exiting the script")
                return True
        else:
            self.user_info.last_user = current_user
        return False

    def _choose_next_user_from_queue(self):
        next_user = self.driver.find_element(by=By.XPATH, value=config['next_user'])
        next_user.click()
