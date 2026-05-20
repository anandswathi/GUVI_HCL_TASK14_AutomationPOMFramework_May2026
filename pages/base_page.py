from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import Config
from utils.logger import get_logger


# ------------------------------------------------------------------- #
# Read framework configuration
# ------------------------------------------------------------------- #

config = Config()

# Fetch explicit wait timeout from config file
timeout_time = int(config.get_config("DEFAULT", "explicit_wait"))


class BasePage:
    """
    Base Page class for all Page Objects.

    This class contains:
        - Common Selenium actions
        - Explicit waits
        - Logging
        - Utility methods

    Every page class should inherit from this class.
    """

    def __init__(self, driver, timeout: int = timeout_time):

        # Selenium WebDriver instance
        self.driver = driver

        # Explicit wait object
        # Used to wait until conditions are satisfied
        self.wait = WebDriverWait(driver, timeout)

        # Store timeout value
        self.timeout = timeout

        # Create logger using subclass module name
        # Example: pages.login_page
        self.log = get_logger(self.__class__.__module__)

    # ================================================================= #
    # NAVIGATION METHODS
    # ================================================================= #

    def open(self, url: str) -> None:
        """
        Navigate to the given URL.
        """

        # Log navigation activity
        self.log.info(f"Navigating to URL: {url}")

        # Open URL in browser
        self.driver.get(url)

    def get_current_url(self) -> str:
        """
        Return current browser URL.
        """

        # Fetch current URL
        url = self.driver.current_url

        # Log current URL
        self.log.debug(f"Current URL: {url}")

        return url

    def get_page_title(self) -> str:
        """
        Return current page title.
        """

        # Fetch page title
        title = self.driver.title

        # Log page title
        self.log.debug(f"Page title: {title!r}")

        return title

    def refresh_page(self) -> None:
        """
        Refresh the current browser page.
        """

        # Log refresh action
        self.log.info("Refreshing the current page.")

        # Refresh browser page
        self.driver.refresh()

    # ================================================================= #
    # EXPLICIT WAIT METHODS
    # ================================================================= #

    def find_element_visible(self, locator: tuple):
        """
        Wait until element becomes visible.
        Returns the WebElement.
        """

        # Log wait action
        self.log.debug(f"Waiting for VISIBLE: {locator}")

        try:
            # Wait until element is visible
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            # Log success
            self.log.debug(f"Element VISIBLE: {locator}")

            return element

        except TimeoutException:

            # Log timeout error
            self.log.error(
                f"TIMEOUT — not visible after {self.timeout}s: {locator}"
            )

            # Raise custom timeout exception
            raise TimeoutException(
                f"Element not visible after {self.timeout}s → {locator}"
            )

    def find_element_clickable(self, locator: tuple):
        """
        Wait until element becomes clickable.
        Returns the WebElement.
        """

        self.log.debug(f"Waiting for CLICKABLE: {locator}")

        try:
            # Wait until element is clickable
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            self.log.debug(f"Element CLICKABLE: {locator}")

            return element

        except TimeoutException:

            self.log.error(
                f"TIMEOUT — not clickable after {self.timeout}s: {locator}"
            )

            raise TimeoutException(
                f"Element not clickable after {self.timeout}s → {locator}"
            )

    def find_element_present(self, locator: tuple):
        """
        Wait until element is present in DOM.
        Returns the WebElement.
        """

        self.log.debug(f"Waiting for PRESENT: {locator}")

        try:
            # Wait until element exists in DOM
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )

            self.log.debug(f"Element PRESENT: {locator}")

            return element

        except TimeoutException:

            self.log.error(
                f"TIMEOUT — not present after {self.timeout}s: {locator}"
            )

            raise TimeoutException(
                f"Element not present after {self.timeout}s → {locator}"
            )

    # ================================================================= #
    # ELEMENT INTERACTION METHODS
    # ================================================================= #

    def click(self, locator: tuple) -> None:
        """
        Click on an element.
        """

        # Log click action
        self.log.info(f"Clicking: {locator}")

        try:
            # Wait until element becomes clickable
            # Then perform click
            self.find_element_clickable(locator).click()

            self.log.debug(f"Click successful: {locator}")

        except (
            ElementNotInteractableException,
            ElementClickInterceptedException,
        ):

            # Log click failure
            self.log.warning(
                f"Element not interactable/intercepted: {locator}"
            )

            raise

    def type_text_into_text_field(
        self,
        locator: tuple,
        text: str,
    ) -> None:
        """
        Clear text field and enter text.
        Password values are masked in logs.
        """

        # Mask password in logs for security
        if "password" in str(locator).lower():
            display_text = "*" * len(text)
        else:
            display_text = text

        # Log typing action
        self.log.info(
            f"Typing '{display_text}' into: {locator}"
        )

        try:
            # Wait until field is visible
            field = self.find_element_visible(locator)

            # Clear existing text
            field.clear()

            # Enter new text
            field.send_keys(text)

            self.log.debug(f"Text entered into: {locator}")

        except ElementNotInteractableException as e:

            self.log.error(
                f"ElementNotInteractableException on {locator}: {e}"
            )

            raise

    def get_text(self, locator: tuple) -> str:
        """
        Return visible text from an element.
        """

        # Get visible text and remove extra spaces
        text = self.find_element_visible(locator).text.strip()

        # Log extracted text
        self.log.debug(f"Got text {text!r} from: {locator}")

        return text

    def get_attribute(
        self,
        locator: tuple,
        attribute: str,
    ) -> str:
        """
        Return value of a given attribute.
        """

        # Fetch attribute value
        value = self.find_element_present(locator).get_attribute(attribute)

        # Log attribute value
        self.log.debug(
            f"Attribute '{attribute}' = {value!r} from: {locator}"
        )

        return value

    def is_element_displayed(self, locator: tuple) -> bool:
        """
        Return True if element is visible on screen.
        """

        try:
            # Check visibility status
            result = self.find_element_visible(locator).is_displayed()

            self.log.debug(
                f"is_displayed = {result}: {locator}"
            )

            return result

        except (TimeoutException, NoSuchElementException):

            # Element not found/visible
            self.log.debug(
                f"Element not found for is_displayed: {locator}"
            )

            return False

    def is_element_enabled(self, locator: tuple) -> bool:
        """
        Return True if element is enabled.
        """

        try:
            # Check enabled status
            result = self.find_element_visible(locator).is_enabled()

            self.log.debug(
                f"is_enabled = {result}: {locator}"
            )

            return result

        except (TimeoutException, NoSuchElementException):

            self.log.debug(
                f"Element not found for is_enabled: {locator}"
            )

            return False

    # ================================================================= #
    # URL WAIT METHODS
    # ================================================================= #

    def wait_for_url_contains(self, substring: str) -> bool:
        """
        Wait until current URL contains given substring.
        """

        self.log.debug(
            f"Waiting for URL to contain: {substring!r}"
        )

        try:
            # Wait until URL contains substring
            result = self.wait.until(
                EC.url_contains(substring)
            )

            self.log.info(
                f"URL now contains: {substring!r}"
            )

            return result

        except TimeoutException:

            self.log.warning(
                f"URL did not contain {substring!r} "
                f"within {self.timeout}s"
            )

            return False

    def wait_for_url_changes(self, current_url: str) -> bool:
        """
        Wait until URL changes from current URL.
        """

        self.log.debug(
            f"Waiting for URL to change from: {current_url}"
        )

        try:
            # Wait until URL changes
            result = self.wait.until(
                EC.url_changes(current_url)
            )

            self.log.info(
                f"URL changed from: {current_url}"
            )

            return result

        except TimeoutException:

            self.log.warning(
                f"URL did not change from "
                f"{current_url!r} within {self.timeout}s"
            )

            return False