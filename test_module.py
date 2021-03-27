import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    @pytest.fixture(autouse=True)
    def start_from_home_page(self):
        self.driver.get("https://www.macmillan.pl")
        try:
            if self.driver.find_element_by_id("rodo-accept-all-cookies").is_displayed():
                self.driver.find_element_by_id("rodo-accept-all-cookies").click()
        except:
            pass
        
    # Check if cookies have been accepted
    def test_accept_cookies(self):
        assert self.driver.find_element_by_id("logo").is_displayed() == True, "Cookies test fail!"

    # Search for representatives in given provinces and collect their names
    # Check if the found values match the expected ones
    def test_find_representatives(self):
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
    def test_products_availability(self):
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
        assert results == expected, "Products availability test fail!"

    # Test searches for given products' MEN numbers
    # The dict with product:men_number pairs is created and compared to the expected dict
    def test_find_men_number(self):
        products = ["Tiger & Friends 2", "Tiger 1", "All Clear - klasa 7", "Evolution plus - klasa 4"]
        actions = ActionChains(self.driver)
        menu_item = self.driver.find_element_by_xpath('//*[@id="top"]/div[3]/nav/ul/li[3]/a')
        self.driver.implicitly_wait(1)
        submenu_item = self.driver.find_element_by_xpath('//*[@id="top"]/div[3]/nav/ul/li[3]/ul/li[6]/a')
        actions.move_to_element(menu_item).perform()
        actions.pause(1)
        submenu_item.click()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        tbodies = soup.find_all("tbody")
        trs = sum((tbody.find_all("tr") for tbody in tbodies), [])
        results = {}
        for product in products:
            for tr in trs:
                try:
                    title = tr.find("span", class_="level").text.strip()
                    if product == title:
                        men = tr.find(class_="men").text.strip()
                        results[title] = men
                except:
                    pass
        expected = {
            "Tiger & Friends 2": "1051/2/2020",
            "Tiger 1": "836/1/2017",
            "All Clear - klasa 7": "848/1/2017",
            "Evolution plus - klasa 4": "856/1/2017"
        }
        assert results == expected, "Finding men numbers test fail!"
                    

if __name__ == "__main__":
    pytest.main()