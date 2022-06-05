import logging
from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime,
                        UniqueConstraint, Boolean, Table)
from sqlalchemy.orm import relationship
from datetime import datetime
from services.database import Base
from typing import Dict


logger = logging.getLogger('models')


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(50), unique=True)
    fullname = Column(String(30), nullable=False)
    created = Column(DateTime, default=datetime.now())

    quiz_result = relationship("QuizResult", back_populates="user")


class Language(Base):
    __tablename__ = "Language"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, nullable=False)
    code = Column(String(2), index=True, nullable=False)
    created = Column(DateTime, default=datetime.now())

    translation = relationship("Translation", back_populates="language")

class Category(Base):
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, nullable=False)
    created = Column(DateTime, default=datetime.now())


word_translation = Table(
    "Word_Translation",
    Base.metadata,
    Column("word_id", ForeignKey('Word.id'), primary_key=True),
    Column("translation_id", ForeignKey('Translation.id'), primary_key=True)
)


class Word(Base):
    __tablename__ = "Word"

    id = Column(Integer, primary_key=True)
    text = Column(String(255), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey(
        'Category.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=False)
    created = Column(DateTime, default=datetime.now())
    translations = relationship("Translation", secondary="Word_Translation", back_populates='word')
    category = relationship("Category")

    verb = relationship("Verb", back_populates='word')


    @property
    def category_name(self) -> str:
        """return the category name. """

        return self.category.name

    @property
    def verb_pronounces(self) -> Dict[str, str]:
        """returns all the verb pronounces that belong to the word if the
        category is a verb, otherwise return an empty dict."""

        if not self.verb:
            return {}

        # convert the verb sqlalchemy.orm.collections.InstrumentedList
        # to a python list. It will always have one element. convert
        # the verb object into a dict and return it.
        verb_obj = list(self.verb)[0].__dict__

        return verb_obj


class Verb(Base):
    __tablename__ = "Verb"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(
        'Word.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'))
    yo = Column(String(15), nullable=True)
    tu = Column(String(15), nullable=True)
    el_ella_usted = Column(String(15), nullable=True)
    nosotros = Column(String(15), nullable=True)
    vosotros = Column(String(15), nullable=True)
    ellos_ellas_ustedes = Column(String(15), nullable=True)
    created = Column(DateTime, default=datetime.now())

    word = relationship("Word", back_populates='verb')


class Translation(Base):
    __tablename__ = "Translation"

    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey(
        'Language.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        index=True)
    translation = Column(String(255), nullable=False)
    created = Column(DateTime, default=datetime.now())

    language = relationship("Language", back_populates="translation")
    word = relationship("Word", secondary="Word_Translation", back_populates='translations')

    @property
    def language_name(self) -> str:
        """returns the language name."""

        return self.language.name


class QuizResult(Base):
    __tablename__ = "QuizResult"

    id = Column(Integer, primary_key=True)
    quizquestion_id = Column(Integer, ForeignKey(
        'QuizQuestion.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=False,
        index=True)
    attempts = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey(
        'User.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'))
    created = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="quiz_result")
    quiz_question = relationship("QuizQuestion", back_populates="quiz_result")



class Quiz(Base):
    __tablename__ = "Quiz"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    active = Column(Boolean, default=1, index=True)
    created = Column(DateTime, default=datetime.now())


class QuizQuestion(Base):
    __tablename__ = "QuizQuestion"
    __table_args__ = (UniqueConstraint('word_id', 'quiz_id', name="unique_word_quiz"),)

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(
        'Word.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=False,
        index=True)
    quiz_id = Column(Integer, ForeignKey(
        'Quiz.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=False,
        index=True)        
    question = Column(String(255), nullable=True)
    created = Column(DateTime, default=datetime.now())

    quiz_result = relationship("QuizResult", back_populates="quiz_question")
    quiz_word = relationship("Word")
