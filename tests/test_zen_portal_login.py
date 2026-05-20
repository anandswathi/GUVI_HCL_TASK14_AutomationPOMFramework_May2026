"""
HCL GUVI TASK - 14
The following task needs to be done using Python Selenium, Pytest and Page Object Model (POM).
the following are the details given below :-

1) Use of Page Object Model (POM) and Explicit Wait is mandatory.
2) Goto your Zen Portal
3) Login to the Zen Portal using your valid Username and Password.
4) Once logged in Log Out of the Zen Portal as well.
5) Create a Pytest based HTML report Positive and Negative test-cases for :-
    a) Successful Login
    b) Unsuccessful Login
    c) Validate Username, Password Input box
    d) Validate Submit button working or not
    e) Validate the functionality of the Logout button
6) Usage of Python OOPS and Python Selenium Exceptions are mandatory.
"""
"""
=====================================================================
HCL GUVI TASK - 14 | SELENIUM AUTOMATION PROJECT
=====================================================================

PROJECT TYPE:
    Selenium Automation Testing using Python, Pytest, and POM

FRAMEWORK REQUIREMENTS:
    ✔ Page Object Model (POM) is mandatory
    ✔ Explicit Waits must be used (no hard dependency on sleep)
    ✔ Python OOPS concepts must be implemented
    ✔ Selenium Exception handling is mandatory
    ✔ Pytest framework must be used
    ✔ HTML test report generation required

---------------------------------------------------------------------
APPLICATION UNDER TEST:
    Zen Portal
    https://www.zenclass.in/

---------------------------------------------------------------------
TEST SCENARIOS TO AUTOMATE:

1. LOGIN FUNCTIONALITY
   --------------------------------------------------
   a) Successful login using valid credentials
   b) Unsuccessful login using invalid credentials

2. INPUT FIELD VALIDATION
   --------------------------------------------------
   a) Validate Username (Email) input box
      - Visibility check
      - Enable/disable check
      - Input acceptance validation

   b) Validate Password input box
      - Visibility check
      - Enable/disable check
      - Input acceptance validation

3. SUBMIT BUTTON VALIDATION
   --------------------------------------------------
   a) Verify login (Submit) button is visible and enabled
   b) Verify successful login using valid credentials
   c) Verify unsuccessful login scenarios:
        - Empty credentials
        - Invalid credentials

4. LOGOUT FUNCTIONALITY
   --------------------------------------------------
   a) Verify successful logout
   b) Ensure user is redirected to login page
   c) Verify session is cleared after logout
   d) Ensure dashboard is inaccessible after logout

---------------------------------------------------------------------
TEST DESIGN REQUIREMENTS:

✔ Use Page Object Model (POM) design pattern
✔ Use Python OOPS principles (classes, inheritance, abstraction)
✔ Use Selenium WebDriver with Explicit Waits
✔ Handle Selenium exceptions properly:
    - TimeoutException
    - NoSuchElementException
    - ElementNotInteractableException
    - ElementClickInterceptedException

---------------------------------------------------------------------
TEST OUTPUT:

✔ Pytest-based execution
✔ HTML report generation required
✔ Separate Positive and Negative test cases
✔ Proper logging and screenshot capture on failure

---------------------------------------------------------------------
END OF SPECIFICATION
=====================================================================
"""

import time

import pytest
from pages.dashboard_page import DashboardPage

# Page Objects
from pages.login_page import LoginPage

# Selenium Exceptions
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)

# Utilities
from utils.config_reader import Config
from utils.logger import get_logger
from utils.screenshot import ScreenshotManager

# ============================================================================== #
#                               LOGGER CONFIGURATION                             #
# ============================================================================== #

# Create module-level logger
log = get_logger(__name__)

# ============================================================================== #
#                               TEST CONFIGURATION                               #
# ============================================================================== #

# Read values from config.ini
config = Config()

