from urllib import request
import re
from typing import Union
from utils.utils import generate_id, By


class UserInfo:
    def __init__(self, driver):
        self.driver = driver
        self.name = ''
        self.age = ''
        self.location = ''
        self.all_targets = []
        self.last_user = {'name': '', 'age': '', 'location': ''}
        self.self_summary = ''
        self.extracted_instagram_username = ''
        self.same_user_counter = 0

    def collect_user_info(self):
        self.name = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-username-text').text
        self.age = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-asl-age').text
        self.location = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-asl-location').text
        self.self_summary = self.driver.find_element(by=By.CLASS_NAME, value='profile-essay-contents').text
        self.extracted_instagram_username = self._extract_instagram(self.self_summary)
        user_data = [self.name, self.age, self.location, self.self_summary, self.extracted_instagram_username]
        self.all_targets.append(user_data)
        user_data = {'name': self.name, 'age': self.age, 'location': self.location, 'self_summary': self.self_summary,
                     'instagram': self.extracted_instagram_username}
        return user_data

    @staticmethod
    def print_identity_parameters(user_parameters):
        print(
            f"NAME: {user_parameters['name']};\n"
            f"AGE: {user_parameters['age']};\n"
            f"LOCATION: {user_parameters['location']};\n"
        )

    @staticmethod
    def _extract_instagram(about_me_text_box) -> Union[str, None]:
        text = about_me_text_box.lower()
        instagram_mentions = ['ig', 'instagram']
        for i in instagram_mentions:
            if i in text:
                print("-" * 30, "The user has mentioned its instagram user:")
                possible_instagram = text.split(i)[1].split(' ')
                if len(possible_instagram[0]) < 5:
                    user_instagram = possible_instagram[1]
                else:
                    user_instagram = possible_instagram[0]
                user_instagram = user_instagram.strip()
                ig_result = re.sub('[-:=]', '', user_instagram)
                return ig_result.strip()
        return None

    # self.last_user = {'name': '', 'age': 0, 'location': ''}

    def _save_users_profile_picture(self):
        profile_image_xpath = self.driver.find_element(by=By.XPATH, value=
        '//*[@id="main_content"]/div[3]/div/div/div[1]/div/img[1]')
        name = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-username-text')
        age = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-asl-age')
        location = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-asl-location')
        generate_random_id = generate_id()
        downloaded_image = profile_image_xpath.get_attribute('src')

        # Saves the picture locally in the project's folder
        request.urlretrieve(downloaded_image, f"{name}{generate_random_id}.jpeg")
        print("Finished copying user's data")

    def _take_screenshot(self):
        users_name = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-username-text')
        generated_id = generate_id()
        self.driver.save_screenshot(f"{users_name}_screenshot_{generated_id}.png")
