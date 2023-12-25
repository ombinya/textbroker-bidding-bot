from selenium.webdriver.common.by import By


class TBAccount:
    def __init__(self, driver, email, password):
        self.driver = driver
        self.email = email
        self.password = password

    def access_account(self):
        self.driver.get("https://www.textbroker.com")

        # Find the Log in link in the navigation bar and click it
        navigation = self.driver.find_element(By.ID, "navigation")
        links = navigation.find_elements(By.TAG_NAME, "a")
        for link in links:
            if link.text == "LOGIN":
                link.click()
                break

        # If the browser remembers you, proceed to the orders page.
        # Otherwise, you must sign in.
        if "home.php" in self.driver.current_url:
            print("Direct access. No need to sign in")
        elif "/login" in self.driver.current_url:
            print("Signing in...")
            self.sign_in()

    def sign_in(self):
        while True:
            try:
                radioGroup = self.driver.find_element(
                    By.XPATH, "//div[@role='radiogroup']")
                break
            except:
                pass

        cols = radioGroup.find_elements(By.CLASS_NAME, "col-sm-6")
        cols[1].click()

        # Enter email
        emailInputField = self.driver.find_element(By.ID, "emailInput")
        emailInputField.clear()
        emailInputField.send_keys(self.email)

        # Enter password
        passwordInputField = self.driver.find_element(By.ID, "passwordInput")
        passwordInputField.clear()
        passwordInputField.send_keys(self.password)

        loginButton = self.driver.find_element(
            By.XPATH, "//button[@data-callback='loginFormSubmit']")
        loginButton.click()

        while True:
            if "/login" not in self.driver.current_url:
                return

    def openOrderLinks(self, orderTable):
        linkTags = orderTable.find_elements(By.TAG_NAME, "a")

        for linkTag in linkTags:
            while True:
                try:
                    linkTag.click()
                except:
                    break
            try:
                tableText = orderTable.text

                if "another author." in tableText:
                    print("Taken by another author")
                    continue
            except:
                pass

            if "Article details" in self.driver.page_source:
                self.driver.refresh()
                terminate = True

            try:
                self.agree_to_write()
                terminate = True
                print("Order locked!")
                break
            except:
                pass

            # Order is yours
            if terminate:
                return True

        return terminate

    def get_results_table(self):
        basicTables = self.driver.find_elements(
            By.XPATH, "//table[@class='basic']")
        searchResultsTable = None

        for t in basicTables:
            if "Title Client ID Quality level Deadline Number of words Possible earnings" in t.text:
                searchResultsTable = t
                break

        assert searchResultsTable
        return searchResultsTable

    def agree_to_write(self):
        tables = self.driver.find_elements(By.TAG_NAME, "table")

        for table in tables:
            if "Order ID" in table.text[:15]:
                break

        tableText = table.text
        tableItems = tableText.split("\n")
        orderId = tableItems[0].split(": ")[1]
        takeOrderBtn = self.driver.find_element(By.ID, "submit_" + orderId)
        takeOrderBtn.click()
