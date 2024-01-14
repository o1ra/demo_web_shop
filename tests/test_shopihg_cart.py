import allure
from selene import browser, have
from allure_commons._allure import step
from allure_commons.types import Severity
from demo_shop.utils.help_post import demowebshop_api_post

base = 'https://demowebshop.tricentis.com'


@allure.tag("UI")
@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.label('layer', 'UI&API')
@allure.feature("Корзина")
@allure.story("Добавление в корзину")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Добавление товара в корзину")
def test_add_to_cart_from_catalog_with_api(browser_setup):
    url = f'{base}/addproducttocart/catalog/22/1/1'
    response = demowebshop_api_post(url)
    cookie = response.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.open('/')

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check one item presents"):
        browser.all('.cart-item-row').should(have.size(1))
        browser.all('.cart-item-row').element_by(have.text('Health Book')
                                                 ).element('[name^="itemquantity"]').should(have.value("1"))


@allure.tag("UI")
@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.label('layer', 'UI&API')
@allure.feature("Корзина")
@allure.story("Добавление в корзину")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Добавление нескольких едениц товара в корзину")
def test_add_to_cart_some_desktop_with_api(browser_setup):
    with step("Adding to cart a 2 laptop"):
        url = f'{base}/addproducttocart/details/31/1'
        data = {'addtocart_31.EnteredQuantity': 2}
        response = demowebshop_api_post(url, data=data)
        cookie = response.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.open('/')

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check one item presents"):
        browser.all('.cart-item-row').should(have.size(1))
        browser.all('.cart-item-row').element_by(have.text('14.1-inch Laptop')
                                                 ).element('[name^="itemquantity"]').should(have.value("2"))


@allure.tag("UI")
@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.label('layer', 'UI&API')
@allure.feature("Корзина")
@allure.story("Добавление в корзину")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Добаление двух разных товаров к корзину")
def test_add_phones_and_laptop_with_api(browser_setup):
    with step("Adding to cart laptop"):
        url_1 = f'{base}/addproducttocart/catalog/31/1/1'
        response_1 = demowebshop_api_post(url_1)
        cookie_1 = response_1.cookies.get("Nop.customer")

    with step("Adding to cart Smartphone"):
        url_2 = f'{base}/addproducttocart/catalog/43/1/1'
        cookies = {"Nop.customer": cookie_1}
        response_2 = demowebshop_api_post(url_2, cookies=cookies)
        cookie_2 = response_2.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.open('/')

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie_2})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check one item presents"):
        browser.all('.cart-item-row').should(have.size(2))
        browser.all('.cart-item-row').element_by(have.text('14.1-inch Laptop')
                                                 ).element('[name^="itemquantity"]').should(have.value("1"))
        browser.all('.cart-item-row').element_by(have.text('Smartphone')
                                                 ).element('[name^="itemquantity"]').should(have.value("1"))
