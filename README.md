# HW_18-19_Blog  
Practical work  
====================================  
ДЗ 18. Практическая работа
Заняття 19. Auth, register and profile page with django class based views, Abstract and Proxy, Django settings, 
admin action, messages, context processor

Ожидаю ссылку на репозиторий и ссылку на задеплоенный проект (если сделали эту опцию)  

Тех задание:  
Блог (опять).  

Функционал:  
Пользователь может зарегистрироваться + логин/логаут  
Пользователь может создавать посты (login required)  
Пользователь может публиковать посты или убирать их в заготовки (пользователь может их позже опубликовать)  
Пользователь может изменять свои посты (login required, filter(owner=...))  
Анонимные пользователи могут публиковать комментарии  
Комментарии модерируется перед публикацией (поле is_published + admin page)  
Администратор получает уведомление на почту о новом посте или комментарии (в консоль)  
Пользователь получает уведомление о новом комментарии под постом с сылкой на пост (консоль) 
(начните с того что бы  email отправлялся при создании комментария)  
Есть страница с списком всех постов  
Есть страница с списком постов пользователя  
Есть страница поста  
Есть страница профиля публичная  
Есть профиль в котором можно изменять свои данные  
Пагинация постов и комментариев  
У поста есть заголовок, краткое описание, картинка (опционально ссылка на изображение или реальный файл изображения) 
и полное описание  
У комментария есть юзернейм и текст (просто два текстовых поля)  
Фикстуры loremipsum  
Админка с функционалом  
Форма обратной связи с админом (в консоль)  
Темплейты с стилизацией  
Разные настройки для разработки и продакшена  
Оптимизация запросов в базу  
Кеширование  
Селери  
Pythonanywhere или Heroku или DigitalOcean или что угодно - развернуть в продашкене 
(без кеширования и бэкграунд задач) **  

пункты с ** опциональны, но желательны - реализацию селери и кеширования можно выполнить в отдельной ветке 
что бы при деплое на продкшен они не использовались  
больше инструкций найдете тут - https://djangogirls.org/resources/  
учтите что на Pythonanywhere (и на других) - redis и celery не заработают (их нужно настраивать отдельно).  
==================================