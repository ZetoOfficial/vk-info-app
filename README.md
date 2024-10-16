# VK Info App

Консольное приложение для получения информации о пользователе ВКонтакте, его подписчиках, подписках и группах в подписках через VK API.

## Требования

- **Python 3.7** или выше
- **VK Access Token** с необходимыми правами (`users`, `friends`, `groups`)

## Установка

### 1. Клонируйте репозиторий

Откройте терминал (для Linux) или командную строку (для Windows) и выполните следующие команды:

```bash
git clone https://github.com/ZetoOfficial/vk_info_app.git
cd vk_info_app
```

### 2. Создайте и активируйте виртуальное окружение (опционально)

**Для Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Для Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Установите зависимости

После активации виртуального окружения установите необходимые библиотеки:

```bash
pip install -r requirements.txt
```

### 4. Настройте файл `.env`

Файл `.env` содержит ваши конфиденциальные данные, такие как VK Access Token. Следуйте этим шагам:

1. **Скопируйте пример файла `.env.example` в `.env`:**

   **Для Linux/macOS:**

   ```bash
   cp .env.example .env
   ```

   **Для Windows:**

   ```cmd
   copy .env.example .env
   ```

2. **Откройте файл `.env` в текстовом редакторе и замените `YOUR_ACCESS_TOKEN` на ваш VK Access Token:**

   ```env
   VK_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
   ```

   **Простой способ получения VK Access Token:**

   - Перейдите на [vkhost](https://vkhost.github.io/) и выберите приложение (admin например)
   - Скопируйте токен из адресной строки

   **Получение VK Access Token путем создания своего приложения:**

   - Перейдите на [VK для разработчиков](https://vk.com/dev) и создайте приложение.
   - Получите токен доступа с правами `friends`, `groups`, `users`.

## Использование

Запуск приложения осуществляется через терминал или командную строку.

```bash
python vk_info.py [user_id] [-o OUTPUT]
```

### Аргументы

- `user_id` (необязательный): Идентификатор пользователя ВКонтакте. По умолчанию `self` (текущий пользователь).
- `-o`, `--output` (необязательный): Путь к файлу результата. По умолчанию `vk_user_info.json`.

### Примеры

1. **Получить информацию о текущем пользователе и сохранить в `vk_user_info.json`:**

   ```bash
   python vk_info.py
   ```

2. **Получить информацию о пользователе с ID `123456` и сохранить в `output.json`:**

   ```bash
   python vk_info.py 123456 -o output.json
   ```

## Результат

После успешного выполнения, в указанном файле будет сохранена информация о пользователе, количестве подписчиков, подписках и группах в читаемом формате JSON с поддержкой кириллицы.

### Пример содержимого `vk_user_info.json`:

```json
{
  "user": {
    "id": 206201111,
    "first_name": "Павел",
    "last_name": "Титов",
    "followers_count": 133
  },
  "followers_count": 133,
  "subscriptions_count": 4,
  "groups": [
    {
      "id": 29346,
      "name": "Тюменский государственный университет | ТюмГУ",
      "screen_name": "tyumen.university"
    },
    ...
  ]
}
```