# Valid credentials
VALID_EMAIL = config.get_config(
    "LOGIN CREDENTIALS",
    "valid_email",
)

VALID_PASSWORD = config.get_config(
    "LOGIN CREDENTIALS",
    "valid_password",
)

# Dummy credentials for field validation
DUMMY_EMAIL = config.get_config(
    "LOGIN CREDENTIALS",
    "dummy_email",
)

DUMMY_PASSWORD = config.get_config(
    "LOGIN CREDENTIALS",
    "dummy_password",
)

# Invalid credentials
INVALID_EMAIL = config.get_config(
    "LOGIN CREDENTIALS",
    "invalid_email",
)

INVALID_PASSWORD = config.get_config(
    "LOGIN CREDENTIALS",
    "invalid_password",
)

# Generic framework settings
PAGE_LOAD_WAIT = int(config.get_config("DEFAULT", "page_load_wait"))

BLANK_SPACES = config.get_config(
    "DEFAULT",
    "blank_spaces",
)


# ============================================================================== #
#                  TEST GROUP A — SUCCESSFUL LOGIN VALIDATIONS                   #
# ============================================================================== #


class TestSuccessfulLogin:
    """
    OOPS Class: Groups all positive login tests.
    Validates the full happy-path login flow.
    """

    def test_positive_valid_login_redirects_away_from_signin(self, login_page, driver):
        """
        POSITIVE — Valid credentials redirect user away from login page.

        Scenario : Enter valid email + password → click Login.
        Expected : URL no longer contains 'login'.
        Validates : Authentication succeeds and navigation to dashboard occurs.
        """

        # Initialize screenshot manager
        sm = ScreenshotManager(driver)

        # Log test start
        log.info("TEST START: " "test_positive_valid_login_redirects_away_from_signin")

        try:
            # Validate config values before test execution
            config.validate()

            # Perform login
            log.info(f"Logging in with valid credentials: " f"{VALID_EMAIL!r}")

            login_page.login(
                VALID_EMAIL,
                VALID_PASSWORD,
            )

            # Wait for page navigation
            time.sleep(PAGE_LOAD_WAIT)

            # Capture current URL
            current_url = login_page.get_current_url()

            log.info(f"Post-login URL: {current_url}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert "login" not in current_url, (
                f"\nFAIL: Still on login page after valid login."
                f"\nURL: {current_url}"
            )

            log.info("PASS: Valid login redirected to dashboard.")

        except (AssertionError, TimeoutException) as e:

            # Capture screenshot on failure
            sm.take_screenshot("positive_valid_login_redirect")

            # Log failure
            log.error(f"FAIL: {e}")

            # Mark test as failed
            pytest.fail(str(e))

    def test_positive_dashboard_accessible_after_login(
        self,
        login_page,
        driver,
    ):
        """
        POSITIVE — Dashboard is accessible after successful login.

        Scenario : Login with valid credentials.
        Expected : DashboardPage.is_logged_in() returns True.
        """
        # Initialize screenshot manager
        sm = ScreenshotManager(driver)

        # Log test start
        log.info("TEST START: " "test_positive_dashboard_accessible_after_login")

        try:
            # Validate config values from env variables are mapped
            config.validate()

            # Login with valid credentials
            login_page.login(
                VALID_EMAIL,
                VALID_PASSWORD,
            )

            # Wait for page load
            time.sleep(PAGE_LOAD_WAIT)

            # Create dashboard page object
            dashboard = DashboardPage(driver)

            # ============================================================= #
            # HANDLE OPTIONAL POPUP
            # ============================================================= #

            if dashboard.is_new_launch_alert_popup_displayed():
                log.info("New launch alert popup detected.")

                dashboard.close_new_launch_alert_popup()

            # ============================================================= #
            # VALIDATE DASHBOARD ACCESS
            # ============================================================= #

            logged_in = dashboard.is_logged_in()

            log.info(f"Dashboard accessible: {logged_in}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert logged_in, (
                f"\nFAIL: Dashboard not accessible "
                f"after valid login."
                f"\nURL: {dashboard.get_current_url()}"
            )

            log.info("PASS: Dashboard accessible after login.")

        except (AssertionError, TimeoutException) as e:

            # Take screenshot on failure
            sm.take_screenshot("positive_dashboard_accessible")

            log.error(f"FAIL: {e}")

            pytest.fail(str(e))

        finally:
            # ============================================================= #
            # CLEANUP
            # ============================================================= #

            # Logout after test execution
            dashboard.logout()


