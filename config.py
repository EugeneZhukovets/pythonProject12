from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class HTTPClientConfig(BaseModel):
    """
    Настройки http клиента
    Поля:
    - url (HttpUrl): URL сервера
    - timeout (float): Таймаут запроса
    """
    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        """
        Возвращает URL клиента
        """
        return str(self.url)


class Settings(BaseSettings):
    """
    Главная модель для хранения всех настроек проекта.

    Загружает переменные из файла `.env` и поддерживает вложенные структуры.

    Поля:
        fake_bank_http_client (HTTPClientConfig): Настройки HTTP-клиента.
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='.'
    )

    fake_bank_http_client: HTTPClientConfig

settings = Settings()

print(settings.fake_bank_http_client.client_url)  # "https://api.sampleapis.com"
print(settings.fake_bank_http_client.timeout)