import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Initialize webdriver along with chrome options. Each test in a class will be able to use the driver
# After the tests are performed, the driver will automatically close
@pytest.fixture(scope="class")
def webdriver(request):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome("./venv/chromedriver", options=chrome_options)
    request.cls.driver = driver
    yield driver
    driver.close()


@pytest.mark.usefixtures("webdriver")
class TestMacmillanUI:

    # This fixture will be run before each test - every single test starts from homepage
    @pytest.fixture()
    def start_from_home_page(self):
        self.driver.get("https://www.macmillan.pl")
        try:
            if self.driver.find_element_by_id("rodo-accept-all-cookies").is_displayed():
                self.driver.find_element_by_id("rodo-accept-all-cookies").click()
        except:
            pass
        
    # Check if cookies have been accepted
    def test_accept_cookies(self, start_from_home_page):
        assert self.driver.find_element_by_id("logo").is_displayed() == True, "Cookies test fail!"

    # Search for representatives in given provinces and collect their names
    # Check if the found values match the expected ones
    def test_find_representatives(self, start_from_home_page):
        provinces_to_test = ["lubelskie", "opolskie"]
        representatives = []
        self.driver.find_element_by_class_name("item-740").click()
        for province in provinces_to_test:
            self.driver.find_element_by_id("searchItem").send_keys(province)
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, '//*[@id="searchRForm"]/ul/li/a/strong').click()
            people = self.driver.find_element_by_class_name("people").find_elements_by_tag_name("h2")
            for person in people:
                representatives.append(person.text)
            self.driver.back()
        expected = ["Radosław Łosiewicz", "Grzegorz Gębala", "Marek Grygorowicz"]
        assert representatives == expected, "Find representatives test fail!"

    # Test the availability of the particular components of given products
    # Search the products' components and collect those with "Oprogramowanie tablicy interaktywnej" in their names
    # Compare found components with the expected ones
    def test_products_availability(self, start_from_home_page):
        main_tab = self.driver.current_window_handle
        products = ["Brainy klasa 5", "Bugs Team 3", "All Clear klasa 7"]
        self.driver.find_element_by_xpath('//*[@id="top"]/div[3]/nav/ul/li[6]/a').click()
        tabs = self.driver.window_handles
        for tab in tabs:
            if tab != main_tab:
                self.driver.switch_to.window(tab)
                break
        self.driver.implicitly_wait(1)
        results = []
        for product in products:
            self.driver.find_elements_by_id("query")[1].send_keys(product + "\n")
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            products_list = soup.find("div", {"id": "ajax_products_list"}).find_all("h2", {"class": "full-text"})
            for i in products_list:
                product_name = i.text.strip()
                if "Oprogramowanie tablicy interaktywnej" in product_name:
                    results.append(product_name)
            self.driver.back()
        expected = ["Brainy klasa 5 Oprogramowanie tablicy interaktywnej (reforma 2017)",\
            "Bugs Team 3 Oprogramowanie tablicy interaktywnej (reforma 2017)",\
            "All Clear klasa 7 Oprogramowanie tablicy interaktywnej (reforma 2017)"]
        assert results == expected

    def test_add_products_to_basket(self, start_from_home_page):
        # To be continued ...
        pass


if __name__ == "__main__":
    pytest.main()