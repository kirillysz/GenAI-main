# Документация REST API  

## Базовый URL  
```
https://ваш-домен/api/v1
https://ваш-домен/api/v1/users
https://ваш-домен/api/v1/chats
https://ваш-домен/api/v1/messages
```


## Общие ответы  
- **200 OK** - Успешный запрос  
- **404 Not Found** - Ресурс не найден  
- **409 Conflict** - Конфликт данных  
- **500 Internal Server Error** - Ошибка сервера  

---

## Пользователи (`/users`)  

### Создать пользователя  
**POST** `/users/add`  

**Пример ответа:**  
```json
{
    "data": {
        "telegram_id": "123456789",
        "status": "created"
    },
    "meta": {}
}
```

### Получить пользователя  
**GET** `/users/get?telegram_id=123456789`  

**Пример ответа:**  
```json
{
    "data": {
        "user_id": 1,
        "status": "found"
    },
    "meta": {}
}
```

---

## Чаты (`/chats`)  

### Получить все чаты пользователя  
**GET** `/chats/get_all_chats?user_id=1`  

**Пример ответа:**  
```json
{
    "data": {
        "chats": [
            {
                "chat_id": "a1b2c3d4-e5f6-7890",
                "user_id": 1,
                "title": "Техподдержка",
                "model": "gpt-4"
            },
            {
                "chat_id": "b2c3d4e5-f6a7-8901",
                "user_id": 1,
                "title": "Вопросы по API",
                "model": "gpt-3.5"
            }
        ],
        "status": "found"
    },
    "meta": {}
}
```

### Создать чат  
**POST** `/chats/create`  

**Пример ответа:**  
```json
{
    "data": {
        "chat": {
            "chat_id": "c3d4e5f6-a7b8-9012",
            "user_id": 1,
            "title": "Новый чат",
            "model": "gpt-4"
        },
        "status": "created"
    },
    "meta": {}
}
```

### Удалить чат
**POST** `/chats/delete`

**Пример ответа:**
```json
{
    "data": {
        "chat": true,
        "status": "deleted"
    },
    "meta": {}
}
```
---

## Сообщения (`/messages`)  

### Получить все сообщения чата  
**GET** `/messages/get_all_messages?chat_id=a1b2c3d4-e5f6-7890`  

**Пример ответа:**  
```json
{
    "data": {
        "messages": [
            {
                "message_id": "m1n2o3p4-q5r6-7890",
                "chat_id": "a1b2c3d4-e5f6-7890",
                "role": "user",
                "content": "Как работает API?"
            },
            {
                "message_id": "p5q6r7s8-t9u0-1234",
                "chat_id": "a1b2c3d4-e5f6-7890",
                "role": "assistant",
                "content": "API работает по REST протоколу..."
            }
        ],
        "status": "found"
    },
    "meta": {}
}
```

### Добавить сообщение  
**POST** `/messages/add`  

**Пример ответа:**  
```json
{
    "data": {
        "chat_id": "a1b2c3d4-e5f6-7890",
        "role": "user",
        "content": "Новое сообщение",
        "status": "created"
    },
    "meta": {}
}
```

### Редактировать сообщение  
**PUT** `/messages/edit?message_id=m1n2o3p4-q5r6-7890`  

**Пример ответа:**  
```json
{
    "data": {
        "chat_id": "a1b2c3d4-e5f6-7890",
        "message_id": "m1n2o3p4-q5r6-7890",
        "content": "Обновленный текст",
        "status": "edited"
    },
    "meta": {}
}
```

---

## Особенности:  
- Все примеры содержат по 2 объекта в массивах, где это уместно.  
- Используются реалистичные UUID и ID.  
- Сохранена структура ответов из исходного кода.  
- Для массивов всегда показан пример с двумя элементами.  