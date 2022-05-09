import logging
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from services.database import Base


logger = logging.getLogger('models')


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(50), unique=True)
    fullname = Column(String(30), nullable=False)
    created = Column(DateTime, default=datetime.now())

    practice_result = relationship("PracticeResult", back_populates="user")


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


class Word(Base):
    __tablename__ = "Word"

    id = Column(Integer, primary_key=True)
    word = Column(String(15), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey(
        'Category.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=False)
    created = Column(DateTime, default=datetime.now())


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


class Sentence(Base):
    __tablename__ = "Sentence"

    id = Column(Integer, primary_key=True)
    sentence = Column(String(255), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey(
        'Category.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=False)
    created = Column(DateTime, default=datetime.now())


class Translation(Base):
    __tablename__ = "Translation"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(
        'Word.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=True,
        index=True)
    sentence_id = Column(Integer, ForeignKey(
        'Sentence.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=True,
        index=True)
    language_id = Column(Integer, ForeignKey(
        'Language.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        index=True)
    translation = Column(String(255), nullable=False)
    created = Column(DateTime, default=datetime.now())

    language = relationship("Language", back_populates="translation")


class PracticeResult(Base):
    __tablename__ = "PracticeResult"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(
        'Word.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=True,
        index=True)
    sentence_id = Column(Integer, ForeignKey(
        'Sentence.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'),
        nullable=True,
        index=True)
    attempts = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey(
        'User.id',
        ondelete='RESTRICT',
        onupdate='CASCADE'))
    created = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="practice_result")
