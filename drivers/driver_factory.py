from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class DriverFactory:
    """
    Simple Driver Factory to create and manage Selenium WebDriver.
    """

    # Store single driver instance (Singleton pattern)
    driver = None

    @classmethod
    def get_driver(cls, browser):
        """
        Create or return existing WebDriver.
        """

        # If driver already exists, reuse it
        if cls.driver is not None:
            return cls.driver

        browser = browser.lower()

        # ===================================================== #
        # CHROME BROWSER
        # ===================================================== #
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")

            cls.driver = webdriver.Chrome(options=options)

        # ===================================================== #
        # EDGE BROWSER
        # ===================================================== #
        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")

            cls.driver = webdriver.Edge(options=options)

        # ===================================================== #
        # FIREFOX BROWSER
        # ===================================================== #
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--width=1480")
            options.add_argument("--height=1080")

            # Disable notifications
            options.set_preference("dom.webnotifications.enabled", False)

            cls.driver = webdriver.Firefox(options=options)

        # ===================================================== #
        # INVALID BROWSER
        # ===================================================== #
        else:
            raise ValueError("Browser not supported: " + browser)

        return cls.driver

    @classmethod
    def quit_driver(cls):
        """
        Close browser and reset driver.
        """

        if cls.driver:
            cls.driver.quit()
            cls.driver = None