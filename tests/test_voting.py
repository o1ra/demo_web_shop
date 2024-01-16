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
@allure.feature("Опрос")
@allure.story("Участие в опросе неавторизированным пользователем")
@allure.link("https://demowebshop.tricentis.com/", name="Testing")
@allure.title("Голосование в опросе неавторизированным пользователем")
def test_voting_in_a_poll_by_unauthorized(base_url):
    url = f'{base_url}/poll/vote'
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
