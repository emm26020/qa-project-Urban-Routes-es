from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import json
from selenium.common import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class UrbanRoutesAutomation:
    def __init__(self, driver):
        self.driver = driver

    # Métodos
    class UrbanRoutesPage:
        from_field = (By.ID, 'from')
        to_field = (By.ID, 'to')
        taxi_button = (
        By.XPATH, "//button[@type='button' and contains(@class, 'button round') and text()='Pedir un taxi']")
        comfort_button = (By.XPATH, ".//*[text()='Comfort']")
        comfort_active_card = (By.CSS_SELECTOR, ".tcard.active")  # Adición: Selección de tarjeta activa para Comfort
        comfort_title = (By.CLASS_NAME, 'tcard-title')  # Adición: Verificar texto Comfort en título
        phone_area_button = (By.XPATH, "//div[contains(@class, 'np-text') and text()='Número de teléfono']")
        phone_number_field = (By.ID, "phone")
        phone_displayed_text = (By.CLASS_NAME, 'np-text')  # Adición: Verificar número de teléfono mostrado
        next_button = (By.XPATH, ".//div[@class='buttons']/button[@class='button full']")
        comment_space = (By.CSS_SELECTOR, "#comment")
        checkbox_blanket = (By.CSS_SELECTOR, "input.switch-input")  # Localizador actualizado

        ask_blanket_button = (By.XPATH, "//div[@class='r-sw-container']/div[@class='r-sw']/div[@class='switch']")
        blanket_slider = (By.CSS_SELECTOR, "span.slider.round")
        ice_cream_plus_button = (By.CSS_SELECTOR, ".counter-plus")
        ice_cream_count = (By.CSS_SELECTOR, ".counter-value")
        final_button = (By.CSS_SELECTOR, ".smart-button-secondary")
        order_taxi_modal_title = (By.XPATH, "//span[@class='smart-button-main']")
  # Adición: Verificar despliegue del modal
        add_card_button = (By.XPATH, "//div[contains(@class, 'pp-title') and text()='Agregar tarjeta']")
        card_number_field = (By.ID, 'number')  # Actualización: Campo para número de tarjeta
        card_code_field = (By.XPATH, "//input[@id='code' and contains(@class, 'card-input')]")
        link_card_button = (By.ID, 'link')  # Adición: Botón para vincular tarjeta
        submit_card_button = (By.XPATH,
                              "//button[@type='submit' and contains(@class, 'button full') and text()='Agregar']")
        close_modal_button = (By.XPATH, "(//button[@class='close-button section-close'])[3]")

        payment_method_button = (By.XPATH, "//div[contains(@class, 'pp-button filled')]")


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

        def click_close_modal(self):  # Adición: Metodo para cerrar la ventana modal
            self.driver.find_element(*self.close_modal_button).click()

    class ComfortMethod:
        def __init__(self, driver):
            self.driver = driver

        def select_comfort(self):
            """Hace scroll hasta el botón Comfort y luego hace clic."""
            comfort_button = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comfort_button)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", comfort_button)  # Hace scroll
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(UrbanRoutesAutomation.UrbanRoutesPage.comfort_button))
            comfort_button.click()

        def return_status_trip(self):
            """Verifica que la tarifa Comfort esté seleccionada."""
            active_tariff = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comfort_active_card)
            return active_tariff.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.comfort_title).text == "Comfort"

    class AddPhoneNumber:
        def __init__(self, driver):
            self.driver = driver

        def write_phone_number(self, number):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.phone_number_field).send_keys(number)

        def post_number(self):
            self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.next_button).click()

        def click_phone_area_button(self):
            """Espera a que el área de número de teléfono sea clickeable y hace clic."""
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.phone_area_button))
            self.driver.find_element(*self.phone_area_button).click()

        def return_phone_number(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.phone_displayed_text).text  # Adición

        def return_phone_number(self):
            return self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.phone_number_field).get_property('value')

        def send_phone_number(self, number):
            self.write_phone_number(number)
            self.post_number()

    class AddCreditCard:
        def __init__(self, driver):
            self.driver = driver

        def click_payment_method_button(self):
            payment_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(UrbanRoutesAutomation.UrbanRoutesPage.payment_method_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", payment_button)
            payment_button.click()

        def click_add_card_button(self):
            add_card_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(UrbanRoutesAutomation.UrbanRoutesPage.add_card_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_button)
            add_card_button.click()


        def enter_card_details(self, card_number, card_code):
            try:
                # Ingresa número de tarjeta
                card_field = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(UrbanRoutesAutomation.UrbanRoutesPage.card_number_field)
                )
                card_field.send_keys(card_number)
                time.sleep(1)

                # Ingresa CVV
                cvv_field = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(UrbanRoutesAutomation.UrbanRoutesPage.card_code_field)
                )
                cvv_field.send_keys(card_code)
                time.sleep(1)

                # Localiza el botón "Agregar"
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(UrbanRoutesAutomation.UrbanRoutesPage.submit_card_button)
                )

                # Realiza un doble clic en el botón "Agregar"
                actions = ActionChains(self.driver)
                actions.double_click(submit_button).perform()
                time.sleep(2)

                print("Doble clic realizado en el botón 'Agregar'.")

                # Cierra la ventana emergente
                close_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(UrbanRoutesAutomation.UrbanRoutesPage.close_modal_button)
                )
                close_button.click()
                print("Ventana emergente cerrada exitosamente.")

                # Verifica que la ventana se haya cerrado
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located(UrbanRoutesAutomation.UrbanRoutesPage.close_modal_button)
                )
                print("Confirmación: La ventana emergente ya no está visible.")

            except Exception as e:
                print(f"Error al ingresar detalles de la tarjeta o cerrar la ventana: {e}")
                raise

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
            """Hace clic en el control visual (slider) para seleccionar la manta."""
            slider = self.driver.find_element(By.CSS_SELECTOR, "span.slider.round")
            checkbox = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.checkbox_blanket)

            # Clic en el slider si el checkbox no está seleccionado
            if not checkbox.is_selected():
                slider.click()
                WebDriverWait(self.driver, 5).until(lambda d: checkbox.is_selected())

        def return_status_blanket(self):
            """Retorna si el checkbox de manta está seleccionado."""
            checkbox = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.checkbox_blanket)
            return checkbox.is_selected()

    class IceCreamOrder:
        def __init__(self, driver):
            self.driver = driver

        def add_ice_cream(self):
            for i in range(2):
                plus_button = self.driver.find_element(*UrbanRoutesAutomation.UrbanRoutesPage.ice_cream_plus_button)
                self.driver.execute_script("arguments[0].scrollIntoView();", plus_button)
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".counter-plus")))
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

