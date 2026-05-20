from os import path, makedirs
from datetime import datetime

from utils.logger import get_logger


# Create logger for this file
log = get_logger(__name__)


class ScreenshotManager:
    """
    Handles screenshot capturing and saving.
    """

    # Folder where screenshots will be saved
    SCREENSHOTS_DIR = path.join(
        path.dirname(__file__),
        "..",
        "screenshots"
    )

    def __init__(self, driver):
        """
        Constructor.

        Args:
            driver: Selenium WebDriver instance
        """

        # Store driver object
        self.driver = driver

        # Create screenshots folder if not present
        makedirs(self.SCREENSHOTS_DIR, exist_ok=True)

        log.info("ScreenshotManager initialized")

    def take_screenshot(self, test_name):
        """
        Take screenshot and save it.

        Args:
            test_name (str): Name of the test

        Returns:
            str: Screenshot file path
        """

        # Create timestamp
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        # Replace invalid filename characters
        safe_name = test_name.replace(" ", "_")

        # Create screenshot file name
        filename = f"{safe_name}_{timestamp}.png"

        # Full file path
        filepath = path.join(
            self.SCREENSHOTS_DIR,
            filename
        )

        try:
            # Save screenshot
            self.driver.save_screenshot(filepath)

            log.info(
                f"Screenshot saved: {filepath}"
            )

            return filepath

        except Exception as e:

            # Log error if screenshot fails
            log.error(
                f"Unable to take screenshot: {e}"
            )

            return ""