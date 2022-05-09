import logging

from datamodels import models

logger = logging.getLogger('fixtures')


def test_fixture_language(db, create_language):

    create_language
    languages = db.query(models.Language).all()
    logger.debug(f'language : {languages} - {len(languages)}')
    for lan in languages:
        logger.debug(f"language {lan.id} - {lan.code}")

    assert len(languages) == 3
