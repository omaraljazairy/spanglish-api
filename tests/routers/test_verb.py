import logging

logger = logging.getLogger('test')


def test_post_verb_ir_success_201(client):
    """create a new verb ir. expect response 201."""

    response = client.post("/verb/", json={
            "word_id": 5,
            "yo": "voy",
            "tu": "vas",
            "el_ella_usted": "va",
            "nosotros": "vamos",
            "vosotros": "vais",
            "ellos_ellas_ustedes": "van"
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_verb_exists_409(client):
    """post an existing verb, should get back 409 error"""

    response = client.post("/verb/", json={
        "word_id": 1,
        "yo": "hablo",
        "tu": "hablas",
        "el_ella_usted": "habla",
        "nosotros": "hablamos",
        "vosotros": "hablais",
        "ellos_ellas_ustedes": "hablan"
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_post_verb_non_verb_category_400(client):
    """
    post a verb but the category of the word is not verb,
    should get back 400 error.
    """

    response = client.post("/verb/", json={
        "word_id": 2,
        "yo": "hablo",
        "tu": "hablas",
        "el_ella_usted": "habla",
        "nosotros": "hablamos",
        "vosotros": "hablais",
        "ellos_ellas_ustedes": "hablan"
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 400


def test_get_all_verbs_list_success(client):

    response = client.get("/verb/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_patch_verb_yo_success(client):
    """update verb with id 2 with pronouns yo to foo."""

    response = client.patch("/verb/update/id/2/", json={"yo": "foo"})
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_verb_not_found_404(client):
    """update verb with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/verb/update/id/1000/", json={
        "yo": "baro"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_verb_success(client):
    """delete verb with id 3 and expect statuscode 204."""

    response = client.delete("/verb/delete/id/2/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_verb_not_found(client):
    """delete verb with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/verb/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
