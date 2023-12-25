import os
from browser import Browser
from tbaccount import TBAccount
from selenium.webdriver.common.by import By
import telegram
import winsound

projectRootFolder = os.path.dirname(os.path.abspath(__file__))

userDataPath = projectRootFolder + r"\User Data"
executablePath = projectRootFolder + r"\chromedriver.exe"

browser = Browser(userDataPath, executablePath)

# Account credentials
email = "example@email.com"
password = "********"

# Telegram Bot information
telegramBotToken = "Telegram Bot Token"
telegramBot = telegram.Bot(telegramBotToken)
telegramChatId = "******"

with browser.get_driver() as driver:
    # Navigate to log in page and access Textbroker account
    tbAccount = TBAccount(driver, email, password)
    tbAccount.access_account()

    print('Redirecting to Open Orders page...')
    driver.get(
        "https://intern.textbroker.com/a/openorder-list-categories.php")

    # Will be true once you have secured an order
    terminate = False

    # The Team orders checkbox is unchecked by default
    # Comment out these lines if you are not willing to complete Team orders
    # ---------------------------------------------------------------------
    while True:
        try:
            driver.find_element(By.ID, "order_type_team_order").click()
            break
        except:
            pass
    # ---------------------------------------------------------------------

    # The level 2 orders checkbox is checked by default
    # Comment out these lines if you are willing to complete level 2 orders
    # ---------------------------------------------------------------------
    while True:
        try:
            driver.find_element(By.ID, "order_type_open_order_2").click()
            break
        except:
            pass
    # ---------------------------------------------------------------------

    while not terminate:
        # Click the 'Start search' button to expose orders if available
        try:
            startSearchBtn = driver.find_element(
                By.XPATH, "//input[@value='Start search']")
            startSearchBtn.click()
        except:
            pass

        # Do nothing if the search results table is not visible
        try:
            searchResultsTable = tbAccount.get_results_table(driver)
            assert searchResultsTable
            tableText = searchResultsTable.text

            # There are tasks available in the search results table
            if "$" in tableText:
                try:
                    terminate = tbAccount.openOrderLinks(searchResultsTable)
                except:
                    pass

                alertSoundPath = projectRootFolder + r"\alert.wav"
                winsound.PlaySound(alertSoundPath, winsound.SND_FILENAME)

                # If you don't want Telegram notifications, comment out this line
                # ---------------------------------------------------------------------
                telegramBot.sendMessage(
                    chat_id=telegramChatId, text='New Order')
                # ---------------------------------------------------------------------
        except:
            pass

        try:
            # You are currently in the submit page, meaning the order is yours to complete
            if "submit" in driver.current_url:
                terminate = True
        except:
            pass

    input("Enter anything and press ENTER to close the browser.")