# ============================================================================== #
#                          TEST GROUP B — UNSUCCESSFUL LOGIN                     #
# ============================================================================== #


class TestUnsuccessfulLogin:
    """
    OOPS Class: Groups all negative login tests.
    Validates the system correctly rejects bad credentials.
    """

    def test_negative_invalid_credentials_stay_on_login_page(
        self,
        login_page,
        driver,
    ):
        """
        NEGATIVE — Invalid email + wrong password stays on login page.

        Scenario : Submit unregistered email + wrong password.
        Expected : URL still contains 'login'.
        """

        # Initialize screenshot manager
        sm = ScreenshotManager(driver)

        log.info("TEST START: " "test_negative_invalid_credentials_stay_on_login_page")

        try:
            # Attempt invalid login
            log.info(f"Attempting invalid login: " f"{INVALID_EMAIL!r}")

            login_page.login(
                INVALID_EMAIL,
                INVALID_PASSWORD,
            )

            # Wait for response
            time.sleep(PAGE_LOAD_WAIT)

            # Fetch current URL
            current_url = login_page.get_current_url()

            log.info(f"URL after invalid login: " f"{current_url}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert login_page.is_on_login_page(), (
                f"\nFAIL: Navigated away with invalid credentials."
                f"\nURL: {current_url}"
            )

            log.info("PASS: Invalid credentials correctly blocked.")

        except (AssertionError, TimeoutException) as e:

            # Capture failure screenshot
            sm.take_screenshot("negative_invalid_credentials")

            log.error(f"FAIL: {e}")

            pytest.fail(str(e))

    def test_negative_empty_credentials_stay_on_login_page(self, login_page, driver):
        """
        NEGATIVE — Empty fields must not submit or navigate away.

        Scenario : Click Sign in button without any credentials.
        Expected : Stays on login page.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_negative_empty_credentials_stay_on_login_page")

        try:
            log.info("Submitting login form with empty credentials.")
            login_page.login("", "")
            time.sleep(1)

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert login_page.is_on_login_page(), (
                f"\nFAIL: Empty form navigated away from login."
                f"\n  URL: {login_page.get_current_url()}"
            )
            log.info("PASS: Empty credentials correctly blocked.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("negative_empty_credentials")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_valid_email_wrong_password(self, login_page, driver):
        """
        NEGATIVE — Correct email + wrong password must not log in.

        Scenario : Use valid email but wrong password.
        Expected : Stays on login page.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_negative_valid_email_wrong_password")

        try:
            config.validate()
            log.info(f"Login: email={VALID_EMAIL!r}, password=WRONG")
            login_page.login(VALID_EMAIL, INVALID_PASSWORD)
            time.sleep(PAGE_LOAD_WAIT)

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert login_page.is_on_login_page(), (
                f"\nFAIL: Logged in with wrong password."
                f"\n  URL: {login_page.get_current_url()}"
            )
            log.info("PASS: Correct email + wrong password blocked.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("negative_wrong_password")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_whitespace_credentials_blocked(self, login_page, driver):
        """
        NEGATIVE — Whitespace-only credentials must not log in.

        Scenario : Enter spaces in both fields and submit.
        Expected : Stays on login page.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_negative_whitespace_credentials_blocked")

        try:
            log.info("Submitting with whitespace-only credentials.")
            login_page.login(BLANK_SPACES, BLANK_SPACES)
            time.sleep(1)

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert login_page.is_on_login_page(), (
                f"\nFAIL: Whitespace credentials allowed login."
                f"\n  URL: {login_page.get_current_url()}"
            )
            log.info("PASS: Whitespace credentials correctly blocked.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("negative_whitespace_credentials")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))


# ============================================================================== #
#           TEST GROUP C — VALIDATE USERNAME & PASSWORD INPUT BOXES              #
# ============================================================================== #


class TestInputFields:
    """
    OOPS Class: Groups all input field validation tests.
    """

    def test_positive_email_field_visible_and_enabled(self, login_page, driver):
        """
        POSITIVE — Email field is visible and enabled.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_email_field_visible_and_enabled")

        try:
            displayed = login_page.is_email_field_displayed()
            enabled = login_page.is_email_field_enabled()

            log.info(f"Email field — displayed={displayed}, enabled={enabled}")

            # ============================================================= #
            # ASSERTIONS
            # ============================================================= #

            assert displayed, "FAIL: Email field not visible."
            assert enabled, "FAIL: Email field not enabled."
            log.info("PASS: Email field is visible and enabled.")

        except (AssertionError, TimeoutException, NoSuchElementException) as e:
            sm.take_screenshot("positive_email_field_visible")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_positive_password_field_visible_and_enabled(self, login_page, driver):
        """
        POSITIVE — Password field is visible and enabled.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_password_field_visible_and_enabled")

        try:
            displayed = login_page.is_password_field_displayed()
            enabled = login_page.is_password_field_enabled()

            log.info(f"Password field — displayed={displayed}, enabled={enabled}")

            # ============================================================= #
            # ASSERTIONS
            # ============================================================= #

            assert displayed, "FAIL: Password field not visible."
            assert enabled, "FAIL: Password field not enabled."
            log.info("PASS: Password field is visible and enabled.")

        except (AssertionError, TimeoutException, NoSuchElementException) as e:
            sm.take_screenshot("positive_password_field_visible")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_positive_email_field_accepts_input(self, login_page, driver):
        """
        POSITIVE — Email field accepts and retains typed text.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_email_field_accepts_input")

        try:
            login_page.enter_email(DUMMY_EMAIL)
            value = login_page.get_email_field_value()
            log.info(f"Email field value after input: {value!r}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert value == DUMMY_EMAIL, (
                f"\nFAIL: Email field value mismatch."
                f"\n  Expected : {DUMMY_EMAIL!r}"
                f"\n  Actual   : {value!r}"
            )
            log.info("PASS: Email field accepts and retains typed input.")

        except (AssertionError, ElementNotInteractableException) as e:
            sm.take_screenshot("positive_email_accepts_input")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_positive_password_field_accepts_input(self, login_page, driver):
        """
        POSITIVE — Password field accepts and retains typed text.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_password_field_accepts_input")

        try:
            login_page.enter_password(DUMMY_PASSWORD)
            value = login_page.get_password_field_value()
            log.info("Password field has value (length masked).")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert value == DUMMY_PASSWORD, f"\nFAIL: Password field value mismatch."
            log.info("PASS: Password field accepts and retains typed input.")

        except (AssertionError, ElementNotInteractableException) as e:
            sm.take_screenshot("positive_password_accepts_input")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))


# ============================================================================== #
#                       TEST GROUP D — VALIDATE SUBMIT->'SIGN IN' BUTTON                    #
# ============================================================================== #


class TestSubmitButton:
    """
    OOPS Class: Groups all submit button validation tests.
    """

    def test_positive_submit_button_visible_and_enabled(self, login_page, driver):
        """
        POSITIVE — Login button is visible and enabled after filling fields.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_submit_button_visible_and_enabled")

        try:
            login_page.enter_email(DUMMY_EMAIL)
            login_page.enter_password(DUMMY_PASSWORD)

            displayed = login_page.is_signin_button_displayed()
            enabled = login_page.is_signin_button_enabled()

            log.info(
                f"Login -> Sign in button — displayed={displayed}, enabled={enabled}"
            )

            # ============================================================= #
            # ASSERTIONS
            # ============================================================= #

            assert displayed, "FAIL: Login -> Sign in button not visible."
            assert enabled, "FAIL: Login -> Sign in button not enabled."
            log.info("PASS: Login -> Sign in button is visible and enabled.")

        except (AssertionError, TimeoutException, NoSuchElementException) as e:
            sm.take_screenshot("positive_submit_visible_enabled")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_positive_submit_valid_credentials_succeeds(self, login_page, driver):
        """
        POSITIVE — Submit with valid credentials navigates away from login.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_submit_valid_credentials_succeeds")

        try:
            config.validate()
            login_page.enter_email(VALID_EMAIL)
            login_page.enter_password(VALID_PASSWORD)
            login_page.click_signin_button()
            time.sleep(PAGE_LOAD_WAIT)

            current_url = login_page.get_current_url()
            log.info(f"URL after submit: {current_url}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert "login" not in current_url, (
                f"\nFAIL: Submit did not navigate away from login."
                f"\n  URL: {current_url}"
            )
            log.info("PASS: Submit with valid credentials succeeded.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("positive_submit_valid_credentials")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_submit_empty_fields_stays_on_page(self, login_page, driver):
        """
        NEGATIVE — Submit with empty fields stays on login.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_negative_submit_empty_fields_stays_on_page")

        try:
            log.info("Clicking Submit with all fields empty.")
            login_page.click_signin_button()
            time.sleep(1)

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert login_page.is_on_login_page(), (
                f"\nFAIL: Empty submit left login page."
                f"\n  URL: {login_page.get_current_url()}"
            )
            log.info("PASS: Empty submit correctly stayed on login page.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("negative_submit_empty_fields")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_submit_invalid_credentials_blocked(self, login_page, driver):
        """
        NEGATIVE — Submit with invalid credentials keeps user on login.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_negative_submit_invalid_credentials_blocked")

        try:
            login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
            time.sleep(PAGE_LOAD_WAIT)

            email_err = login_page.get_email_error_text()
            pswd_err = login_page.get_password_error_text()

            if email_err:
                log.info(f"Email error: {email_err!r}")
            if pswd_err:
                log.info(f"Password error: {pswd_err!r}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert login_page.is_on_login_page(), (
                f"\nFAIL: Invalid credentials bypassed auth."
                f"\n  URL: {login_page.get_current_url()}"
            )
            log.info("PASS: Invalid credentials submit correctly blocked.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("negative_submit_invalid_credentials")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_submit_empty_email_field_and_password_field_displays_error_msg(
        self, login_page, driver
    ):
        """
        NEGATIVE — Submit with Empty Email field and Password field displays appropriate error messages under password field
        """

        sm = ScreenshotManager(driver)
        log.info(
            "TEST START: test_negative_submit_empty_email_field_and_password_field_displays_error_msg"
        )

        try:
            login_page.enter_email("")
            value_email = login_page.get_email_field_value()
            log.info(f"Email field value after input: {value_email!r}")

            login_page.enter_password("")
            value_pswd = login_page.get_password_field_value()
            log.info("Password field has value (length masked).")

            login_page.click_signin_button()

            email_err = login_page.get_email_error_text() or "no error value"
            pswd_err = login_page.get_password_error_text() or "no error value"

            if email_err:
                log.info(f"Email error: {email_err!r}")
            if pswd_err:
                log.info(f"Password error: {pswd_err!r}")

            # ============================================================= #
            # ASSERTIONS
            # ============================================================= #

            # Validate email field empty
            assert value_email.strip() == "", "Email field should be empty"

            # Validate password field empty
            assert value_pswd.strip() == "", "Password field should be empty"

            # Validate email error displayed
            assert email_err.strip() != "", "Email error message not displayed"

            # Validate password error displayed
            assert pswd_err.strip() != "", "Password error message not displayed"

            # Validate proper error content
            assert (
                "email" in pswd_err.lower() and "password" in pswd_err.lower()
            ), f"Unexpected password error: {pswd_err}"

            log.info(
                "PASS: Submit with Empty Email field and Password field displays appropriate error messages under password field."
            )

        except Exception as e:

            sm.take_screenshot("empty_email_password_validation_failure")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_submit_empty_email_field_and_filled_password_field_displays_error_msg(
        self, login_page, driver
    ):
        """
        NEGATIVE — Submit with Empty Email field and filled Password field displays appropriate error messages under email field
        """

        sm = ScreenshotManager(driver)
        log.info(
            "TEST START: test_negative_submit_empty_email_field_and_filled_password_field_displays_error_msg"
        )

        try:
            login_page.enter_email("")
            value_email = login_page.get_email_field_value()
            log.info(f"Email field value after input: {value_email!r}")

            login_page.enter_password(DUMMY_PASSWORD)
            value_pswd = login_page.get_password_field_value()
            log.info("Password field has value (length masked).")

            login_page.click_signin_button()

            email_err = login_page.get_email_error_text() or "no error value"
            pswd_err = login_page.get_password_error_text() or "no error value"

            if email_err:
                log.info(f"Email error: {email_err!r}")
            if pswd_err:
                log.info(f"Password error: {pswd_err!r}")

            # ============================================================= #
            # ASSERTIONS
            # ============================================================= #

            # Validate email field empty
            assert value_email.strip() == "", "Email field should be empty"

            # Validate password field not empty
            assert value_pswd.strip() != "", "Password field should not be empty"

            # Validate email error displayed
            assert email_err.strip() != "", "Email error message not displayed"

            # Validate password error displayed
            assert pswd_err.strip() != "", "Password error message not displayed"

            # Validate proper error content
            assert "email" in email_err.lower(), f"Unexpected email error: {email_err}"

            log.info(
                "PASS: Submit with Empty Email field and filled Password field displays appropriate error messages under email field."
            )

        except Exception as e:

            sm.take_screenshot("empty_email_filled_password_validation_failure")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_submit_filled_email_field_and_empty_password_field_displays_error_msg(
        self, login_page, driver
    ):
        """
        NEGATIVE — Submit with filled Email field and empty Password field displays appropriate error messages under password field
        """

        sm = ScreenshotManager(driver)
        log.info(
            "TEST START: test_negative_submit_filled_email_field_and_empty_password_field_displays_error_msg"
        )

        try:
            login_page.enter_email(DUMMY_EMAIL)
            value_email = login_page.get_email_field_value()
            log.info(f"Email field value after input: {value_email!r}")

            login_page.enter_password("")
            value_pswd = login_page.get_password_field_value()
            log.info("Password field has value (length masked).")

            login_page.click_signin_button()

            email_err = login_page.get_email_error_text() or "no error value"
            pswd_err = login_page.get_password_error_text() or "no error value"

            if email_err:
                log.info(f"Email error: {email_err!r}")
            if pswd_err:
                log.info(f"Password error: {pswd_err!r}")

            # ============================================================= #
            # ASSERTIONS
            # ============================================================= #

            # Validate email field empty
            assert value_email.strip() != "", "Email field should not be empty"

            # Validate password field empty
            assert value_pswd.strip() == "", "Password field should be empty"

            # Validate email error displayed
            assert email_err.strip() != "", "Email error message not displayed"

            # Validate password error displayed
            assert pswd_err.strip() != "", "Password error message not displayed"

            # Validate proper error content
            assert (
                "password" in pswd_err.lower()
            ), f"Unexpected password error: {pswd_err}"

            log.info(
                "PASS: Submit with filled Empty Email field and empty Password field displays appropriate error messages under password field."
            )

        except Exception as e:

            sm.take_screenshot("filled_email_empty_password_validation_failure")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))


# ============================================================================== #
#               TEST GROUP E — VALIDATE LOGOUT BUTTON FUNCTIONALITY              #
# ============================================================================== #


class TestLogout:
    """
    OOPS Class: Groups all logout validation tests.
    Uses logged_in_dashboard fixture — starts each test already authenticated.
    """

    def test_positive_logout_redirects_to_login_page(self, logged_in_dashboard, driver):
        """
        POSITIVE — Logout redirects the user back to the login page.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_logout_redirects_to_login_page")

        try:
            pre_url = logged_in_dashboard.get_current_url()
            log.info(f"Pre-logout URL: {pre_url}")

            if logged_in_dashboard.is_new_launch_alert_popup_displayed():
                log.info("New launch alert popup detected.")
                logged_in_dashboard.close_new_launch_alert_popup()

            logged_in_dashboard.logout()
            time.sleep(PAGE_LOAD_WAIT)

            post_url = logged_in_dashboard.get_current_url()
            log.info(f"Post-logout URL: {post_url}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert logged_in_dashboard.is_logged_out(), (
                f"\nFAIL: Logout did not redirect to login." f"\n  URL: {post_url}"
            )
            log.info("PASS: Logout correctly redirected to login page.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("positive_logout_redirect")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_positive_dashboard_inaccessible_after_logout(
        self, logged_in_dashboard, driver
    ):
        """
        POSITIVE — Dashboard is inaccessible after logout (session destroyed).
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_positive_dashboard_inaccessible_after_logout")

        try:
            dashboard_url = logged_in_dashboard.get_current_url()
            log.info(f"Dashboard URL before logout: {dashboard_url}")

            if logged_in_dashboard.is_new_launch_alert_popup_displayed():
                log.info("New launch alert popup detected.")
                logged_in_dashboard.close_new_launch_alert_popup()

            logged_in_dashboard.logout()
            time.sleep(PAGE_LOAD_WAIT)

            # Attempt to navigate back to the dashboard
            log.info("Attempting to revisit dashboard URL after logout.")
            logged_in_dashboard.open(dashboard_url)
            time.sleep(PAGE_LOAD_WAIT)

            final_url = logged_in_dashboard.get_current_url()
            log.info(f"URL after revisit attempt: {final_url}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert "login" in final_url or dashboard_url not in final_url, (
                f"\nFAIL: Dashboard still accessible after logout."
                f"\n  URL: {final_url}"
            )
            log.info("PASS: Dashboard inaccessible after logout.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("positive_dashboard_inaccessible")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))

    def test_negative_session_cleared_after_logout(self, logged_in_dashboard, driver):
        """
        NEGATIVE — User must NOT still be logged in after logout.
        """
        sm = ScreenshotManager(driver)
        log.info("TEST START: test_negative_session_cleared_after_logout")

        try:
            log.info(
                f"is_logged_in before logout: {logged_in_dashboard.is_logged_in()}"
            )

            if logged_in_dashboard.is_new_launch_alert_popup_displayed():
                log.info("New launch alert popup detected.")
                logged_in_dashboard.close_new_launch_alert_popup()

            logged_in_dashboard.logout()
            time.sleep(PAGE_LOAD_WAIT)

            still_logged_in = logged_in_dashboard.is_logged_in()
            log.info(f"is_logged_in after logout: {still_logged_in}")

            # ============================================================= #
            # ASSERTION
            # ============================================================= #

            assert not still_logged_in, (
                f"\nFAIL: User still logged in after logout."
                f"\n  URL: {logged_in_dashboard.get_current_url()}"
            )
            log.info("PASS: Session correctly cleared after logout.")

        except (AssertionError, TimeoutException) as e:
            sm.take_screenshot("negative_session_cleared")
            log.error(f"FAIL: {e}")
            pytest.fail(str(e))
