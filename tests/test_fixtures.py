import logging

logger = logging.getLogger('fixtures')


def test_fixture_user(created_user):
    """check if the fixtures were created."""

    logger.debug(f"created_user: {created_user}")
    assert len(created_user) >= 3


def test_fixture_language(created_language):
    """check if the fixtures were created."""

    logger.debug(f"created_languages: {created_language}")
    assert len(created_language) >= 3


def test_fixture_category(created_category):
    """check if the fixtures were created."""

    logger.debug(f"created_category: {created_category}")
    assert len(created_category) >= 3


def test_fixture_word(created_word):
    """check if the fixtures were created."""

    logger.debug(f"created_word: {created_word}")
    assert len(created_word) >= 3


def test_fixture_verb(created_verb):
    """check if the fixtures were created."""

    logger.debug(f"created_verb: {created_verb}")
    assert len(created_verb) >= 2


def test_fixture_translation(created_translation):
    """check if the fixtures were created."""

    logger.debug(f"created_translation: {created_translation}")
    assert len(created_translation) >= 2


def test_fixture_quiz(created_quiz):
    """check if the fixtures were created."""

    logger.debug(f"created_quizes: {created_quiz}")
    assert len(created_quiz) >= 2


def test_fixture_quizquestion(created_quizquestion):
    """check if the fixtures were created."""

    logger.debug(f"created_quizquestions: {created_quizquestion}")
    assert len(created_quizquestion) >= 2


def test_fixture_quizresult(created_quizresult):
    """check if the fixtures were created."""

    logger.debug(f"created_quizresult: {created_quizresult}")
    assert len(created_quizresult) >= 2
