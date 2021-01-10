from selenium.webdriver.common.by import By
from selenium_ui.conftest import print_timing
from util.conf import CONFLUENCE_SETTINGS
from selenium_ui.base_page import BasePage

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    #print(datasets)
    app_specific_page = datasets['custom_pages']
    app_spec_page_id = datasets['page_id']

    app_spec_username = datasets['username']

    print(f"PageID: {app_spec_page_id}")
    print(app_spec_username)
    custDebug = True
        

    @print_timing("selenium_app_custom_action")
    def measure():

        @print_timing("selenium_app_custom_action:viewPageReaders")
        def sub_viewPageReaders():

            print("===============CUSTOM ACTION READERS LOG============")
            
            print(f"{CONFLUENCE_SETTINGS.server_url}/plugins/readers-page/showpageelements.action?pageId={app_spec_page_id}")
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/readers-page/showpageelements.action?pageId={app_spec_page_id}")
            if custDebug: print("Page called")
            page.wait_until_visible((By.ID, "admin-restful-table"))
            if custDebug: print("Page wait complete")
            button_add = webdriver.find_elements(By.ID, "dialog-show-button")
            assert len(button_add) > 0
            if custDebug: print("========= Assert 1 complete")
           
        @print_timing("selenium_app_custom_action:addPageReaderUser")
        def sub_addPageReaderUser():
        
            webdriver.find_element(By.ID, "dialog-show-button").click()
            page.wait_until_visible((By.ID, "admin-dialog"))
            
            
            elements = webdriver.find_elements(By.CSS_SELECTOR, "#admin-dialog > .aui-dialog2-header")
            assert len(elements) > 0
            if custDebug: print("========= Assert 2 complete")
            
            
            element = webdriver.find_element(By.LINK_TEXT, "Start typing for selecting user...")
            if custDebug: print("Find complete")
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-1-find1.png")
            
            page.wait_until_visible((By.CSS_SELECTOR, ".select2-choice"))
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-2-wait1.png")
            if custDebug: print("Wait 1 complete")
            webdriver.find_element(By.CSS_SELECTOR, ".select2-choice").click()
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-3-action1.png")
            if custDebug: print("Action 1 complete")
            #webdriver.implicitly_wait(5)
            webdriver.find_element(By.CSS_SELECTOR, ".select2-choice").send_keys(app_spec_username)
            
            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-4-action2.png")
            if custDebug: print("Action 2 complete")
            #webdriver.implicitly_wait(5)
            try:
              page.wait_until_visible((By.CSS_SELECTOR, ".select2-result-label"))           #Kdyz toto zhuci, je pravdepodobne uzivateli jiz reader element prirazen na teto strance a nema smysl pokracovat jinak nez prohlednutim a potvrzenim stranky.
              if custDebug: print("Wait for .select2-result-label complete")
              elements = webdriver.find_elements(By.CSS_SELECTOR, ".select2-result-label")
              if len(elements) == 0:
                  if custDebug: print("User {app_spec_username} cannot be added as a reader to page {app_spec_page_id}")
                  #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-5-action3-err.png")
                  return
            except:
                print(f"User {app_spec_username} cannot be selected for some reasons. OK.")
                return

            #webdriver.save_screenshot(f"./debug/{app_spec_page_id}-{app_spec_username}-5-action3.png")
            if custDebug: print("Action 3 complete")
            webdriver.find_element(By.CSS_SELECTOR, ".select2-result-label").click()
            if custDebug: print("Action 4 complete")
            page.wait_until_visible((By.ID, "users-and-groups"))
            if custDebug: print("Wait 2 complete")
            #page.wait_until_visible((By.CSS_SELECTOR, ".mht-table-username")):    #Kdyz toto zhuci, je pravdepodobne uzivateli jiz reader element prirazen na teto strance a nema smysl pokracovat jinak nez prohlednutim a potvrzenim stranky.
            if custDebug: print("Wait 3 complete")
            elements = webdriver.find_elements(By.CSS_SELECTOR, ".mht-table-username")
            if len(elements) == 0:
                if custDebug: print(f"User {app_spec_username} is already added as a reader. OK.")
                return
            if custDebug: print("========= Assert 3 complete")
            assert webdriver.find_element(By.CSS_SELECTOR, ".mht-table-username").text == app_spec_username
            if custDebug: print("========= Assert 4 complete")
            webdriver.find_element(By.ID, "dialog-next-button").click()
            if custDebug: print("Action 5 complete")
            page.wait_until_visible((By.ID, "require-confirmation"))
            if custDebug: print("Wait 4 complete")
            webdriver.find_element(By.ID, "require-confirmation").click()
            if custDebug: print("Action 6 complete")
            webdriver.find_element(By.ID, "dialog-submit-button").click()
            if custDebug: print("Action 7 complete")
            #Tady by se mohlo overit, ze se reader element zalozil.

        @print_timing("selenium_app_custom_action:confirmPageRead")
        def sub_confirmPageRead():
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/pages/viewpage.action?pageId={app_spec_page_id}")
            if custDebug: print("Action 8 complete")

            try:
                page.wait_until_visible((By.ID, "reader-expander-trigger-top"))
                elements = webdriver.find_elements(By.ID, "reader-expander-trigger-top")
                assert len(elements) > 0
                if custDebug: print("======= Assert 5 complete")
                webdriver.find_element(By.ID, "reader-expander-trigger-top").click()
                print("Action 9 complete")
            except:
                print('No reading confirmation on this page.')
                return
            
            assert webdriver.find_element(By.CSS_SELECTOR, ".aui-group:nth-child(1) > .aui-item:nth-child(1)").text == "You are required to read this page and confirm your reading by buttons below."
            if custDebug: print("Assert 6 complete")
            
            webdriver.find_element(By.ID, "reader-button-confirm-top").click()
            if custDebug: print("Action 10 complete")
            
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/pages/viewpage.action?pageId={app_spec_page_id}")
            if custDebug: print("Action 10 complete")
            elements = webdriver.find_elements(By.ID, "reader-expander-trigger-top")
            assert len(elements) == 0
            if custDebug: print("Assert 7 complete")
            
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

