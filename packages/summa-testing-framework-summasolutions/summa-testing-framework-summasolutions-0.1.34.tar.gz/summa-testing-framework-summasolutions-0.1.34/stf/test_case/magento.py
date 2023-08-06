from .base import BaseTestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import string
import random
from random import randint


class MagentoTestCase(BaseTestCase):
    def visit_product_page(self, sku):
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            search_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='search']")))
            search_input.send_keys(sku)
            search_input.submit()
            pdp = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-info-main']")))
            
        except:
            success = False
        
        return self.assertTrue(success, "Product Page was not found")

    def random_char(self, y):
        # function to generate random characters
        return ''.join(random.choice(string.ascii_lowercase) for x in range(y))


    def generateDocNumber(self):
        # function to generate a random document number
        return str(randint(20000000, 79999999))


    def generateMail(self):
        # function to generate a random mail address
        return 'automated_' + self.random_char(8) + str(randint(0, 999)) + '@testing.com'

    def checkout_loader(self):
        # function wait for checkout loader
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        loading_mask = wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading-mask']")))

    def add_simple_product(self):
        # function to add a simple product from product page
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # add to cart
            add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='product-addtocart-button']")))
            add_to_cart_button.click()
            
        except:
            success = False

        return self.assertTrue(success, "Product could not be added to cart")

    def validate_product_was_added(self):
        # function to validate success message in add to cart
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # wait for success message that contains cart link
            success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-ui-id='message-success']/.//a[contains(@href,'cart')]")))
            
        except:
            success = False
            
        return self.assertTrue(success, "Product was not added to cart")

    def open_minicart(self):
        # function to open minicart from header
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True
        
        try:
            # press minicart button
            minicart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-block='minicart']")))
            minicart_button.click()
            
        except:
            success = False

        return self.assertTrue(success, "Minicart could not be opened")

    def go_to_cart_from_minicart(self):
        # function to press go to cart button in minicart
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # press go to cart button
            cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='secondary']/a[contains(@class,'viewcart')]")))
            cart_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Cart could not be reached")

    def convert_price(self, priceText):
        # function to convert a string price to float
        sinMoneda = priceText.replace("$","")
        notacion = sinMoneda.replace(".","")
        notacionPunto = notacion.replace(",",".")
        return float(notacionPunto)

    def validate_cart_totals(self, discount_amount):
        # function to validate totals in cart
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True
        
        try:
            grand_total = 0
            table_grand_total = 0
            # wait for cart totals
            cart_totals = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='cart-totals']")))
            
            # sum all item subtotals from product list
            items_subtotal = 0
            product_price_list = driver.find_elements(By.XPATH, "//table[@id='shopping-cart-table']/.//td[contains(@class,'subtotal')]/.//span[@class='price']")
            for item in product_price_list:
                items_subtotal = items_subtotal + self.convert_price(item.get_attribute('innerHTML'))
            
            # obtain data from cart totals table
            subtotal_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//tr[contains(@class, 'sub')]/.//span[@class='price']")))
            table_subtotal = self.convert_price(subtotal_text.get_attribute('innerHTML'))

            # validate both subtotals against each other
            if items_subtotal == table_subtotal:
                pass
            else:
                raise Exception("Cart Subtotals don't match")

            # sum all subtotals from cart totals table
            if discount_amount > 0:
                # obtain discount data
                discount_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//tr[@class='totals']/.//span[@class='price']")))
                table_discount = self.convert_price(discount_text.get_attribute('innerHTML'))
            else:
                table_discount = 0
            grand_total = round(table_subtotal + table_discount,2)

            # validate grand total
            grand_total_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//tr[contains(@class,'grand')]/.//span[@class='price']")))
            table_grand_total = self.convert_price(grand_total_text.get_attribute('innerHTML'))
            if grand_total == table_grand_total:
                pass
            else:
                raise Exception

            
        except:
            success = False
        
        return self.assertTrue(success, "Cart Grand Total doesn't match: "+str(grand_total)+" against "+str(table_grand_total))


    def validate_checkout_cart_totals(self, payment_plan, discount_amount):
        # function to validate totals in checkout cart
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            grand_total = 0
            table_grand_total = 0
            cart_totals_xpath = "//div[@class='opc-block-summary']"
            # wait for cart totals summary
            cart_totals = wait.until(EC.visibility_of_element_located((By.XPATH, cart_totals_xpath)))
            
            # sum all item subtotals from product list
            items_subtotal = 0
            product_price_list = driver.find_elements(By.XPATH, cart_totals_xpath+"/.//div[contains(@class,'subtotal')]/.//span[@class='price']")
            for item in product_price_list:
                items_subtotal = items_subtotal + self.convert_price(item.get_attribute('innerHTML'))
            
            # obtain data from cart totals table
            # subtotal
            subtotal_text = wait.until(EC.visibility_of_element_located((By.XPATH, cart_totals_xpath+"/.//tr[contains(@class, 'sub')]/.//span[@class='price']")))
            table_subtotal = self.convert_price(subtotal_text.get_attribute('innerHTML'))
            # shipping
            shipping_cost_text = wait.until(EC.visibility_of_element_located((By.XPATH, cart_totals_xpath+"/.//tr[contains(@class, 'shipping')]/.//span[@class='price']")))
            table_shipping_cost = self.convert_price(shipping_cost_text.get_attribute('innerHTML'))
            # financing cost
            table_financing_cost = 0
            if payment_plan['interest']:
                financing_cost_text = wait.until(EC.visibility_of_element_located((By.XPATH, cart_totals_xpath+"/.//tr[contains(@class, 'discount_coupon')]/.//span[@class='price']")))
                table_financing_cost = self.convert_price(financing_cost_text.get_attribute('innerHTML'))
            # discount coupon
            table_discount = 0
            if discount_amount > 0:
                discount_text = wait.until(EC.visibility_of_element_located((By.XPATH, cart_totals_xpath+"/.//tr[contains(@class,'discount') and not(contains(@class,'coupon'))]/.//span[@class='price']")))
                table_discount = self.convert_price(discount_text.get_attribute('innerHTML'))
            # grand total
            grand_total_text = wait.until(EC.visibility_of_element_located((By.XPATH, cart_totals_xpath+"/.//tr[contains(@class, 'grand')]/.//span[@class='price']")))
            table_grand_total = self.convert_price(grand_total_text.get_attribute('innerHTML'))
            
            # validate both subtotals against each other
            if items_subtotal == table_subtotal:
                pass
            else:
                raise Exception
            
            # validate grand total
            grand_total = round(table_subtotal + table_shipping_cost + table_financing_cost + table_discount,2)
            if grand_total == table_grand_total:
                pass
            else:
                raise Exception
            
        except:
            success = False
        
        return self.assertTrue(success, "Cart Grand Total doesn't match: "+str(grand_total)+" against "+str(table_grand_total))
        

    def add_discount_coupon_in_cart(self, coupon_code):
        # function to add a discount coupon in cart
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True
        discount_form_xpath = "//form[@id='discount-coupon-form']"

        try:
            # wait for cart totals
            cart_totals = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='cart-totals']")))
            subtotal_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//tr[contains(@class, 'sub')]/.//span[@class='price']")))

            # expand coupon input
            expand_coupon = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='block-discount']")))
            expand_coupon.click()

            # fill discount coupon
            input_coupon = wait.until(EC.visibility_of_element_located((By.XPATH, discount_form_xpath+"/.//input[@id='coupon_code']")))
            input_coupon.send_keys(coupon_code)

            # press apply
            apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, discount_form_xpath+"/.//button[contains(@class,'apply')]")))
            apply_button.click()

            # wait for success message
            coupon_success = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-ui-id='message-success']/*[contains(text(),'"+coupon_code+"')]")))
            
        except:
            success = False
        
        return self.assertTrue(success, "Discount coupon could not be added")

        
    def go_to_checkout(self):
        # function to go to checkout from cart
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # press checkout button
            checkout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-role='proceed-to-checkout']")))
            checkout_button.click()
            
        except:
            success = False

        return self.assertTrue(success, "Checkout page could not be reached")

    def select_shipping_method(self, shipping_method):
        # function to choose shipping method in checkout first step
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # wait for shipping methods
            shipping_methods_selector = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='delivery-method-selector']")))

            # choose shipping_method
            shipping_selector = self.config['shipping_parameters'][shipping_method]
            shipping_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='delivery-method-selector']/.//button[contains(@class,'select-"+str(shipping_selector)+"')]")))
            shipping_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Shipping method could not be selected")

    def fill_customer_email(self, email):
        # function to input customer email
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # fill customer email
            input_email = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='customer-email']")))
            input_email.send_keys(email)

            # continue
            continueBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//fieldset[@id='customer-email-fieldset']/.//button[contains(@data-bind,'confirmStep')]")))
            continueBtn.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Customer email could not be filled")

    def fill_customer_email_storepickup(self, email):
        # function to input customer email when shipping method is store pickup
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # fill customer email
            input_email = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='store-pickup-checkout-customer-email']")))
            input_email.send_keys(email)

            # continue
            continueBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//fieldset[@id='store-pickup-customer-email-fieldset']/.//button[contains(@data-bind,'confirmStep')]")))
            continueBtn.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Customer email could not be filled")

    def fill_personal_data(self, form_xpath, customer):
        # function to fill personal data in checkout forms
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])

        # First Name
        first_name = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='firstname']")))
        first_name.send_keys(customer['firstname'])
        # Last Name
        last_name = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='lastname']")))
        last_name.send_keys(customer['lastname'])
        # Vat ID
        vat_id = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='vat_id']")))
        vat_id.send_keys(customer['vat_id'])
        # Telephone Number
        telephone_number = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='telephone']")))
        telephone_number.send_keys(customer['telephone'])

    def fill_address_data(self, form_xpath, address):
        # function to fill address data in checkout forms
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])

        # Street
        street_name = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='street[0]']")))
        street_name.send_keys(address['street'])
        # Street Number
        street_number = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='street[1]']")))
        street_number.send_keys(address['number'])
        # Postcode
        postal_code = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='postcode']")))
        postal_code.send_keys(address['postcode'])
        # Region
        region = wait.until(
            EC.visibility_of_element_located((By.XPATH, form_xpath+"//select[@name='region_id']/option[@value='"+address['region_id']+"']")))
        region.click()
        # City
        city = wait.until(EC.visibility_of_element_located((By.XPATH, form_xpath+"//input[@name='city']")))
        city.send_keys(address['city'])
        
    def fill_new_shipping_address(self, customer, shipping_address):
        # function to fill new shipping address
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True
        
        try:
            shipping_form = "//div[@id='shipping-new-address-form']/."
            self.checkout_loader()

            # fill personal data
            self.fill_personal_data(shipping_form, customer)

            # fill new shipping address data in the form
            self.fill_address_data(shipping_form, shipping_address)

            # confirm address
            update_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//form[@id='co-shipping-form']/.//button[@data-role='opc-continue']")))
            update_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Shipping address could not be filled")


    def fill_new_billing_address(self, customer, billing_address):
        # function to fill new billing address in payment step
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            billing_form = "//div[@class='checkout-billing-address']/."
            self.checkout_loader()

            # fill personal data
            self.fill_personal_data(billing_form, customer)

            # fill new billing address data in the form
            self.fill_address_data(billing_form, billing_address)

            # confirm address
            update_button = wait.until(EC.element_to_be_clickable((By.XPATH, billing_form+"//button[contains(@class,'action-update')]")))
            update_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Billing address could not be filled")

    def select_delivery_type(self, delivery_type):
        # function to choose shipping delivery type in checkout first step after selecting shipping method: delivery
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            self.checkout_loader()

            # select delivery type
            delivery_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='"+delivery_type+"']")))
            delivery_selector.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Delivery could not be selected")

    def select_store(self, store_id):
        # function to choose a store to pickup the order
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True
        
        try:
            # wait for store selector list
            store_list = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@id='store-selector-popup']")))

            # select store to pickup order
            store_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@id='store-selector-popup']/.//div[@class='select-location']/button)["+store_id+"]")))
            store_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Store could not be selected")

    def continue_to_payment(self):
        # function to continue to payment step in checkout
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # press continue button
            continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='shipping-method-buttons-container']/.//button[@data-role='opc-continue']")))
            continue_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Payment page could not be reached")

    def continue_to_payment_storepickup(self):
        # function to continue to payment step in checkout when method is store pickup
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True
        
        try:
            # press continue button
            continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='checkout-step-store-selector']/.//button[@data-role='opc-continue']")))
            continue_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Payment page could not be reached")

    def select_payment_method(self, payment_method):
        # function to select a payment method in payment step in checkout
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            self.checkout_loader()

            # wait for payment methods list
            payment_methods_list = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@id='checkout-payment-method-load']")))

            # select payment method
            payment_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+payment_method+"']")))
            payment_selector.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Payment method could not be selected")

    def fill_payment_data(self, payment_method, card, payment_plan):
        # function to fill payment data in payment method section
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # check which method has been selected
            if payment_method == 'mercadopago_custom_aggregator':
                suffix = '-ag'
                self.fill_mercadopago_card(suffix, card, payment_plan)
            if payment_method == 'mercadopago_custom':
                suffix = ''
                self.fill_mercadopago_card(suffix, card, payment_plan)
            if payment_method == 'checkmo':
                pass
            
        except:
            success = False
        
        return self.assertTrue(success, "Payment data could not be filled")

    def fill_mercadopago_card(self, suffix, card, payment_plan):
        # function to fill mercadopago credit card form
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            self.checkout_loader()
            
            # fill card form
            # Card Number
            card_number = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='card-number"+suffix+"']")))
            card_number.send_keys(card['number'])

            # Expiration Date
            exp_month = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='expiration-month"+suffix+"']/option[@value='"+card['month']+"']")))
            exp_month.click()
            exp_year = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='expiration-year"+suffix+"']/option[@value='"+card['year']+"']")))
            exp_year.click()

            # Card Holder Name
            card_holder = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='card-holder-name"+suffix+"']")))
            card_holder.send_keys(card['owner'])

            # Security Code
            security_code = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='security-code"+suffix+"']")))
            security_code.send_keys(card['cvv'])

            # Holder Document Type
            doc_type = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='document-type"+suffix+"']/option[@value='DNI']")))
            doc_type.click()

            # Document Number
            doc_number = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='cdocument-number"+suffix+"']")))
            doc_number.send_keys(card['dni'])

            # Issuer
            if card['issuer'] != 0:
                issuer_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='issuer"+suffix+"']/option[@value='"+card['issuer']+"']")))
                issuer_selector.click()
                # Installments
                installments_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='installments"+suffix+"']/option[@value='"+payment_plan['installments']+"']")))
                installments_selector.click()
            
        except:
            success = False
        
        return self.assertTrue(success)

    def place_order(self):
        # function to place order in payment step
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            self.checkout_loader()

            # press place order button
            place_order_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'payment-method _active')]/.//button[@type='submit']")))
            place_order_button.click()
            
        except:
            success = False
        
        return self.assertTrue(success, "Order could not be placed")

    def success_page(self):
        # function to validate success page
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success = True

        try:
            # check for generated order id
            order_id = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='checkout-success']")))
            
        except:
            success = False
        
        return self.assertTrue(success, "Order was not generated successfuly")
