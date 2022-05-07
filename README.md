# Spanglish API
--------------
is an API created to help me learn the spanish language. It is the main backend that will contain all the words, sentences, and translations I learn every day. I can add, modify and get all words, sentences and their translations. The words and sentences will be categorized. The main language for the translation here is English. But it can also be another language. The goal of this backend is not to build a dictionary, but a tool with quizes that help me learn the language on my own way. It can have a front-end to fetch words or sentences, make questions and saves answers and results. The results can show me how my mistakes and which category can I improve my self in.
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
    Word: +word str
    Word: +category_id int
    Word: +created datetime

    class Verb
    Verb: +word_id int
    Verb: +yo str
    Verb: +tu str
    Verb: +el-ella-usted str
    Verb: +nosotros str
    Verb: +vosotros str
    Verb: +ellos-ellas-ustedes str
    Verb: +created datetime

    class Sentence
    Sentence: +id int
    Sentence: +category_id int
    Sentence: +sentence str
    Sentence: +created datetime
    
    class Translation
    Translation: +id int
    Translation: +word_id int
    Translation: +sentence_id int
    Translation: +language_id int
    Translation: +translation str
    Translation: +created datetime

    class PracticeResult
    PracticeResult: +id int
    PracticeResult: +word_id int
    PracticeResult: +sentence_id int
    PracticeResult: +attempts int
    PracticeResult: +user_id int
    PracticeResult: +created datetime


    Category "1" --> "many" Word
    Category "1" --> "many" Sentence
    Word "1" --> "1" Verb
    Translation "1" --> "many" Language
    Word "1" --> "many" Translation
    Sentence "1" --> "many" Translation
    User "1" --> "many" PracticeResult
    Word "many" <--> "many" PracticeResult
    Sentence "many" <--> "many" PracticeResult

```

## Usage
--------

- To start the app, first run the container:
  make start 
- To enter the container
  make bash
- To unittest the application
  make test
