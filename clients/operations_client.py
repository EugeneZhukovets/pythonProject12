import allure
from httpx import Response

from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.operations import CreateOperationSchema, OperationSchema, UpdateOperationSchema
from tools.routes import APIRoutes


class OperationsClient(BaseClient):

    @allure.step("Получить список операций")
    def get_operations_api(self) -> Response:
        """
                Получить список всех операций.

                :return: Ответ от сервера с информацией о всех операциях.
                """
        return self.get(APIRoutes.OPERATIONS)

    @allure.step("Получить операцию по ID")
    def get_operation_api(self, operation_id: int) -> Response:
        """
        Получить операцию по идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера с информацией об операции.
        """
        return self.get(f"{APIRoutes.OPERATIONS}/{operation_id}")

    @allure.step("Создать операцию")
    def create_operation_api(self, operation: CreateOperationSchema) -> Response:
        """
                Создать операцию.

                :param operation: Данные для создания новой операции.
                :return: Ответ от сервера с информацией о созданной операции.
                """
        return self.post(
            APIRoutes.OPERATIONS,
            json=operation.model_dump(mode='json', by_alias=True)
        )

    @allure.step("Обновить операцию по id={operation_id}")
    def update_operation_api(self, operation_id: int, operation: UpdateOperationSchema) -> Response:
        """
                Обновить операцию по идентификатору.

                :param operation_id: Идентификатор операции, которую нужно обновить.
                :param operation: Данные для обновления операции.
                :return: Ответ от сервера с обновленными данными операции.
                """
        return self.patch(
            f"{APIRoutes.OPERATIONS}/{operation_id}",
            json=operation.model_dump(mode='json', by_alias=True, exclude_none=True)
        )

    @allure.step("Delete operation by id {operation_id}")
    def delete_operation_api(self, operation_id: int) -> Response:
        """
        Удалить операцию по идентификатору.

        :param operation_id: Идентификатор операции, которую нужно удалить.
        :return: Ответ от сервера с результатом удаления операции.
        """
        return self.delete(f"{APIRoutes.OPERATIONS}/{operation_id}")

    def create_operation(self) -> OperationSchema:
        """
        Упрощенный метод для создания новой операции.

        Этот метод создает операцию с помощью схемы `CreateOperationSchema`, отправляет запрос
        на создание, а затем преобразует ответ в объект `OperationSchema`.

        :return: Объект `OperationSchema`, представляющий созданную операцию.
        """
        # Создаем запрос с фейковыми данными (по умолчанию для теста)
        request = CreateOperationSchema()
        # Отправляем запрос на создание
        response = self.create_operation_api(request)
        # Возвращаем созданную операцию как объект схемы
        return OperationSchema.model_validate_json(response.text)



def get_operations_client(settings: Settings) -> OperationsClient:
    """
    Функция для создания экземпляра OperationsClient с нужными настройками.

    :param settings: Конфигурация с настройками для работы с API.
    :return: Экземпляр клиента для работы с операциями.
    """
    return OperationsClient(client=get_http_client(settings.fake_bank_http_client))
