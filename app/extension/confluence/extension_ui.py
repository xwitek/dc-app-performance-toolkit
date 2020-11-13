from selenium.webdriver.common.by import By
from selenium_ui.conftest import print_timing
from util.conf import CONFLUENCE_SETTINGS

from selenium_ui.base_page import BasePage


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    @print_timing("selenium_app_custom_action")
    def measure():

        @print_timing("selenium_app_custom_action:dbViewActionPage")
        def sub_dbview_action():
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/dbview/dbView.action?actiontype=viewDB")
            page.wait_until_visible((By.XPATH, "//h1[contains(.,\'Confluence Database View\')]"))
            assert webdriver.title == "Confluence Database View - Confluence"
            page.wait_until_visible((By.ID, "inlineDialogTablesShow"))

        @print_timing("selenium_app_custom_action:dbViewActionTables")
        def sub_dbview_tables():
            webdriver.find_element(By.ID, "inlineDialogTablesShow").click()
            page.wait_until_visible((By.LINK_TEXT, "\"AO_8F902A_READER_ELEMENT\""))
            webdriver.find_element(By.LINK_TEXT, "\"AO_8F902A_READER_ELEMENT\"").click()
            elements = webdriver.find_elements(By.CSS_SELECTOR, ".ace_text-input")
            assert len(elements) > 0
            elements = webdriver.find_elements(By.ID, "submitQuery")
            assert len(elements) > 0

        @print_timing("selenium_app_custom_action:dbViewActionTables")
        def sub_dbview_sql_result():
            webdriver.find_element(By.ID, "submitQuery").click()
            page.wait_until_visible((By.ID, "resultTable"))
            assert webdriver.find_element(By.XPATH, "//table[@id=\'resultTable\']/thead/tr/th").text == "AUTHOR_USER_NAME"

        sub_dbview_action()
        sub_dbview_tables()
        sub_dbview_sql_result()
    measure()
