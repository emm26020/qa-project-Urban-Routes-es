import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages import UrbanRoutesAutomation
from helpers import retrieve_phone_code

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
        comfort_method = UrbanRoutesAutomation.ComfortMethod(self.driver)
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(UrbanRoutesAutomation.UrbanRoutesPage.comfort_button))
        comfort_method.select_comfort()
        assert comfort_method.return_status_trip() == True, "La tarifa Comfort no fue seleccionada correctamente."

    def test_click_phone_area(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'np-text') and text()='Número de teléfono']")))
        route_page = UrbanRoutesAutomation.UrbanRoutesPage(self.driver)
        route_page.click_phone_area_button()

    def test_click_phone_area(self):
        """Prueba para hacer clic en el área de número de teléfono."""
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'np-text') and text()='Número de teléfono']")))
        route_page = UrbanRoutesAutomation.UrbanRoutesPage(self.driver)
        route_page.click_phone_area_button()

    def test_add_phone_number(self):
        phone_section = UrbanRoutesAutomation.AddPhoneNumber(self.driver)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(UrbanRoutesAutomation.UrbanRoutesPage.phone_area_button)
        )
        phone_section.send_phone_number(data.phone_number)
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable((By.ID, "code")))
        self.driver.find_element(By.ID, "code").send_keys(retrieve_phone_code(self.driver))  # Actualizado
        self.driver.find_element(By.XPATH, "//button[text()='Confirmar']").click()
        assert phone_section.return_phone_number() == data.phone_number, "El número de teléfono no coincide."

    def test_add_credit_card(self):
        add_card = UrbanRoutesAutomation.AddCreditCard(self.driver)

        # Hacer clic en el botón de metodo de pago
        add_card.click_payment_method_button()

        # Hacer clic en "Agregar tarjeta"
        add_card.click_add_card_button()

        # Ingresar detalles de la tarjeta
        add_card.enter_card_details(data.card_number, data.card_code)

        # Validar que la tarjeta se haya agregado correctamente
        try:
            payment_method_text = WebDriverWait(self.driver, 10).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, "pp-value-text"))
            )
            assert payment_method_text.text == "Tarjeta", "El método de pago no cambió a 'Tarjeta' tras agregar la tarjeta."
            print("La tarjeta fue agregada correctamente.")
        except Exception as e:
            print(f"Error al validar el cambio del método de pago: {e}")
            raise

    def test_write_message(self):
        message = data.message_for_driver
        write_message = UrbanRoutesAutomation.SendNewMessage(self.driver)
        write_message.write_new_message(message)
        assert write_message.return_message() == message

    def test_select_blanket(self):
        """Valida que el checkbox de manta se seleccione correctamente."""
        blanket_section = UrbanRoutesAutomation.AskBlanket(self.driver)
        blanket_section.ask_blanket()

        # Verifica que el checkbox está seleccionado
        assert blanket_section.return_status_blanket(), "La opción de manta no fue seleccionada correctamente."

    def test_add_ice_cream(self):
        ice_cream_section = UrbanRoutesAutomation.IceCreamOrder(self.driver)
        ice_cream_section.add_ice_cream()
        assert ice_cream_section.return_ice_cream_count() == "2", "No se agregaron 2 helados correctamente."

    def test_taxi_modal_is_displayed(self):
        """Valida si el modal para pedir un taxi se despliega correctamente."""
        # Hacer clic en el botón de reserva
        reserve_button = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.reserve_button)
        reserve_button.click()

        # Esperar a que el modal esté visible
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                UrbanRoutesAutomation.UrbanRoutesPage.order_taxi_modal_title
            )
        )

        # Validar que el modal está visible
        modal_title = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.order_taxi_modal_title)
        assert modal_title.is_displayed(), "El modal para pedir un taxi no se desplegó correctamente."
