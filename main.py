import random
import time
from urllib import request

from selenium import webdriver

from personal_info import username, passwd, opening_lines, DEFAULT_LINES


class ScrapeOkCupidApp:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def exception_handling(self):
        self.driver.get('https://www.okcupid.com/who-you-like?cf=likesIncoming')

    def enter_application(self):
        # Requests the specific site
        self.driver.get("https://www.okcupid.com/login/")
        # Let Instagram site load
        self.driver.implicitly_wait(4)

    def login(self):
        email = self.driver.find_element_by_id('username')
        email.send_keys(username)
        self.driver.implicitly_wait(2)

        password = self.driver.find_element_by_id('password')
        password.send_keys(passwd)
        self.driver.implicitly_wait(2)

        login_button = self.driver.find_element_by_class_name('login-actions-button')
        login_button.click()
        self.driver.implicitly_wait(8)
        # Wait enough for the script-runner to enter the code from the smartphone's message
        time.sleep(20)

    def navigate_to_liked_users_webpage(self):
        self.driver.get('https://www.okcupid.com/who-you-like?cf=likesIncoming')
        time.sleep(5)

    def reject_cookies(self):
        personalize_my_choices = self.driver.find_element_by_id('onetrust-pc-btn-handler')
        personalize_my_choices.click()
        reject_all = self.driver.find_element_by_class_name('ot-pc-refuse-all-handler')
        reject_all.click()

    def send_entrance(self, number_of_entities=10, opening_lines=DEFAULT_LINES):
        for _ in range(number_of_entities):
            try:
                # Choose the first user in queue (the last one you liked on the application)
                choose_entity = self.driver.find_element_by_class_name('userrow-bucket-card-link-container')
                choose_entity.click()
                self.driver.implicitly_wait(3)
                # Open message box of specific user
                message_box = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/main/div[1]/div[3]/div/div/div[3]/span/div/button[2]')
                message_box.click()
                self.driver.implicitly_wait(3)

                # Check if the user's inbox is full
                inbox_is_full = self.driver.find_element_by_class_name('messenger-banner')
                if "has a full inbox" in inbox_is_full.text:
                    users_name = self.driver.find_element_by_class_name('profile-basics-username-text')
                    print(f"{users_name.text}'s inbox is full, you cannot send her/him any more messages."
                          f"\nThe script is deleting this user from the liked_users collection.")
                    delete_liked_user = self.driver.find_element_by_xpath(
                        '/html/body/div[1]/main/div[1]/div[3]/div/div/div[3]/span/div/button[1]/div')
                    delete_liked_user.click()

                #  Write an opening line to start the chat
                introduce_yourself = self.driver.find_element_by_class_name('messenger-composer')
                introduce_yourself.send_keys(random.choice(opening_lines))
                self.driver.implicitly_wait(3)

                # Send the message you wrote to the other side
                send_hello = self.driver.find_element_by_class_name('messenger-toolbar-send')
                send_hello.click()
                self.driver.implicitly_wait(3)

                # It's possible to save users' parameters over here on local folder for later-on processing

            except Exception as e:
                print(e)
                self.exception_handling()
                continue

            # Return to the main page of 'users you already liked"
            self.driver.get('https://www.okcupid.com/who-you-like?cf=likesIncoming')
            time.sleep(2)

        print("==========================\nFinished running the script")

    def save_users_profile_picture(self):
        profile_image_xpath = self.driver.find_element_by_xpath(
            '//*[@id="main_content"]/div[3]/div/div/div[1]/div/img[1]')
        users_name = self.driver.find_element_by_class_name('profile-basics-username-text')
        generate_random_id = str(random.randint(1, 100))
        downloaded_image = profile_image_xpath.get_attribute('src')
        # Saves the picture locally in the project's folder
        request.urlretrieve(downloaded_image, f"{users_name}{generate_random_id}.jpeg")
        print("finish")

    def take_screenshot(self):
        generated_id = str(random.randint(1, 100))
        self.driver.save_screenshot(f"sreenshot{generated_id}.png")


def main():
    run_script = ScrapeOkCupidApp()
    run_script.enter_application()
    run_script.login()
    run_script.navigate_to_liked_users_webpage()
    run_script.reject_cookies()
    run_script.send_entrance(number_of_entities=40, opening_lines=opening_lines)


if __name__ == '__main__':
    main()
