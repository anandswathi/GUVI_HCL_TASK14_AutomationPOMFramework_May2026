from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)

from pages.base_page import BasePage
from utils.config_reader import Config


class LoginPage(BasePage):
    """
    Page Object Model for Login Page.

    This class contains:
        - Login page actions
        - Field validations
        - Error message validations
        - Login workflow methods
    """

    # ================================================================= #
    # CONFIGURATION
    # ================================================================= #

    # Read configuration file
    config = Config()

    # Login page URL from config file
    URL = config.get_config("URL", "login_url")

    # ================================================================= #
    # LOCATORS
    # ================================================================= #

    # Email input field
    EMAIL_FIELD = (
        By.XPATH,
        "//input[@placeholder='Enter your mail']",
    )

    # Password input field
    PASSWORD_FIELD = (
        By.XPATH,
        "//input[@placeholder='Enter your password ']",
    )

    # Sign In button
    SIGNIN_BTN = (
        By.XPATH,
        "//button[text()='Sign in']",
    )

    # Email validation error message
    EMAIL_ERROR = (
        By.XPATH,
        "//p[contains(text(), 'Incorrect email!') "
        "or contains(text(),'Email required!')]",
    )

    # Password validation error message
    PASSWORD_ERROR = (
        By.XPATH,
        "//p[contains(text(), 'Incorrect password!') "
        "or contains(text(), 'Password required!') "
        "or contains(text(), 'Email and password required!')]",
    )

    # ================================================================= #
    # CONSTRUCTOR
    # ================================================================= #

    def __init__(self, driver):

        # Initialize BasePage constructor
        super().__init__(driver)

    # ================================================================= #
    # PAGE ACTION METHODS
    # ================================================================= #

    def open_login_page(self) -> "LoginPage":
        """
        Open the application login page.

        Returns:
            LoginPage: Current page object instance
        """

        # Log navigation activity
        self.log.info("Opening Zen Portal login page.")

        # Navigate to login URL
        self.open(self.URL)

        return self

    def enter_email(self, email: str) -> "LoginPage":
        """
        Enter email into email input field.

        Args:
            email (str): User email address

        Returns:
            LoginPage: Current page object instance
        """

        # Log email entry action
        self.log.info(f"Entering email: {email!r}")

        # Enter email text
        self.type_text_into_text_field(
            self.EMAIL_FIELD,
            email,
        )

        return self

    def enter_password(self, password: str) -> "LoginPage":
        """
        Enter password into password input field.

        Password is masked in logs.

        Args:
            password (str): User password

        Returns:
            LoginPage: Current page object instance
        """

        # Log password action without exposing password
        self.log.info("Entering password: ***")

        # Enter password text
        self.type_text_into_text_field(
            self.PASSWORD_FIELD,
            password,
        )

        return self

    def click_signin_button(self) -> None:
        """
        Click the Sign In button.
        """

        # Log click action
        self.log.info("Clicking the Sign In button.")

        # Click sign in button
        self.click(self.SIGNIN_BTN)

    def login(
        self,
        email: str,
        password: str,
    ) -> None:
        """
        Perform complete login workflow.

        Steps:
            1. Enter email
            2. Enter password
            3. Click Sign In button

        Args:
            email (str): User email address
            password (str): User password
        """

        # Log login workflow start
        self.log.info(
            f"Starting login flow for: {email!r}"
        )

        # Enter email
        self.enter_email(email)

        # Enter password
        self.enter_password(password)

        # Click login button
        self.click_signin_button()

        # Log login submission
        self.log.info("Login form submitted.")

    # ================================================================= #
    # FIELD DISPLAY / ENABLED VALIDATIONS
    # ================================================================= #

    def is_email_field_displayed(self) -> bool:
        """
        Verify whether email field is visible.
        """

        self.log.debug(
            "Checking if email field is displayed."
        )

        return self.is_element_displayed(
            self.EMAIL_FIELD
        )

    def is_email_field_enabled(self) -> bool:
        """
        Verify whether email field is enabled.
        """

        self.log.debug(
            "Checking if email field is enabled."
        )

        return self.is_element_enabled(
            self.EMAIL_FIELD
        )

    def is_password_field_displayed(self) -> bool:
        """
        Verify whether password field is visible.
        """

        self.log.debug(
            "Checking if password field is displayed."
        )

        return self.is_element_displayed(
            self.PASSWORD_FIELD
        )

    def is_password_field_enabled(self) -> bool:
        """
        Verify whether password field is enabled.
        """

        self.log.debug(
            "Checking if password field is enabled."
        )

        return self.is_element_enabled(
            self.PASSWORD_FIELD
        )

    def is_signin_button_displayed(self) -> bool:
        """
        Verify whether Sign In button is visible.
        """

        self.log.debug(
            "Checking if sign-in button is displayed."
        )

        return self.is_element_displayed(
            self.SIGNIN_BTN
        )

    def is_signin_button_enabled(self) -> bool:
        """
        Verify whether Sign In button is enabled.
        """

        self.log.debug(
            "Checking if sign-in button is enabled."
        )

        return self.is_element_enabled(
            self.SIGNIN_BTN
        )

    # ================================================================= #
    # FIELD VALUE METHODS
    # ================================================================= #

    def get_email_field_value(self) -> str:
        """
        Return current value from email field.
        """

        # Get field value
        value = self.get_attribute(
            self.EMAIL_FIELD,
            "value",
        )

        # Log value
        self.log.debug(
            f"Email field value: {value!r}"
        )

        return value

    def get_password_field_value(self) -> str:
        """
        Return current value from password field.
        """

        # Get password field value
        value = self.get_attribute(
            self.PASSWORD_FIELD,
            "value",
        )

        # Log without exposing password
        self.log.debug(
            "Password field has a value (masked)."
        )

        return value

    # ================================================================= #
    # ERROR MESSAGE METHODS
    # ================================================================= #

    def get_email_error_text(self) -> str:
        """
        Return email validation error message.

        Returns empty string if error message is absent.
        """

        try:
            # Fetch email error text
            text = self.get_text(self.EMAIL_ERROR)

            # Log error message
            self.log.debug(
                f"Email error text: {text!r}"
            )

            return text

        except TimeoutException:

            # Error message not displayed
            self.log.debug(
                "No email error message found."
            )

            return ""

    def get_password_error_text(self) -> str:
        """
        Return password validation error message.

        Returns empty string if error message is absent.
        """

        try:
            # Fetch password error text
            text = self.get_text(self.PASSWORD_ERROR)

            # Log error message
            self.log.debug(
                f"Password error text: {text!r}"
            )

            return text

        except TimeoutException:

            # Error message not displayed
            self.log.debug(
                "No password error message found."
            )

            return ""

    # ================================================================= #
    # PAGE VALIDATION METHODS
    # ================================================================= #

    def is_on_login_page(self) -> bool:
        """
        Verify whether browser is currently on login page.
        """

        # Validate login URL
        on_page = "login" in self.get_current_url()

        # Log validation result
        self.log.debug(
            f"Is on login page: {on_page}"
        )

        return on_page