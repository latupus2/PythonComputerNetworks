# Task6: Askona parser
Парсер вырезан. База данных и обработчик запросов разделены на два контейнера. Используется nginx для перенаправления запросов с 80 порта. Добавлена блокировка российских ip. Создание тоннеля через Localtunnel.

---
## Запуск
 1. Создание сети
  ```
  docker network create askona_network
  ```
 2. Запускаем контейнер с PostgreSQL
  ```
  docker run -d --name db --network askona_network -e POSTGRES_USER=askona_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=askona_parser -p 5432:5432 postgres:13
  ```
 3. Собираем образ приложения
  ```
  docker build -t url_saver_app . -f dockerfile_app .
  ```
 4. Запускаем контейнер приложения
  ```
  docker run -d --name app --network askona_network -p 5000:5000 url_saver_app
  ```
 5. Собираем образ Nginx
  ```
  docker build -t my-nginx -f dockerfile_nginx . 
  ```
 6. Запускаем контейнер Nginx
  ```
  docker run -d -p 80:80 --name my-nginx-container --network askona_network my-nginx
  ```
 7. Генерация ссылки
  ```
  lt -p 80
  ``` 
  
---
## Использование
 1. Сохранение ссылки
  ```
  curl "http://localhost/save_url?url=YOUR_URL"
  ```
 2. Получение ссылок из БД
  ```
  curl "http://localhost/get_urls"
  ```  

 Можно использовать адресную строку вашего браузера.  
 Для дополнительной информации можно перейти по `http://localhost/docs`

---