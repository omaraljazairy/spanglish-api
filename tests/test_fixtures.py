import logging

logger = logging.getLogger('fixtures')


def test_fixture_language(created_language):
    """check if the fixtures were created."""

    logger.debug(f"created_languages: {created_language}")
    assert len(created_language) == 3


def test_fixture_category(created_category):
    """check if the fixtures were created."""

    logger.debug(f"created_category: {created_category}")
    assert len(created_category) == 3


def test_fixture_word(created_word):
    """check if the fixtures were created."""

    logger.debug(f"created_word: {created_word}")
    assert len(created_word) == 3
