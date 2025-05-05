from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional


def init_selenium(options: Optional[Options] = None) -> WebDriver:
    """
    Initializes a Selenium WebDriver instance with the specified options.
    Args:
        options (Optional[Options]): A Selenium Options object to configure the WebDriver.
                                     If not provided, a default Options object is created
                                     with the "--headless" argument for headless operation.
    Returns:
        WebDriver: An instance of Selenium WebDriver configured with the provided or default options.
    """

    if not options:
        options = Options()
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def wait_page_to_be_loaded(driver: WebDriver, timeout: int = 10):
    """
    Waits for an  element on a webpage with class "Story_title" to be loaded within a given timeout period.
    Args:
        driver (WebDriver): The Selenium WebDriver instance controlling the browser.
        timeout (int, optional): The maximum time to wait for the element to be present, in seconds. Defaults to 10.
    Raises:
        TimeoutException: If the element is not found within the specified timeout.
    Notes:
        This function waits for an element with the class name "Story_title" to be present on the page.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Story_title"))
        )
    except:
        print("Timeout.")


def scrap_page(driver: WebDriver) -> list[str]:
    """
    Scrapes a webpage using the provided WebDriver instance and extracts data
    from elements with the class name "Story_data". Each extracted element is
    processed to retrieve and preprocess its title.
    Args:
        driver (WebDriver): The Selenium WebDriver instance used to interact
                            with the webpage.
    Returns:
        list[str]: A list of titles extracted
    Notes:
        - The function waits for the page to be fully loaded before scraping.
        - If an element does not contain the required data or an error occurs
          during processing, it is skipped.
        - The `spacy_preprocessor` function is used to preprocess the title
    """
    wait_page_to_be_loaded(driver)
    elements = driver.find_elements(By.CLASS_NAME, "Story_data")
    page_data = []
    for elem in elements:
        try:
            title = elem.find_element(By.CLASS_NAME, "Story_title").text
            page_data.append(title)
        except:
            continue
    return page_data


def scrap_from_algolia() -> list[str]:
    """
    Retrieves a DataFrame containing news articles scraped from Algolia.
    This function initializes a Selenium WebDriver, navigates through multiple pages
    of the Algoliawebsite, and collects article data. The collected data is then
    returned as a Polars DataFrame.
    Returns:
        list[str]: A list of str extracted
    """
    url = "https://hn.algolia.com"
    driver = init_selenium()
    driver.get(url)
    wait_page_to_be_loaded(driver)

    all_data = []

    while True:
        page_data = scrap_page(driver)
        all_data.extend(page_data)

        try:
            next_button = driver.find_element(
                By.XPATH,
                "//li[contains(@class, 'Pagination_item-current')]/following-sibling::li[1]/button",
            )
            next_button.click()
            wait_page_to_be_loaded(driver)
        except:
            print("No more pages.")
            break

    driver.quit()

    return all_data
