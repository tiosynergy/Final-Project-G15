#  Персональний помічник — Перелік команд

## Запуск пакету:
-  `assistant-bot`

- `Неправильна команда`
Приклад: `addsd`

## 1. Зберігати контакти
- `add <name> [phone]`  
  Приклад: `add Petro Kozak 0501234567`

- `add-address <name> "<address>"`  
  Приклад: `add-address Petro Kozak "Kyiv, Banana Str"`

- `add-email <name> <email>`  
  Приклад: `add-email Petro Kozak petro@example.com`

- `add-birthday <name> <DD.MM.YYYY>`  
  Приклад: `add-birthday Petro Kozak 15.03.1995`

## 2. Дні народження
- `birthdays <number_of_days>`  
  Приклад: `birthdays 7` / `birthdays 30`

## 3. Валідація
Автоматична. Приклади помилок:  
`add Ivan 123` → Phone number must be 10 digits.  
`add-email Ivan Ivan@invalid` → Invalid email format...

## 4. Пошук контактів
- `search <keyword>`  
  Приклад: `search Petro` / `search Khreshchatyk`

## 5. Редагування та видалення контактів
Приклад: `change-name Petro Kozak | Petro`
Приклад: `change Petro Kozak 0501234567 0679876543`
Приклад: `change-address Petro Kozak "Lviv, Apple str"`
Приклад: `change-email Petro Kozak new@kozak.com`
Приклад: `change-birthday Petro Kozak 15.03.1995 16.03.1996`
Приклад: `delete-phone Petro Kozak 0679876543`
Приклад: `delete-address Petro Kozak`
Приклад: `delete-email Petro Kozak new@kozak.com`

## 6–8. Нотатки
- `add-note <text>`  
Приклад: `add-note Buy milk and bread tomorrow morning`
Приклад: `add-note Prepare demo presentation for Neoversity`
- `search-notes <keyword>`
Приклад: `search-notes milk`
- `edit-note <id> <new text>`
Приклад: `edit-note 2 Buy milk, bread and eggs tomorrow`
- `delete-note <id>`
Приклад: `delete-note 1`
- `show-note <id>`
Приклад: `show-note 2`
- `show-notes`
Приклад: `show-notes`


## Загальні
- `all` — всі контакти
- `help` — цей список
- `exit` / `close` — зберегти і вийти