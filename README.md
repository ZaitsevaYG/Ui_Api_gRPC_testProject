<h1> Проект по тестированию демо-проекта "Tool Shop"</h1>

![This is an image](src/tool_shop/data/rm_data/Tool_Shop_page.png)

Проект основан на учебном приложении <a href="https://github.com/testsmith-io/practice-software-testing.git">TestSmith Practice Software Testing</a> - интернет-магазине инструментов с трёхслойной архитектурой (UI + REST API + gRPC).
## Запуск приложения
### Требования
|  Компонент       | Версия     |              Установка              |
|:-----------------|:----------:|:-----------------------------------:|
| Docker           | 20.10+     | https://www.docker.com/get-started  |
| Docker Compose   | 2.0+       |   Входит в состав Docker Desktop    |
| Python           | 3.10+      |  https://www.python.org/downloads/  |
| Poetry           | 1.6+       |         pip install poetry          |

### Запуск тестируемого приложения

Клонируем официальный репозиторий приложения
```bash
git clone https://github.com/testsmith-io/practice-software-testing.git
cd practice-software-testing
```
Запускаем все сервисы через Docker Compose
```bash
docker-compose up -d
```

### Проверка работоспособности
| Сервис       |                       URL                        |                Описание                 |
|:-------------|:------------------------------------------------:|:---------------------------------------:|
| UI           |              http://localhost:4200               |         Веб-интерфейс магазина          |
| API Docs     |     http://localhost:8091/api/documentation      |      Swagger UI для REST API            |
| gRPC         |          http://localhost:50051                  | gRPC endpoint (проверяется через тесты) |

### Настройка тестового окружения
```bash
# Вернись в папку с тестами
cd ../Tool_shop

# Установи зависимости через Poetry
poetry install

# Активируй виртуальное окружение
poetry shell
```