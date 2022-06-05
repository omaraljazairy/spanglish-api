import logging
from datetime import datetime, timedelta

logger = logging.getLogger('test')


def test_post_word_calle_success_201(client):
    """create a new word Calle. expect response 201."""

    response = client.post("/word/", json={
        "text": "Calle",
        "category_id": 2,
        "translations": [
            {
                'language_id': 1,
                'translation': "Street"
            }
        ]})
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_word_exists_409(client):
    """post an existing word, should get back 409 error"""

    response = client.post("/word/", json={
        "text": "Hablar",
        "category_id": 1,
        "translations": [
            {
                "language_id": 1,
                "translation": "talk"
            }
        ]
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_get_all_words_list_success(client):

    response = client.get("/word/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_get_word_by_category(client):
    """make a get request with the category_id, expect to get a response
    as a list with word and their translations."""

    response = client.get("/word/category_id/1/?limit=3&offset=0")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")
    logger.debug(f"total records: {len(data)}")

    assert response.status_code == 200
    assert len(data) == 3


def test_get_words_excluded_from_quiz_result(client):
    """expect words that are not from the current day."""

    one_day_ago = str(datetime.today() - timedelta(days=2))
    query = f"exclude_from_result_date={one_day_ago}&limit=5&offset=0"

    response = client.get(f"/word/category_id/1/?{query}")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")
    logger.debug(f"total records: {len(data)}")

    assert response.status_code == 200
    assert len(data) == 2


def test_get_word_by_id_with_verb(client):
    """provide a word id and expect a json response that contains the
    word, a list of translations and the verb pronounces."""

    response = client.get("/word/id/1/")
    expected_response = {
        'id': 1,
        'text': 'Hablar',
        'category_name': 'Verb',
        'translations': [
            {
                'language_name': 'English', 'translation': 'to speak'
            },
            {
                'language_name': 'English', 'translation': 'to talk'
            },
        ],
        'verb_pronounces': {
            'yo': 'Hablo',
            'tu': 'Hablas',
            'el_ella_usted': 'Habla',
            'nosotros': 'hablamos',
            'vosotros': 'hablais',
            'ellos_ellas_ustedes': 'hablan'
        }
    }

    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")
    logger.debug(f"total records: {len(data)}")

    assert response.status_code == 200
    assert data == expected_response


def test_get_word_by_id_without_verb(client):
    """provide a word id and expect a json response that contains the
    word, a list of translations and no verb."""

    response = client.get("/word/id/2/")
    expected_response = {
        'id': 2,
        'text': 'Jueves',
        'category_name': 'Day',
        'translations': [
            {
                'language_name': 'English', 'translation': 'Thursday'
            }
        ],
        'verb_pronounces': {}
    }

    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")
    logger.debug(f"total records: {len(data)}")

    assert response.status_code == 200
    assert data == expected_response


def test_patch_word_code_success(client):
    """update word with id 2 with category 1."""

    response = client.patch("/word/update/id/2/", json={"category_id": 1})
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_word_not_found_404(client):
    """update word with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/word/update/id/1000/", json={
        "text": "Hola"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_word_success(client):
    """delete word with id 6 and expect statuscode 204."""

    response = client.delete("/word/delete/id/6/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_word_not_found(client):
    """delete word with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/word/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
