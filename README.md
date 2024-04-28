# Помогающий ментально телеграм бот
Этот бот призван помогать людям при помощи моральной поддержки. Он отвечает на текстовые сообщения текстом, а на
голосовые - голосом. Предусмотрены широкие возможности для отладки и настройки.

# Технологии и библиотеки

Использованные технологии:<br>
<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" width="50px" height="50px">
<img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" width="50px" height="50px">
<img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" width="50px" height="50px">

Использованные библиотеки python:
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [pydantic-settings](https://pypi.org/project/pydantic-settings/)
- [requests](https://pypi.org/project/requests/)

# Как запустить проект?

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/LaGGgggg/yp_multi_helper_tg_bot.git
cd yp_multi_helper_tg_bot
```

### 2. Создайте виртуальное окружение

#### С помощью [pipenv](https://pipenv.pypa.io/en/latest/):

```bash
pip install --user pipenv
pipenv shell  # create and activate
```

#### Или классическим методом:

```bash
python -m venv .venv  # create
.venv\Scripts\activate.bat  # activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Установите переменные окружения (environment variables)

Создайте файл `.env`, это должно выглядеть так: `yp_multi_helper_tg_bot/.env`. После скопируйте это в `.env`

```dotenv
BOT_TOKEN=<your_bot_token>
DB_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
STT_API_KEY=<your_stt_api_key>
STT_FOLDER_ID=<your_stt_folder_id>
TTS_API_KEY=<your_tts_api_key>
TTS_FOLDER_ID=<your_tts_folder_id>
GPT_API_KEY=<your_gpt_api_key>
GPT_FOLDER_ID=<your_gpt_folder_id>
DEBUG_USER_ID=<your_debug_user_id>
```
_**Не забудьте поменять значения на свои! (поставьте их после "=")**_

#### Больше о переменных:
BOT_TOKEN - [токен телеграм бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)<br>
DB_URL - [url базы данных](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) sqlalchemy<br>
STT_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
STT_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>
TTS_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
TTS_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>
GPT_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
GPT_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>
DEBUG_USER_ID - ID пользователя, который сможет получать файлы с логами бота (при помощи команд)

### 5. Запустите проект

```bash
python main.py
```

# Продакшен настройка

### 1. Установите [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 2. Установите [docker](https://docs.docker.com/engine/install/)

### 3. Установите [docker compose plugin](https://docs.docker.com/compose/install/linux/)

### 4. Клонируйте репозиторий

```bash
git clone https://github.com/LaGGgggg/yp_multi_helper_tg_bot.git
cd yp_multi_helper_tg_bot
```

### 5. Установите переменные окружения (environment variables)

Создайте файл `.env`, это должно выглядеть так: `yp_multi_helper_tg_bot/.env`. После скопируйте это в `.env`

```dotenv
BOT_TOKEN=<your_bot_token>
DB_URL=postgresql://<username>:<password>@postgres:5432/<database_name>
STT_API_KEY=<your_stt_api_key>
STT_FOLDER_ID=<your_stt_folder_id>
TTS_API_KEY=<your_tts_api_key>
TTS_FOLDER_ID=<your_tts_folder_id>
GPT_API_KEY=<your_gpt_api_key>
GPT_FOLDER_ID=<your_gpt_folder_id>
DEBUG_USER_ID=<your_debug_user_id>

# docker compose section
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database_name>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata
```
_**Не забудьте поменять значения на свои! (поставьте их после "=")**_

#### Больше о переменных:
BOT_TOKEN - [токен телеграм бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)<br>
DB_URL - [url базы данных](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) sqlalchemy<br>
STT_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
STT_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>
TTS_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
TTS_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>
GPT_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
GPT_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>
DEBUG_USER_ID - ID пользователя, который сможет получать файлы с логами бота (при помощи команд)<br>

POSTGRES_USER - [POSTGRES_USER](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_PASSWORD - [POSTGRES_PASSWORD](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_DB - [POSTGRES_DB](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_HOST - [POSTGRES_HOST](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_PORT - [POSTGRES_PORT](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
PGDATA - [PGDATA](https://hub.docker.com/_/postgres) стандартная переменная окружения docker

### 6. Запустите docker compose

```bash
docker compose up -d
```

### 7. После успешного запуска проверьте сервер

```bash
docker compose logs -f
```


# Дополнительные возможности настройки

Помимо обязательных переменных окружения, есть опциональные, расширяющие возможности конфигурации проекта.
Ниже представлены эти переменные с типизацией и значениями по умолчанию
(несмотря на то, что представлен код на python, переменные окружения должны устанавливаться из файла `.env`).

```python
# Сообщения об ошибках:
# сообщение, которое выводится пользователю при ошибке обращения в API
USER_FRIENDLY_REQUEST_ERROR_MESSAGE: str = \
    'Произошла ошибка, пожалуйста, повторите попытку или обратитесь в поддержку'
# шаблон сообщения, которое записывается в логи при неизвестной ошибке во время обращения в API
# (должно включать в себя "{service_name}", "{error}" и "{context}")
LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE: str = \
    'An exception occurred while requesting {service_name} answer: {error}\n\nContext: "{context}"'
# шаблон сообщения, которое записывается в логи при статус-коде ответа API, не равном 200
# (должно включать в себя "{service_name}", "{status_code}" и "{context}")
LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE: str = \
    'Incorrect {service_name} answer status code: {status_code} (context: "{context}")'

# TTS (text to speech)
TTS_CHARACTERS_IN_BLOCK: int = 250  # количество символов в блоке
TTS_URL: str = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'  # url для обращения в API
TTS_LANGUAGE: str = 'ru-RU'  # язык
TTS_VOICE: str = 'filipp'  # голос

# STT (speech to text)
STT_SECONDS_IN_BLOCK: int = 15  # количество секунд в блоке
STT_URL: str = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'  # url для обращения в API
STT_LANGUAGE: str = 'ru-RU'  # язык

# GPT
GPT_URL: str = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'  # url для обращения в API
# url для обращения в API для токенизации
GPT_TOKENIZE_URL: str = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize'
GPT_MODEL: str = 'yandexgpt-lite'  # модель GPT
GPT_TEMPERATURE: float = 1  # температура GPT
# системный промпт
GPT_SYSTEM_PROMPT: str = (
    'Ты должен оказать поддержку. Общайся вежливо и создавай хорошее настроение. Будь краток.'
    ' Не пиши НИЧЕГО про готовность оказать поддержку или создать хорошее настроение'
)
GPT_RESPONSE_MAX_TOKENS: int = 300  # максимальное количество токенов в ответе GPT

# Лимиты запросов
REQUEST_MAX_SECOND_BLOCKS: int = 2  # максимальное количество блоков секунд при обращении в STT
REQUEST_MAX_CHARACTER_BLOCKS: int = 5  # максимальное количество блоков символов при обращении в TTS
REQUEST_MAX_TOKENS: int = 300  # максимальное количество токенов при обращении в GPT

# Лимиты пользователей
SECOND_BLOCKS_LIMIT_BY_USER: int = 25  # максимальное количество блоков секунд на одного пользователя
CHARACTER_BLOCKS_LIMIT_BY_USER: int = 20  # максимальное количество блоков символов на одного пользователя
TOKENS_LIMIT_BY_USER: int = 2500  # максимальное количество токенов на одного пользователя
MAX_USERS_AMOUNT_LIMIT: int = 10  # максимальное количество пользователей бота
```
