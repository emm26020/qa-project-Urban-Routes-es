import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages import UrbanRoutesAutomation

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    def test_set_a_route(self):
        self.driver.get(data.urban_routes_url)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, "from")))
        route_page = UrbanRoutesAutomation.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        route_page.set_route(address_from, address_to)
        assert route_page.return_from() == address_from
        assert route_page.return_to() == address_to

    def test_click_taxi_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and contains(@class, 'button round') and text()='Pedir un taxi']")))
        route_page = UrbanRoutesAutomation.UrbanRoutesPage(self.driver)
        route_page.click_taxi_button()

    def test_select_comfort(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, ".//*[text()='Comfort']")))
        travel_method = UrbanRoutesAutomation.ComfortMethod(self.driver)
        travel_method.select_comfort()
        assert travel_method.return_status_trip() == True

    def test_click_phone_area(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'np-text') and text()='Número de teléfono']")))
        route_page = UrbanRoutesAutomation.UrbanRoutesPage(self.driver)
        route_page.click_phone_area_button()

    def test_select_phone_number(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, "phone")))
        send_phone = UrbanRoutesAutomation.AddPhoneNumber(self.driver)
        new_phone = data.phone_number
        send_phone.send_phone_number(new_phone)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, "code")))
        self.driver.find_element(By.ID, "code").send_keys(UrbanRoutesAutomation.retrieve_phone_code(self.driver))
        self.driver.find_element(By.XPATH, ".//*[text()='Confirmar']").click()
        assert send_phone.return_phone_number() == new_phone

    def test_write_message(self):
        message = data.message_for_driver
        write_message = UrbanRoutesAutomation.SendNewMessage(self.driver)
        write_message.write_new_message(message)
        assert write_message.return_message() == message

    def test_ask_for_blanket(self):
        blanket = UrbanRoutesAutomation.AskBlanket(self.driver)
        blanket.ask_blanket()
        assert blanket.return_status_blanket() == True

    def test_order_ice_cream(self):
        ice_cream = UrbanRoutesAutomation.IceCreamOrder(self.driver)
        ice_cream.add_ice_cream()
        assert ice_cream.return_ice_cream_count() == "2"

    def test_final_button_enabled(self):
        final_button = UrbanRoutesAutomation.FinalButton(self.driver)
        assert final_button.is_final_button_enabled() == True
