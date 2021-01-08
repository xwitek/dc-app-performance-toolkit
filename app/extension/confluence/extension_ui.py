from selenium.webdriver.common.by import By
from selenium_ui.conftest import print_timing
from util.conf import CONFLUENCE_SETTINGS
import random


from selenium_ui.base_page import BasePage


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_pages']:
        app_specific_page = datasets['custom_pages']

        #app_spec_page_id = datasets['page_id']  #obsahuje i stranky ze spacu DS
        #vyber nahodne stranky z poolu, aby nebyla v DS spacu - tam se nahodne chytaji klavesove zkratky i kdyz nemaji
        app_spec_page_id=""
        while app_spec_page_id == "":
            randPage = random.choice (datasets['pages'])
            print(f"Page selected: {randPage[0]} - {randPage[1]}")
            if randPage[1] != 'ds':
              app_spec_page_id = randPage[0]
              print(f"Page {randPage} assigned.")
        
        app_spec_username = datasets['username']
        

    @print_timing("selenium_app_custom_action")
    def measure():

        @print_timing("selenium_app_custom_action:viewPageReaders")
        def sub_viewPageReaders():
          
            print("===============CUSTOM ACTION READERS LOG============")
            #print(datasets)
            print (f"PageID: {app_spec_page_id}")
            print (app_spec_username)
            print(f"{CONFLUENCE_SETTINGS.server_url}/plugins/readers-page/showpageelements.action?pageId={app_spec_page_id}")
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/readers-page/showpageelements.action?pageId={app_spec_page_id}")
            print("Page called")
            page.wait_until_visible((By.ID, "admin-restful-table"))
            print("Page wait complete")
            button_add = webdriver.find_elements(By.ID, "dialog-show-button")
            assert len(button_add) > 0
            print("========= Assert 1 complete")
           
        @print_timing("selenium_app_custom_action:addPageReaderUser")
        def sub_addPageReaderUser():
        
            webdriver.find_element(By.ID, "dialog-show-button").click()
            page.wait_until_visible((By.ID, "admin-dialog"))
            
            
            elements = webdriver.find_elements(By.CSS_SELECTOR, "#admin-dialog > .aui-dialog2-header")
            assert len(elements) > 0
            print("========= Assert 2 complete")
            
            
            element = webdriver.find_element(By.LINK_TEXT, "Start typing for selecting user...")
            print("Find complete")
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-1-find1.png")
            
            page.wait_until_visible((By.CSS_SELECTOR, ".select2-choice"))
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-2-wait1.png")
            print("Wait 1 complete")
            webdriver.find_element(By.CSS_SELECTOR, ".select2-choice").click()
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-3-action1.png")
            print("Action 1 complete")
            webdriver.implicitly_wait(1)
            webdriver.find_element(By.CSS_SELECTOR, ".select2-choice").send_keys(app_spec_username)
            
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-4-action2.png")
            print("Action 2 complete")
            webdriver.implicitly_wait(2)
            page.wait_until_visible((By.CSS_SELECTOR, ".select2-result-label"))           #Kdyz toto zhuci, je pravdepodobne uzivateli jiz reader element prirazen na teto strance a nema smysl pokracovat jinak nez prohlednutim a potvrzenim stranky.
            elements = webdriver.find_elements(By.CSS_SELECTOR, ".select2-result-label")
            if len(elements) == 0:
                print("User {app_spec_username} cannot be added as a reader to page {app_spec_page_id}")
                webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-5-action3-err.png")
                return
                
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-5-action3.png")
            print("Action 3 complete")
            webdriver.find_element(By.CSS_SELECTOR, ".select2-result-label").click()
            print("Action 4 complete")
            page.wait_until_visible((By.ID, "users-and-groups"))
            print("Wait 2 complete")
            #page.wait_until_visible((By.CSS_SELECTOR, ".mht-table-username")):    #Kdyz toto zhuci, je pravdepodobne uzivateli jiz reader element prirazen na teto strance a nema smysl pokracovat jinak nez prohlednutim a potvrzenim stranky.
            print("Wait 3 complete")
            elements = webdriver.find_elements(By.CSS_SELECTOR, ".mht-table-username")
            if len(elements) == 0:
                return
            print("Assert 3 complete")
            assert webdriver.find_element(By.CSS_SELECTOR, ".mht-table-username").text == app_spec_username
            print("Assert 4 complete")
            webdriver.find_element(By.ID, "dialog-next-button").click()
            print("Action 5 complete")
            page.wait_until_visible((By.ID, "require-confirmation"))
            print("Wait 4 complete")
            webdriver.find_element(By.ID, "require-confirmation").click()
            print("Action 6 complete")
            webdriver.find_element(By.ID, "dialog-submit-button").click()
            print("Action 7 complete")
            #Tady by se mohlo overit, ze se reader element zalozil.
            
        @print_timing("selenium_app_custom_action:confirmPageRead")
        def sub_confirmPageRead():
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/pages/viewpage.action?pageId={app_spec_page_id}")
            print("Action 8 complete")
            page.wait_until_visible((By.ID, "reader-expander-trigger-top"))
            elements = webdriver.find_elements(By.ID, "reader-expander-trigger-top")
            assert len(elements) > 0
            print("Assert 5 complete")
            
            webdriver.find_element(By.ID, "reader-expander-trigger-top").click()
            print("Action 9 complete")
            
            assert webdriver.find_element(By.CSS_SELECTOR, ".aui-group:nth-child(1) > .aui-item:nth-child(1)").text == "You are required to read this page and confirm your reading by buttons below."
            print("Assert 6 complete")
            
            webdriver.find_element(By.ID, "reader-button-confirm-top").click()
            print("Action 10 complete")
            
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/pages/viewpage.action?pageId={app_spec_page_id}")
            print("Action 10 complete")
            elements = webdriver.find_elements(By.ID, "reader-expander-trigger-top")
            assert len(elements) == 0
            print("Assert 7 complete")
            
            """
            webdriver.get("http://ec2-18-156-200-53.eu-central-1.compute.amazonaws.com:8090/pages/viewpage.action?pageId=app_spec_page_id")
            elements = webdriver.find_elements(By.ID, "reader-expander-trigger-top")
            assert len(elements) > 0
            webdriver.find_element(By.ID, "reader-expander-trigger-top").click()
            assert webdriver.find_element(By.CSS_SELECTOR, ".aui-group:nth-child(1) > .aui-item:nth-child(1)").text == "You are required to read this page and confirm your reading by buttons below."
            webdriver.find_element(By.ID, "reader-button-confirm-top").click()
            webdriver.get("http://ec2-18-156-200-53.eu-central-1.compute.amazonaws.com:8090/pages/viewpage.action?pageId=app_spec_page_id")
            elements = webdriver.find_elements(By.ID, "reader-expander-trigger-top")
            assert len(elements) == 0
            """
        
        if app_spec_page_id != "":
          sub_viewPageReaders()
          sub_addPageReaderUser()
          sub_confirmPageRead()
    measure()

