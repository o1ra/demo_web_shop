import allure
import jsonschema
from allure_commons._allure import step
from allure_commons.types import Severity
from demo_shop.utils.help_post import demowebshop_api_post
from demo_shop.utils.load_shema import load_path
from demo_shop.utils.random_email import random_email

base = 'https://demowebshop.tricentis.com'


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.feature("Опрос")
@allure.story("Участие в опросе неавторизированным пользователем")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
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

    with step('Проверить сообщение об ошибке'):
        expected_error_message = "Only registered users can vote."
        assert result.json()["error"] == expected_error_message, "Неверное сообщение об ошибке"


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.feature("Подписка")
@allure.story("Успешная подписка на письма")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
def test_subscribe_news_letter_successful():
    url = f'{base}/subscribenewsletter'
    schema = load_path("subscribe_news_letter_success.json")
    data = {
        "email": random_email,

    }

    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить сообщение с результатом'):
        expected_error_message = ("Thank you for signing up! "
                                  "A verification email has been sent. "
                                  "We appreciate your interest.")
        assert result.json()["Result"] == expected_error_message, "Неверное сообщение об ошибке"


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.feature("Подписка")
@allure.story("Попытка оформить подписку с некорректной почты")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
def test_subscribe_news_letter_unsuccessful():
    url = f'{base}/subscribenewsletter'
    schema = load_path("subscribe_news_letter_fail.json")
    data = {
        "email": "test",

    }

    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить сообщение об ошибке'):
        assert result.json()["Result"] == "Enter valid email", "Неверное сообщение об ошибке"


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.feature("Список желаний")
@allure.story("Добавление товара в список желаний")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
def test_added_wishlist():
    url = f'{base}/addproducttocart/details/22/2'
    schema = load_path("added_wishlist_success.json")

    data = {
        'addtocart_22.EnteredQuantity': 1,

    }
    result = demowebshop_api_post(url, data=data)

    with step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200

    with step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)

    with step('Проверить статус ответа'):
        assert result.json()["success"], "Статус ответа не равен True"

    with step('Проверить количество товара в списке желаний'):
        expected_wishlist_count = "(1)"
        assert result.json()["updatetopwishlistsectionhtml"] == expected_wishlist_count, ("Неверное количество товара "
                                                                                          "в списке желаний")


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.feature("Список желаний")
@allure.story("Добавление больше одного товара в список желаний")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
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

    with step('Проверить статус ответа'):
        assert not result.json()["success"], "Статус ответа не равен False"

    with step('Проверить сообщение об ошибке'):
        expected_error_message = [
            "Your quantity exceeds stock on hand. The maximum quantity that can be added is 1."
        ]
        assert result.json()["message"] == expected_error_message, "Неверное сообщение об ошибке"
