import allure
import jsonschema
from allure_commons._allure import step
from allure_commons.types import Severity
from demo_shop_tests.utils.help_post import demowebshop_api_post
from demo_shop_tests.utils.load_shema import load_path


@allure.tag("API")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Irina_Kirillova")
@allure.label('layer', 'API')
@allure.feature("Список желаний")
@allure.story("Добавление товара в список желаний")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Добавление товара в список желаний")
def test_added_wishlist(base_url):
    url = f'{base_url}/addproducttocart/details/22/2'
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
@allure.label('layer', 'API')
@allure.feature("Список желаний")
@allure.story("Добавление больше одного товара в список желаний")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Добавление больше одного товара в список желаний")
def test_added_wishlist_2_qwantity_product(base_url):
    url = f'{base_url}/addproducttocart/details/78/2'
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
