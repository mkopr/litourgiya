**litourgiya app**  

[TOC]

Description
=
Service
-
Service that allows to get/edit/delete info about Church Calendar:  
- calendar info - date, season, season week, weekday  
- celebrations info - title, colour, rank, rank number

Exercise
-
```text  
Zadanie:  
- we Flasku, api restowe  x
- Będzie korzystało z API: http://calapi.inadiutorium.cz/api-doc  
- Mock logowania: wystarczy podać username żeby zidentyfikować użytkownika  
- Request przyjmujący przedział dat. Dla danego przedziału uruchamiane jest asynchroniczne zadanie, które pobiera i zapisuje do bazy danych listę dni liturgicznych (ze wspomnianego API). Lista jest powiązana z użytkownikiem. Ten sam użytkownik może w dwóch różnych requestach podać przedziały, którę będą miały część wspólną - musimy zadbać o brak duplikatów.  
- Request do zwracania listy powiązanych z danym użytkownikiem dni, z filtrowaniem (po przedziale dat, po weekdayu, po kolorze obowiązujących szat liturgicznych), obsługa paginacji  
- Musimy założyć, że dane pobierane z API są nieprawidłowe, więc musimy mieć requesta, który będzie mógł te dane edytować  
- Endpoint, który zwraca losowy dzień z listy zapisanych dla danego użytkownika  
- Endpoint, który pozwala usunąć wszystkie dane powiązane z danym użytkownikiem  
- Całość powinna dać się łatwo uruchomić na (w miarę) dowolnym innym sprzęcie z systemem UNIXowym (najlepiej Docker/docker-compose, może być dokładna instrukcja uruchomienia)  
```

Dev setup
=
Install `pip-tools` then run `pip-sync requirements*.txt`.

How to run
=
```bash  
docker-compose up --build  
```

How to check PEP8 & imports
=
```bash  
docker build -t test_image -f Dockerfile-test .  
docker run --rm test_image flake8 /litourgiya  
docker run --rm test_image flake8 /test  
```

Endpoints
=
/api/login
-
**Method POST**
>To login user pass in request body userrname  
>**Body**: `{"Username":"your_name"}`  
>**Responses**:  
>- HTTP 200 OK -> `{"message": "your_name exists in db"}`
>- HTTP 201 CREATED -> `{"message": "created user: your_name"}`
>- HTTP 400 BAD REQUEST -> serializer errors

/api/download
-
**Method GET**
> Get data from outside api and put it to celery task and convert to database objects  
>**Header**:  `Authorization: Username your_name`  
>**Responses**:  
>- HTTP 200 OK -> `{"message": "Download triggered for dates: start=2017-08-02', end=2018-09-03"}`
>- HTTP 400 BAD REQUEST -> serializer errors
>- HTTP 401 UNAUTHORIZED

/api/search
-
**Method GET**
>Get all data related with user  
>**Header**:  `Authorization: Username your_name`  
>**Params with examples**:  
>- start=2018-08-12
>- end=2018-09-12
>- weekday=monday
>- color=white
>- page=2
>- size=50
>**Responses**: 
>- HTTP 200 OK -> `{
    "count": 1,
    "size": 20,
    "page": 1,
    "data": [
        {
            "user": 1,
            "id": 1,
            "celebrations": [
                {
                    "colour": "green",
                    "rank_num": 2.6,
                    "rank": "Sunday",
                    "id": 1,
                    "calendar": 1,
                    "title": "13th Sunday in Ordinary Time"
                }
            ],
            "season_week": 13,
            "weekday": "sunday",
            "date": "2018-07-01T00:00:00+00:00",
            "season": "ordinary"
        },
        {
            "user": 1,
            "id": 2,
            "celebrations": [
                {
                    "colour": "green",
                    "rank_num": 3.13,
                    "rank": "ferial",
                    "id": 2,
                    "calendar": 2,
                    "title": "Monday, 13th week in Ordinary Time"
                }
            ],
            "season_week": 13,
            "weekday": "monday",
            "date": "2018-07-02T00:00:00+00:00",
            "season": "ordinary"
        }]`
>- HTTP 400 BAD REQUEST -> serializer errors
>- HTTP 401 UNAUTHORIZED

**Method PUT**
>Edit data related with user.  
>To edit calendar set correct date in request body  
>To edit celebration set corrent ID in request body.  
>**Header**:  `Authorization: Username your_name`  
>**Body**: `{"weekday": "thursday", "date": "2018-08-02", "season_week": 17, "celebrations": [ { "calendar": 9, "rank": "ferial", "rank_num": 3.13, "colour": "green", "id": 15, "title": "Thursday, 17th week in Ordinary Time" }, { "calendar": 9, "rank": "optional memorial", "rank_num": 3.12, "colour": "white", "id": 16, "title": "The most Saint Eusebius of Vercelli, bishop" }, ], "season": "non-ordinary"}`  
>**Responses**:  
>- HTTP 200 OK
>- HTTP 400 BAD REQUEST -> serializer errors
>- HTTP 401 UNAUTHORIZED
>- HTTP 404 NOT FOUND

**Method DELETE**
>Delete all related with user calendars and celebrations  
>**Header**:  `Authorization: Username your_name`  
>**Responses**:  
>- HTTP 200 OK
>- HTTP 400 BAD REQUEST
>- HTTP 401 UNAUTHORIZED

/api/random
-
**Method GET**
>Get one random object related with user  
>**Header**:  `Authorization: Username your_name`  
>**Responses**:  
>- HTTP 200 OK -> `{
    "date": "2018-02-19T00:00:00+00:00",
    "season_week": 1,
    "weekday": "monday",
    "season": "lent",
    "celebrations": [
        {
            "title": "Monday, 1st week of Lent",
            "rank_num": 2.9,
            "calendar": 267,
            "id": 360,
            "colour": "violet",
            "rank": "ferial"
        }
    ],
    "id": 267,
    "user": 1
}`
>- HTTP 401 UNAUTHORIZED

   
