from selenium import webdriver


class Browser:
    def __init__(self, userDataPath, executablePath):
        # Browser settings
        self.userDataPath = userDataPath
        self.executablePath = executablePath
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"--user-data-dir=" + self.userDataPath)

    def get_driver(self):
        """Fires up the Chrome browser and returns the Chrome webdriver object.
        """
        self.driver = webdriver.Chrome(
            executable_path=self.executablePath,
            chrome_options=self.options
        )

        self.driver.implicitly_wait(5)

        return self.driver
