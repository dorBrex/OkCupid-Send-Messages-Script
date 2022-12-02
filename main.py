import time
from utils.personal_info import OPENING_LINE
from scrape_okcupid.main_okcupid_logics import ScrapeOkCupidApp
from scrape_okcupid.login_logics import Login
from exceptions_and_popups_handlers.close_pop_ups import ClosePopUps
from contact_users.contact_user import ContactUser


def main():
    app = ScrapeOkCupidApp()
    app.open_application()
    time.sleep(5)
    driver = app.shared_drive()
    app_login = Login(driver)
    if not app_login.logged_in():
        app_login.login()
    app.navigate_to_liked_users_webpage()
    pop_ups_handler = ClosePopUps(driver)
    pop_ups_handler.close_cookies_tracking_permission_window()
    main_logic = ContactUser(driver)
    main_logic.send_messages_logic(number_of_users_to_contact=50, message=OPENING_LINE)


if __name__ == '__main__':
    main()
