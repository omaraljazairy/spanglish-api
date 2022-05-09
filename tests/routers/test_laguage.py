import logging

logger = logging.getLogger('test')


def test_post_language_fr_success_201(client):
    """create a new language FR. expect response 201."""

    response = client.post("/language/", json={
        "name": "French",
        "code": "FR"})
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_language_exists_409(client):
    """post an existing language, should get back 409 error"""

    response = client.post("/language/", json={
        "name": "English",
        "code": "EN"
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_get_all_languages_list_success(client):

    response = client.get("/language/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_patch_language_code_success(client):
    """update language with id with code DE."""

    response = client.patch("/language/update/id/2/", json={"code": "DE"})
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_language_not_found_404(client):
    """update language with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/language/update/id/1000/", json={
        "name": "A Language"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_language_success(client):
    """delete language with id 3 and expect statuscode 204."""

    response = client.delete("/language/delete/id/3/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_language_not_found(client):
    """delete language with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/language/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
