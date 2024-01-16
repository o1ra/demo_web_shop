import allure
import jsonschema
from allure_commons._allure import step
from allure_commons.types import Severity
from demo_shop_tests.utils.help_post import demowebshop_api_post
from demo_shop_tests.utils.load_shema import load_path
from demo_shop_tests.utils.random_email import random_email


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.label('layer', 'API')
@allure.feature("Подписка")
@allure.story("Успешная подписка на письма")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Успешная подписка на письма")
def test_subscribe_news_letter_successful(base_url):
    url = f'{base_url}/subscribenewsletter'
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
@allure.label('layer', 'API')
@allure.feature("Подписка")
@allure.story("Попытка оформить подписку с некорректной почты")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Попытка оформить подписку с некорректной почты")
def test_subscribe_news_letter_unsuccessful(base_url):
    url = f'{base_url}/subscribenewsletter'
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


