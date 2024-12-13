from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import json
from selenium.common import WebDriverException

class UrbanRoutesAutomation:
    def __init__(self, driver):
        self.driver = driver

    # Métodos
    class UrbanRoutesPage:
        from_field = (By.ID, 'from')
        to_field = (By.ID, 'to')
        taxi_button = (By.XPATH, "//button[@type='button' and contains(@class, 'button round') and text()='Pedir un taxi']")
        comfort_button = (By.XPATH, ".//*[text()='Comfort']")
        phone_area_button = (By.XPATH, "//div[contains(@class, 'np-text') and text()='Número de teléfono']")
        phone_number_field = (By.ID, "phone")
        next_button = (By.XPATH, ".//div[@class='buttons']/button[@class='button full']")
        comment_space = (By.CSS_SELECTOR, "#comment")
        ask_blanket_button = (By.XPATH, "//div[@class='r-sw-container']/div[@class='r-sw']/div[@class='switch']")
        ice_cream_plus_button = (By.CSS_SELECTOR, ".counter-plus")
        ice_cream_count = (By.CSS_SELECTOR, ".counter-value")
        final_button = (By.CSS_SELECTOR, ".smart-button-secondary")

        def __init__(self, driver):
            self.driver = driver

        def set_from(self, from_address):
            self.driver.find_element(*self.from_field).send_keys(from_address)

        def set_to(self, to_address):
            self.driver.find_element(*self.to_field).send_keys(to_address)

        def return_from(self):
            return self.driver.find_element(*self.from_field).get_property('value')

        def return_to(self):
            return self.driver.find_element(*self.to_field).get_property('value')

        def set_route(self, from_address, to_address):
            self.set_from(from_address)
            self.set_to(to_address)

        def click_taxi_button(self):
            self.driver.find_element(*self.taxi_button).click()

        def click_phone_area_button(self):
            self.driver.find_element(*self.phone_area_button).click()

    class ComfortMethod:
        def __init__(self, driver):
            self.driver = driver

        def select_comfort(self):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comfort_button).click()

        def return_status_trip(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comfort_button).is_displayed()

    class AddPhoneNumber:
        def __init__(self, driver):
            self.driver = driver

        def write_phone_number(self, number):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.phone_number_field).send_keys(number)

        def post_number(self):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.next_button).click()

        def return_phone_number(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.phone_number_field).get_property('value')

        def send_phone_number(self, number):
            self.write_phone_number(number)
            self.post_number()

    class SendNewMessage:
        def __init__(self, driver):
            self.driver = driver

        def write_new_message(self, message):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comment_space).send_keys(message)

        def return_message(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comment_space).get_property('value')

    class AskBlanket:
        def __init__(self, driver):
            self.driver = driver

        def ask_blanket(self):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.ask_blanket_button).click()

        def return_status_blanket(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.ask_blanket_button).is_displayed()

    class IceCreamOrder:
        def __init__(self, driver):
            self.driver = driver

        def add_ice_cream(self):
            for i in range(2):
                plus_button = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.ice_cream_plus_button)
                self.driver.execute_script("arguments[0].scrollIntoView();", plus_button)
                WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".counter-plus")))
                plus_button.click()
                WebDriverWait(self.driver, 5).until(
                    lambda d: int(self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.ice_cream_count).text) == i + 1
                )

        def return_ice_cream_count(self):
            element = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.ice_cream_count)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.text

    class FinalButton:
        def __init__(self, driver):
            self.driver = driver

        def is_final_button_enabled(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.final_button).is_enabled()

    @staticmethod
    def retrieve_phone_code(driver) -> str:
        code = None
        for i in range(10):
            try:
                logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                        and 'api/v1/number?number' in log.get("message")]
                for log in reversed(logs):
                    message_data = json.loads(log)["message"]
                    body = driver.execute_cdp_cmd('Network.getResponseBody',
                                                  {'requestId': message_data["params"]["requestId"]})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
            except WebDriverException:
                time.sleep(1)
                continue
            if not code:
                raise Exception("No se encontró el código de confirmación del teléfono.\n"
                                "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
            return code
