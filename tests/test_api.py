import allure
import jsonschema
from allure_commons._allure import step
from allure_commons.types import Severity
from selene import browser
from demo_shop.utils.help_post import demowebshop_api_post
from demo_shop.utils.load_shema import load_path
from demo_shop.utils.random_email import random_email

base = 'https://demowebshop.tricentis.com'
EMAIL = 'iri.kirillova.qa@gmail.com'
PASSWORD = 'test_diplom23'


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.feature("Главное меню")
@allure.story("Продажа")
@allure.link("https://krisha.kz", name="Testing")
def test_voting_in_a_poll_by_unauthorized():
    url = f'{base}/poll/vote'
    schema = load_path("pool_by_unauthorized.json")
    data = {
        "pollAnswerId": 2,

    }

    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить, что в корзине пусто'):
        assert result.json()["error"] == "Only registered users can vote."


# def test_login_though_api():
#     url = f'{base}/login'
#     data = {"Email": EMAIL,
#             "Password": PASSWORD,
#             "RememberMe": False}
#
#     with step("Авторизация с помощью API"):
#         result = requests.post(url=url, data=data, allow_redirects=False)
#
#     with step("Получаем cookie"):
#         cookie = result.cookies.get("NOPCOMMERCE.AUTH")
#
#     with step("Set cookie from API"):
#         browser.open(base)
#         browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
#         browser.open(base)
#
#
#     with step("Ответить на опрос"):
#         url = f'{base}/poll/vote'
#         schema = load_path("pool_by_authorized.json")
#         data = {
#         "pollAnswerId": 1,
#
#     }
#
#     result = demowebshop_api_post(url=url, data=data)
#
#     with step('Проверить, что API возвращает 200 код ответа'):
#         assert result.status_code == 200
#
#     with step('Провалидировать схему ответа'):
#         jsonschema.validate(result.json(), schema)


def test_subscribe_news_letter_successful():
    url = f'{base}/subscribenewsletter'
    schema = load_path("subscribe_news_letter_success.json")
    data = {
             "email": random_email,

     }
    print(random_email)
    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить, что в корзине пусто'):
        assert result.json()["Result"] == ("Thank you for signing up! "
                                           "A verification email has been sent. "
                                           "We appreciate your interest.")



def test_subscribe_news_letter_unsuccessful():
    url = f'{base}/subscribenewsletter'
    schema = load_path("subscribe_news_letter.json")
    data = {
        "email": "test",

    }

    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить, что в корзине пусто'):
        assert result.json()["Result"] == "Enter valid email"


def test_added_wishlist():
    url = f'{base}/addproducttocart/details/22/2'
    schema = load_path("added_wishlist.json")

    data = {
        'addtocart_22.EnteredQuantity': 1,

    }
    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить, что в корзине пусто'):
        assert result.json()["success"] == True
        assert result.json()["updatetopwishlistsectionhtml"] == "(1)"


def test_added_wishlist_2_qwantity_product():
    url = f'{base}/addproducttocart/details/78/2'
    schema = load_path("added_wishlist_fail.json")
    data = {
        'addtocart_78.EnteredQuantity': 2,

    }

    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить, что в корзине пусто'):
        assert result.json()["success"] == False

        assert result.json()["message"] == ["Your quantity exceeds stock on hand. The maximum quantity that can be added is 1."]
