import time
from sysconfig import get_config_vars

import pytest

from drivers.driver_factory import DriverFactory
from utils.config_reader import Config
from utils.logger import get_logger
from utils.screenshot import ScreenshotManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# Module-level logger for conftest hooks
log = get_logger("conftest")

# Constants whose value is read from config.ini file
config = Config()
BROWSER = config.get_config("DEFAULT", "browser")
BASE_URL = config.get_config("URL", "base_url")
PAGE_LOAD_WAIT = int(config.get_config("DEFAULT", "page_load_wait"))
VALID_EMAIL = config.get_config("LOGIN CREDENTIALS", "valid_email")
VALID_PASSWORD = config.get_config("LOGIN CREDENTIALS", "valid_password")

# ══════════════════════════════════════════════════════════════════════════════ #
#  FIXTURE — WebDriver                                                       #
# ══════════════════════════════════════════════════════════════════════════════ #

@pytest.fixture(scope="function")
def driver():
    log.info("=" * 70)
    log.info(f"Launching {BROWSER.capitalize()} browser for test.")

    driver = DriverFactory.get_driver(BROWSER)
    log.info("Browser launched and maximised.")

    yield driver        # ← test runs here

    log.info("Quitting browser after test.")
    DriverFactory.quit_driver()
    log.info("=" * 70)


# ══════════════════════════════════════════════════════════════════════════════ #
#  FIXTURE — Login Page                                                          #
# ══════════════════════════════════════════════════════════════════════════════ #

@pytest.fixture(scope="function")
def login_page(driver):
    """
    Returns a LoginPage instance already navigated to the login URL.
    Use in tests that start on the login page.
    """
    log.info("Fixture: opening login page.")
    page = LoginPage(driver)
    page.open_login_page()
    time.sleep(PAGE_LOAD_WAIT)
    log.info(f"Fixture: login page ready. URL={driver.current_url}")
    return page


# ══════════════════════════════════════════════════════════════════════════════ #
#  FIXTURE — Logged-In Dashboard                                                 #
# ══════════════════════════════════════════════════════════════════════════════ #

@pytest.fixture(scope="function")
def logged_in_dashboard(driver):
    """
    Returns a DashboardPage after completing a valid login.
    Use in tests that require the user to already be authenticated.
    Validates credentials are set via env vars before proceeding.
    """
    log.info("Fixture: performing login to reach dashboard.")
    #Config.validate()   # Guard: crash early if env vars not set

    login = LoginPage(driver)
    login.open_login_page()
    time.sleep(PAGE_LOAD_WAIT)

    login.login(VALID_EMAIL, VALID_PASSWORD)
    time.sleep(PAGE_LOAD_WAIT)

    log.info(f"Fixture: logged in. URL={driver.current_url}")
    return DashboardPage(driver)


# ══════════════════════════════════════════════════════════════════════════════ #
#  HOOK — Screenshot on Failure                                                  #
# ══════════════════════════════════════════════════════════════════════════════ #

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after every test phase (setup / call / teardown).

    When a test FAILS during the 'call' phase:
      1. Captures a screenshot of the current browser state
      2. Attaches the screenshot path to the pytest HTML report
      3. Logs the failure with full test name and screenshot path

    The 'tryfirst=True' ensures this hook runs before pytest-html's own
    report generation so the screenshot attachment is included.
    """
    # ── Let the test run and collect its outcome ──────────────────────────────
    outcome = yield
    report  = outcome.get_result()

    # ── Only act on FAILURES in the test CALL phase ───────────────────────────
    # 'call' phase = the actual test body (not setup/teardown)
    if report.when == "call" and report.failed:

        # ── Retrieve the driver fixture from the test's fixture request ────────
        # item.funcargs contains all fixtures available to this test
        driver = item.funcargs.get("driver")

        if driver is None:
            log.warning(f"No 'driver' fixture found for test: {item.nodeid}")
            return

        # ── Take the screenshot ────────────────────────────────────────────────
        sm          = ScreenshotManager(driver)
        test_name   = item.nodeid.replace("::", "_").replace("/", "_")
        screenshot  = sm.take_screenshot(test_name)

        # ── Log the failure ────────────────────────────────────────────────────
        log.error(f"TEST FAILED: {item.nodeid}")
        log.error(f"Current URL at failure: {driver.current_url}")

        if screenshot:
            log.error(f"Screenshot captured: {screenshot}")
        else:
            log.warning("Screenshot could not be saved.")

        # ── Attach screenshot to pytest-html report ────────────────────────────
        # pytest-html reads extras from item._report_sections or via plugin extras
        if screenshot:
            try:
                # pytest-html extras — attach image inline in the HTML report
                from pytest_html import extras as html_extras
                extra = getattr(report, "extras", [])
                extra.append(html_extras.image(screenshot, name="Failure Screenshot"))
                report.extras = extra
                log.info("Screenshot attached to HTML report.")
            except ImportError:
                # pytest-html not installed — skip attachment, path already logged
                log.debug("pytest-html not available; screenshot path logged only.")
            except Exception as e:
                log.warning(f"Could not attach screenshot to report: {e}")


# ══════════════════════════════════════════════════════════════════════════════ #
#  HOOK — Log Test Start and End                                                 #
# ══════════════════════════════════════════════════════════════════════════════ #

def pytest_runtest_logreport(report):
    """
    Logs the outcome of each test phase to the log file.
    Provides a clean pass/fail/skip summary for every test.
    """
    if report.when == "call":
        if report.passed:
            log.info(f"PASSED  : {report.nodeid}")
        elif report.failed:
            log.error(f"FAILED  : {report.nodeid}")
        elif report.skipped:
            log.warning(f"SKIPPED : {report.nodeid}")
