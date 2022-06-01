import logging

logger = logging.getLogger('test')


def test_post_word_calle_success_201(client):
    """create a new word Calle. expect response 201."""

    response = client.post("/word/", json={
        "text": "Calle",
        "category_id": 2,
        "translation": [
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
        "translation": [
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


def test_get_word_by_category_translation(client):
    """make a get request with the category_id, expect to get a response
    as a list with word and their translations."""

    response = client.get("/word/category_id/1/limit/3/offset/0/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


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
