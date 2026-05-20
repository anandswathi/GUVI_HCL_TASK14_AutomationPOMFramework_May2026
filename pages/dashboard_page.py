from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object Model for Dashboard Page.

    This class contains:
        - Dashboard validations
        - Popup handling
        - Logout actions
        - Dashboard state verification
    """

    # ================================================================= #
    # LOCATORS
    # ================================================================= #

    # User avatar/profile icon
    USER_AVATAR = (
        By.XPATH,
        "(//div[contains(@class,'MuiAvatar-root')])[1]",
    )

    # Logout button inside profile dropdown
    LOGOUT_BTN = (
        By.XPATH,
        "//div[contains(text(),'Log out')]",
    )

    # Profile dropdown element
    PROFILE_DROPDOWN = (
        By.XPATH,
        "//p[contains(@class,'avatar-profile-name')]",
    )

    # Dashboard heading/indicator
    DASHBOARD_INDICATOR = (
        By.XPATH,
        "//p[contains(text(),'Dashboard')]",
    )

    # Welcome message displayed on dashboard
    USER_DASHBOARD_WELCOME_MSG = (
        By.XPATH,
        "//p[contains(text(),'Welcome')]",
    )

    # New launch alert popup container
    NEW_LAUNCH_ALERT_POPUP = (
        By.XPATH,
        "//div[@class='mobile-app-promotion-main-div']",
    )

    # Close button for popup
    NEW_LAUNCH_ALERT_POPUP_CLOSE_BTN = (
        By.XPATH,
        "//button[@aria-label='Close popup']",
    )

    # ================================================================= #
    # CONSTRUCTOR
    # ================================================================= #

    def __init__(self, driver):

        # Initialize parent BasePage class
        super().__init__(driver)

    # ================================================================= #
    # DASHBOARD STATE VALIDATIONS
    # ================================================================= #

    def is_logged_in(self) -> bool:
        """
        Verify whether user is successfully logged in.

        Validation checks:
            1. URL should not contain 'login'
            2. Dashboard indicator should be visible
            3. Welcome message should be visible
        """

        try:
            # Validate URL
            url_ok = "login" not in self.get_current_url()

            # Validate dashboard heading visibility
            dashboard_indicator_ok = self.is_element_displayed(
                self.DASHBOARD_INDICATOR
            )

            # Validate welcome message visibility
            user_dashboard_indicator_ok = self.is_element_displayed(
                self.USER_DASHBOARD_WELCOME_MSG
            )

            # Final login validation result
            result = (
                url_ok
                and (
                    dashboard_indicator_ok
                    and user_dashboard_indicator_ok
                )
            )

            # Log validation result
            self.log.info(
                f"is_logged_in={result} | "
                f"URL ok={url_ok}, "
                f"Dashboard Indicator={dashboard_indicator_ok}, "
                f"Welcome Msg={user_dashboard_indicator_ok}"
            )

            return result

        except TimeoutException:

            # Log timeout exception
            self.log.warning(
                "is_logged_in check timed out — returning False."
            )

            return False

    def is_on_dashboard(self) -> bool:
        """
        Verify whether current page is dashboard page.
        """

        # Get current browser URL
        current_url = self.get_current_url()

        # Check whether URL contains 'dashboard'
        result = "dashboard" in current_url

        # Log result
        self.log.debug(
            f"is_on_dashboard={result} "
            f"for URL: {current_url}"
        )

        return result

    # ================================================================= #
    # NEW LAUNCH ALERT POPUP METHODS
    # ================================================================= #

    def close_new_launch_alert_popup(self) -> None:
        """
        Close the New Launch Alert popup.
        """

        self.log.debug(
            "Checking if popup close button "
            "is displayed and enabled."
        )

        # Verify button visibility
        displayed = self.is_element_displayed(
            self.NEW_LAUNCH_ALERT_POPUP_CLOSE_BTN
        )

        # Verify button enabled state
        enabled = self.is_element_enabled(
            self.NEW_LAUNCH_ALERT_POPUP_CLOSE_BTN
        )

        # Log popup button state
        self.log.info(
            f"Popup Close Button — "
            f"displayed={displayed}, enabled={enabled}"
        )

        # Click close button
        self.click(
            self.NEW_LAUNCH_ALERT_POPUP_CLOSE_BTN
        )

    def is_new_launch_alert_popup_displayed(self) -> bool:
        """
        Verify whether New Launch Alert popup is visible.
        """

        self.log.debug(
            "Checking if new launch alert popup is displayed."
        )

        # Check popup visibility
        return self.is_element_displayed(
            self.NEW_LAUNCH_ALERT_POPUP
        )

    # ================================================================= #
    # PROFILE / LOGOUT ACTIONS
    # ================================================================= #

    def click_profile_dropdown(self) -> None:
        """
        Click profile dropdown to reveal logout option.
        """

        # Log action
        self.log.info(
            "Clicking profile dropdown "
            "to reveal Logout option."
        )

        # Click profile dropdown
        self.click(self.PROFILE_DROPDOWN)

    def click_logout(self) -> None:
        """
        Click Logout button.

        If Logout button is not immediately visible,
        open profile dropdown first.
        """

        self.log.info(
            "Attempting to click Logout button."
        )

        try:
            # Attempt direct logout click
            self.click(self.LOGOUT_BTN)

        except TimeoutException:

            # Logout button hidden under dropdown
            self.log.warning(
                "Logout button not visible — "
                "opening profile dropdown first."
            )

            # Open profile dropdown
            self.click_profile_dropdown()

            # Click logout button
            self.click(self.LOGOUT_BTN)

    def logout(self) -> None:
        """
        Complete logout workflow.

        Steps:
            1. Click Logout
            2. Wait for redirect to login page
        """

        self.log.info("Starting logout flow.")

        # Perform logout action
        self.click_logout()

        # Wait until URL contains login
        self.wait_for_url_contains("login")

        # Log successful logout
        self.log.info(
            f"Logout complete. "
            f"Current URL: {self.get_current_url()}"
        )

    # ================================================================= #
    # POST LOGOUT VALIDATIONS
    # ================================================================= #

    def is_logged_out(self) -> bool:
        """
        Verify whether user is successfully logged out.
        """

        # Check whether URL contains login
        result = "login" in self.get_current_url()

        # Log validation result
        self.log.info(f"is_logged_out={result}")

        return result