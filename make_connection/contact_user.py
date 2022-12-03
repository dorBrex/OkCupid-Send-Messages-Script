import random
from utils.utils import THREE_SECONDS, TEN_USERS, By, THIRTY
from utils.personal_info import OPENING_LINE
from data_extractor.data_collector import UserInfo
from main_logic.main_okcupid_logics import ScrapeOkCupidApp
from .config_reader import conf


class ReachOutToUser:

    def __init__(self, driver):
        self.driver = driver
        self.user_info = UserInfo(self.driver)
        self.main_logic = ScrapeOkCupidApp(self.driver)

    def send_messages(self, number_of_users_to_contact: int = TEN_USERS, message: list = OPENING_LINE):
        for _ in range(number_of_users_to_contact):
            try:
                self._close_conversation_box_covering_screen()
                self._choose_user_from_queue()

                current_user_parameters = self.user_info.collect_user_info()
                self.user_info.print_identity_parameters(current_user_parameters)

                if self._repeating_the_same_user(current_user_parameters):
                    print("-" * THIRTY, "\nEXIT SCRIPT")
                    return

                self._open_messaging_box()
                if self._is_inbox_full():
                    self._pass_user()
                    continue

                self._write_line(message)
                self._send_message()

                # It's possible to save users parameters over here on local folder for later-on "processing" you stocker

            except Exception as e:
                print(e)
                self.main_logic.navigate_to_liked_users_webpage()
                self._close_conversation_box_covering_screen()
                continue

            # Return to the main page of users you already liked
            self.main_logic.navigate_to_liked_users_webpage()

        print("-" * THIRTY, "\nFinished running the script")
        [print(f"{count}. {user}") for count, user in enumerate(self.user_info.all_targets)]

        print("-" * THIRTY, "\nFinished running the script")

    def _choose_user_from_queue(self):
        # Choose the first user from the queue (the last one you liked on the application)
        choose_entity = self.driver.find_element(by=By.CLASS_NAME, value=conf['choose_from_queue'])
        choose_entity.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _open_messaging_box(self):
        # Open message box of specific user
        message_box = self.driver.find_element(by=By.XPATH, value=conf['message_box'])
        message_box.click()
        self.driver.implicitly_wait(THREE_SECONDS)

    def _is_inbox_full(self):
        try:
            inbox_is_full = self.driver.find_element(by=By.CLASS_NAME, value=conf['inbox_is_full'])
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
        self._close_conversation_box_covering_screen()
        delete_liked_user = self.driver.find_element(by=By.XPATH, value=conf['delete_liked_user'])
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

    # TODO: BUGFIX THIS SHIT - SUCCEED TO CLOSE CONVERSATION BOXES OF - FULL INBOX
    def _close_conversation_box_covering_screen(self):
        try:
            last_user_talk_to_pop_up_messenger = self.driver.find_element(
                by=By.XPATH, value=conf['close_open_conversation'])
            last_user_talk_to_pop_up_messenger.click()
        # closed the chat and now can go on
        except Exception as e:
            pass
        try:
            last_user_talk_to_pop_up_messenger = self.driver.find_element(
                by=By.XPATH, value=conf['close_finished_conversation'])
            last_user_talk_to_pop_up_messenger.click()
        except Exception as e:
            pass

        try:
            close_conversation_with_full_inbox = self.driver.find_element(by=By.XPATH,
                                                                          value=conf[
                                                                              'close_conversation_with_full_inbox'])
            close_conversation_with_full_inbox.click()
        except Exception as e:
            pass

        try:
            full_messager = self.driver.find_element(By.CLASS_NAME, value=conf['full_messager'])
            full_messager.click()
        except Exception as e:
            pass

        try:
            close_again = self.driver.find_element(By.CLASS_NAME, value=conf['close_again'])
            close_again.click()
        except Exception as e:
            pass

    def _repeating_the_same_user(self, current_user_params: dict):
        if not self.user_info.last_user['name']:
            self.user_info.last_user['name'] = current_user_params['name']
            return False
        if self.user_info.last_user['name'] == current_user_params['name'] and \
                self.user_info.last_user['age'] == current_user_params['age'] \
                and self.user_info.last_user['location'] == current_user_params['location']:

            self.user_info.same_user_counter += 1
            if self.user_info.same_user_counter >= 3:
                print(f"\nYOU TRIED TO CONTACT {current_user_params} MORE THAN 3 TIMES ALREADY !\n "
                      f"Exiting the script in order to not get stuck in the same endless loop of actions")
                return True
        else:
            self.user_info.last_user['name'], self.user_info.last_user['age'], self.user_info.last_user['location'] = \
                current_user_params['name'], current_user_params['age'], current_user_params['location']
        return False

    def _choose_next_user_from_queue(self):
        next_user = self.driver.find_element(by=By.XPATH, value=conf['next_user'])
        next_user.click()
