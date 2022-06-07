# Spanglish API
--------------
This API is used as a backend system where Spanish words or sentences can be added and translated. It supports creating quizzes with quiz questions existing from the Spanish words. The results of the quizzes can be added here and fetched. 
Any interface can use it as a backend.
This api is built using Python 3.9 and FastAPI with PostgreSQL as a database.

## Usage & endpoints
--------------------
- /language/ : post, get, patch and delete a language that will be used for the translation.
- /category/ : post, get and patch categories. each word text will have a category, for example Days, Months, Verbs, ... etc.
- /word/ : post, get and patch Spanish texts. Each word has a category linked to it.
- /verb/ : post, get and patch a verb pronounce. A verb is linked to a word that has to have the category `Verb`. 
- /translation/ : post, get and patch a translation for each word. Each word can have multiple translations from different languages.
- /quiz/ : post, get and patch a quiz. A Quiz will have a title and questions linked to it.
- /quizquestion/ :post, get and patch a question that contains a word + a text for the question. each question is belongs to a quiz.
- /quizresult/ :post, get and patch quizresult by providing the question, the user_id and the number of attempts.
- /user/ :post, get and patch users. Users are ment to take the quiz questions.

## Changelogs
All change logs can be found [here](CHANGELOG.md)

## Class Diagram
----------------

```mermaid
classDiagram
    class User
    User: +id int
    User: +username str
    User: +password str
    User: +email str
    User: +fullname str
    User: +created datetime

    class Language
    Language: +id int
    Language: +name str
    Language: +code str
    Language: +created datetime

    class Category
    Category: +id int
    Category: +name str
    Category: +created datetime

    class Word
    Word: +id int
    Word: +text str
    Word: +category_id int
    Word: +created datetime
    Word: +category_name() str
    Word: +verb_pronounces() dict

    class Verb
    Verb: +word_id int
    Verb: +yo str
    Verb: +tu str
    Verb: +el-ella-usted str
    Verb: +nosotros str
    Verb: +vosotros str
    Verb: +ellos-ellas-ustedes str
    Verb: +created datetime
    
    class Translation
    Translation: +id int
    Translation: +language_id int
    Translation: +translation str
    Translation: +created datetime

    class Quiz
    Quiz: +id int
    Quiz: +title str
    Quiz: +active bool
    Quiz: +created datetime

    class QuizQuestion
    QuizQuestion: +id int
    QuizQuestion: +word_id int
    QuizQuestion: +quiz_id int
    QuizQuestion: +question str
    QuizQuestion: +created datetime

    class QuizResult
    QuizResult: +id int
    QuizResult: +quizquestion_id int
    QuizResult: +attempts int
    QuizResult: +user_id int
    QuizResult: +created datetime


    Category "1" --> "many" Word
    Word "1" --> "1" Verb
    Translation "1" --> "many" Language
    Word "many" <--> "many" Translation
    User "1" --> "many" QuizResult
    Word "many" <--> "many" QuizQuestion
    Quiz "1" --> "many" QuizQuestion
    QuizQuestion "many" <--> "many" QuizResult

```

## Setup & Installation
--------
1. The application is running on a docker container. To run all the containers, you need to create an .env file that will contain the following sample data:
```
 DB_USER=user
 DB_PASSWORD=pass
 DB_HOST=171.28.0.2
 DB_PORT=3306
 DB_DATABASE=Language
 ENVIRONMENT=dev
```
2. Place the ***.env*** file in the root of the project. the same place where the Dockerfile and docker-compose.yml are placed.
3. Execute the command **make start** to build and run the docker containers.
4. To run the FastAPI server, execute the command **make run**. This will run the application and create the database.
5. To enter the container, execute the command **make bash** .
6. To access the API and see the docs, go to **http://0.0.0.0:8005/redoc** or **http://0.0.0.0:8005/docs** .
7. To run unittests, execute the command **make test**

## Authors
Omar Aljazairy: omar@fedal.nl
