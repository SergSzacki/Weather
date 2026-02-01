# Программа "Погода" v:2.0

## Описание

Это веб-приложение на FastAPI, которое показывает текущую погоду для различных городов.

## Развертывание

Приложение развернуто через Yandex Cloud Serverless Containers с использованием CI/CD из SourceCraft.

## CI/CD Pipeline

Этот проект использует встроенный CI/CD от SourceCraft для автоматического развертывания в Yandex Cloud при каждом изменении в ветке `main`.

### Настройка CI/CD

Для работы CI/CD необходимо настроить следующие secrets в настройках репозитория:

1. `YC_REGISTRY_ID` - ID реестра в Yandex Container Registry
2. `YC_FOLDER_ID` - ID каталога в Yandex Cloud
3. `YC_SA_KEY` - ключ сервисного аккаунта с правами на работу с Container Registry и Serverless Containers

### Создание сервисного аккаунта в Yandex Cloud

1. Перейдите в [консоль Yandex Cloud](https://console.cloud.yandex.ru/)
2. Выберите ваш каталог
3. Перейдите в раздел "Сервисные аккаунты"
4. Создайте новый сервисный аккаунт с именем `weather-app-ci`
5. Назначьте ему роли:
   - `container-registry.images.pusher` - для загрузки образов в реестр
   - `serverless.containers.functionCall` - для управления Serverless Containers
6. Создайте ключ для сервисного аккаунта и сохраните его как `YC_SA_KEY` в secrets репозитория

### Настройка Container Registry

1. Перейдите в раздел "Container Registry"
2. Создайте реестр для хранения образов приложения
3. Сохраните ID реестра как `YC_REGISTRY_ID` в secrets репозитория
4. Убедитесь, что сервисный аккаунт имеет доступ к реестру

### Запуск CI/CD

Pipeline запускается автоматически при каждом push в ветку `main`. Также можно запустить вручную:

1. Перейдите в раздел CI/CD репозитория в SourceCraft
2. Выберите workflow "Deploy to Yandex Cloud"
3. Нажмите "Запустить" и при необходимости укажите тег образа

### Что делает CI/CD pipeline

1. Собирает Docker-образ приложения
2. Загружает образ в Yandex Container Registry
3. Обновляет Yandex Serverless Container с новым образом
4. Приложение становится доступно по публичному URL контейнера