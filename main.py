import time
from utils.personal_info import OPENING_LINE
from main_logic.main_okcupid_logics import ScrapeOkCupidApp
from main_logic.login_logics import Login
from exceptions_and_popups_handlers.close_pop_ups import ClosePopUps
from make_connection.contact_user import ReachOutToUser


def main():
    #  open OkCupid and navigate to the main page
    chrome_navigator = ScrapeOkCupidApp()
    chrome_navigator.open_application()
    time.sleep(5)

    # Create a general web-drive object for the usage of the rest of the classes
    driver = chrome_navigator.share_web_drive_object()

    # login to OkCupid
    app_login = Login(driver)
    if not app_login.logged_in():
        app_login.login()

    # Navigate to the 'liked users' section
    chrome_navigator.navigate_to_liked_users_webpage()

    # Handle pop-ups of the OkCupid App
    # pop_ups_handler = ClosePopUps(driver)
    # pop_ups_handler.close_cookies_tracking_permission_window() - return this line if needed

    # Start sending messages
    contact_user_logic = ReachOutToUser(driver)
    contact_user_logic.send_messages(number_of_users_to_contact=50, message=OPENING_LINE)


if __name__ == '__main__':
    main()
