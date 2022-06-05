# Spanglish API
--------------
is an API created to help me learn the spanish language. It is the main backend that will contain all the words (text) and translations I learn every day. I can add, modify and get all words or sentences and their translations. The spanish texts will be categorized. The main language for the translation here is English. But it can also be another language. The goal of this backend is not to build a dictionary, but a tool with quizes that help me learn the language on my own way. It can have a front-end to fetch spanish texts, make questions and saves answers and results. The results can show me how my mistakes and which category can I improve my self in.
This api is built using Python FastAPI.

## Changelogs
All change logs can be found [here](CHANGELOG.md)

## Authors
Omar Aljazairy: omar@fedal.nl

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
    Word "many" <--> "many" QuizResult
    Quiz "1" --> "many" QuizQuestion
    QuizQuestion "many" <--> "many" QuizResult

```

## Usage
--------

- To start the app, first run the container:
  make start 
- To enter the container
  make bash
- To unittest the application
  make test
