import logging

logger = logging.getLogger('test')


def test_post_translation_ir_success_201(client):
    """create a new translation ir. expect response 201."""

    response = client.post("/translation/", json={
        "word_id": 5,
        "language_id": 1,
        "translation": "to go"
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_translation_exists_409(client):
    """post an existing translation, should get back 409 error"""

    response = client.post("/translation/", json={
        "word_id": 1,
        "language_id": 1,
        "translation": "to talk"
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_get_all_translations_list_success(client):

    response = client.get("/translation/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_patch_translation_code_success(client):
    """update translation_id 2 with a different translation."""

    response = client.patch("/translation/update/id/3/", json={
        "translation": "Wednesday"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_translation_not_found_404(client):
    """update translation with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/translation/update/id/1000/", json={
        "text": "Hola"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_translation_success(client):
    """delete translation with id 4 and expect statuscode 204."""

    response = client.delete("/translation/delete/id/4/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_translation_not_found(client):
    """delete translation with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/translation/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
