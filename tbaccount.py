from selenium.webdriver.common.by import By


class TBAccount:
    def __init__(self, driver, email, password):
        self.driver = driver
        self.email = email
        self.password = password

    def access_account(self):
        """Navigates to the Log In page and signs in to the Textbroker account. Since the User Data folder is included in the project, 
        it is likely that the Textbroker site will remember your account. In such a case, the 
        Textbroker account will be signed in automatically.
        """

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
        """Fills in user credentials and clicks the Log In button
        """

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
        """Attempts to open each order link in the order table and takes an order. 
        If an order is captured, any attempt to continue looking for orders should be terminated.

        Keyword arguments:
        orderTable -- table element which carries order links.
        Return: True, if the bot successfully captures an order. Otherwise, False.
        """

        linkTags = orderTable.find_elements(By.TAG_NAME, "a")

        for linkTag in linkTags:
            linkTag.click()

            tableText = orderTable.text

            # The order has been taken by another author
            if "another author." in tableText:
                continue

            # The phrase 'Article details' will only appear if the order is yours for the taking
            if "Article details" in self.driver.page_source:
                self.driver.refresh()
                terminate = True

            # If the accept button is visible, click it to agree to write
            # Comment out these lines if you prefer to read the instructions first before accepting to write
            # ----------------------------------------------------------------------------------------------
            try:
                self.agree_to_write()
                break
            except:
                pass
            # ----------------------------------------------------------------------------------------------

            # Order is yours, no need to go on to the other order links.
            if terminate:
                return True

        # False
        return terminate

    def get_results_table(self):
        """Locate the table element representing the search results table and return it.

        Return: table element representing the search results table
        """

        basicTables = self.driver.find_elements(
            By.XPATH, "//table[@class='basic']")
        searchResultsTable = None

        for t in basicTables:
            if "Title Client ID Quality level Deadline Number of words Possible earnings" in t.text:
                searchResultsTable = t
                break

        return searchResultsTable

    def agree_to_write(self):
        """Locate the accept order button and click it.
        """

        tables = self.driver.find_elements(By.TAG_NAME, "table")

        for table in tables:
            if "Order ID" in table.text[:15]:
                break

        tableText = table.text
        tableItems = tableText.split("\n")
        orderId = tableItems[0].split(": ")[1]
        takeOrderBtn = self.driver.find_element(By.ID, "submit_" + orderId)
        takeOrderBtn.click()
