# GUVI_HCL_TASK14_AutomationPOMFramework_May2026
GUVI HCL TASK 14 - Automation POM Framework

The current repository contains python codes to the questions mentioned in HCL GUVI Python Task 14 - https://docs.google.com/document/d/11Q4lIy7gNieDvBMq_9fCx9h0qfJ7E2OF0a4ruyK1aJA/edit?tab=t.0

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
