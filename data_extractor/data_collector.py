import io
import os
import re
import time
from urllib import request
from typing import Union

from data_extractor.ig_processor import process_ig_words, remove_emojis
from utils.utils import generate_id, By, THIRTY
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PIL import Image as Image


def special_women_needs(filters):
    def find_filters(original_function):
        def search(*args, **kwargs):
            summary_text = list(args)[1]
            split_text = summary_text.split()
            res = any([True for word in split_text if word in filters])
            return res
        return search
    return find_filters


class OkCupidUser:
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

    @special_women_needs(['דתייה', 'דת', 'בורא', 'אבא', 'שבת', 'דתיה', 'שומרת', 'עולם'])
    def _find_god(self, self_summary):
        pass

    @special_women_needs(['בעלי', 'החבר', 'משחקים', 's+1', 'd+1'])
    def _zahla_or_fakaza_detector(self, self_summary):
        pass

    def collect_user_info(self):
        self.name = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-username-text').text
        self.age = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-asl-age').text
        self.location = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-asl-location').text
        self.self_summary = self.driver.find_element(by=By.CLASS_NAME, value='profile-essay-contents').text
        if self._find_god(self.self_summary) or self._zahla_or_fakaza_detector(self.self_summary):
            return None

        self.extracted_instagram_username = self._extract_instagram(self.self_summary)

        user_data = [self.name, self.age, self.location, self.self_summary, self.extracted_instagram_username]
        self.all_targets.append(user_data)
        user_data = {'name': self.name, 'age': self.age, 'location': self.location, 'self_summary': self.self_summary,
                     'instagram': self.extracted_instagram_username}

        self._save_users_profile_picture(user_data)
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
        text = remove_emojis(text)
        if text.endswith("."):
            text = text[:-1]

        instagram_mentions = ['ig', 'instagram']

        # search for certain known formats on instagram nicknames
        ig_with_low_shift = re.findall('\w+_+\w+', text)
        ig_with_dot = re.findall('\s\w+.+\w+\s', text)
        ig_with_digits = re.findall('\w+\d+', text)
        ig_at_gign = re.findall('@\w+', text)
        instagram_nickname = ''
        if ig_at_gign:
            instagram_nickname = ig_at_gign[0].strip()
        if ig_with_low_shift:
            instagram_nickname = ig_with_low_shift[0].strip()
        # if ig_with_dot:
        #     instagram_nickname = ig_with_dot[0].strip()
        if ig_with_digits:
            if not ig_with_digits[0].isdigit():
                instagram_nickname = ig_with_digits[0].strip()
        if instagram_nickname:
            # ig_index = text.find(instagram_nickname)
            # if ig_index != 0:
            #     character_before_ig_string = text[ig_index-1]
            #     if character_before_ig_string != '' and character_before_ig_string != ' ':
            return instagram_nickname

        for i in instagram_mentions:
            if i in text:
                if process_ig_words:
                    continue
                print("-" * THIRTY, "The user has mentioned its instagram user:")
                possible_instagram = text.split(i)[1].split(' ')
                if len(possible_instagram[0]) < 5:
                    user_instagram = possible_instagram[1]
                else:
                    user_instagram = possible_instagram[0]
                user_instagram = user_instagram.strip()
                ig_result = re.sub('[-:=]', '', user_instagram)

                loweralphabets = "abcdefghijklmnopqrstuvwxyz"
                upperalphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                digits = "123456789"
                special_chars = "_."
                x = loweralphabets + upperalphabets + digits + special_chars
                res = []
                for u in ig_result:
                    a = ""
                    for h in u:
                        if h in x:
                            a += h
                    res.append(a)

                ig_of_user = ''.join(res).strip()
                print(ig_of_user)
                return ig_of_user
        return None

    # self.last_user = {'name': '', 'age': 0, 'location': ''}

    def _save_users_profile_picture(self, user_parameters):
        time.sleep(2)
        profile_image_xpath = self.driver.find_element(by=By.CLASS_NAME, value=
        'profile-thumb')
        profile_image_xpath.click()
        time.sleep(2)
        profile_picture = self.driver.find_element(by=By.CLASS_NAME, value='photo-overlay-images')
        image = Image.open(io.BytesIO(profile_picture.screenshot_as_png))

        # converting the file from rgb to jpg and saving it
        image = image.convert("RGB")
        image.save('picture.jpg')
        time.sleep(2)

        # saving user's parameters in order to use them as the picture's indicator name
        name = user_parameters['name']
        age = user_parameters['age']
        location = user_parameters['location']
        generate_random_id = generate_id()

        # escaping the big picture screen
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        # TODO : bugfix the shit here - saved picture to the wrong folder

        # building the path to save the picture at and making sure the folder exists
        project_source_folder = os.path.abspath('.')
        profile_pictures_folder = os.path.join(project_source_folder, 'profile_pictures')
        if not os.path.exists(profile_pictures_folder):
            os.mkdir(profile_pictures_folder)

        image.save(os.path.join(profile_pictures_folder, f"{name}_{age}_{location}_{generate_random_id}.jpg"))

        print(f"Finished copying {user_parameters['name']}'s picture")

    def _take_screenshot(self):
        users_name = self.driver.find_element(by=By.CLASS_NAME, value='profile-basics-username-text')
        generated_id = generate_id()
        self.driver.save_screenshot(f"{users_name}_screenshot_{generated_id}.png")


