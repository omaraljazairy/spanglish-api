import logging

logger = logging.getLogger('test')


def test_post_quiz_body_success_201(client):
    """create a new quiz body. expect response 201."""

    response = client.post("/quiz/", json={
        "title": "Body",
        "active": 1,
        "user_id": 1})
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_quiz_without_active_success_201(client):
    """create a new quiz without the active param. expect
    it to be true by default response 201.
    """

    response = client.post("/quiz/", json={
        "title": "Something",
        "user_id": 1})

    response_data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response_data}")

    assert response.status_code == 201
    assert response_data['active']


def test_post_quiz_exists_409(client):
    """post an existing quiz, should get back 409 error"""

    response = client.post("/quiz/", json={
        "title": "Days",
        "active": 1,
        "user_id": 1
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_get_all_quizs_list_success(client):
    """expect a list of quizzes objects. the first object should be the
    same as the expected object."""

    response = client.get("/quiz/all/")
    data = response.json()
    expected = {
        "id": 1,
        "title": "Verbs",
        "active": True,
        "created": "2022-06-01T00:00:00",
        "questions": [
            {
                'question': 'what is the meaning of',
                'word_text': 'Hablar',
                'active': True
            }
        ]
    }

    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2
    assert data[0] == expected


def test_patch_quiz_title_success(client):
    """update quiz with id 2 with title months."""

    response = client.patch("/quiz/update/id/2/", json={"title": 'occupation'})
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_quiz_deactivate_success(client):
    """update quiz with id 3 with title months."""

    response = client.patch("/quiz/update/id/3/", json={"active": 0})
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_quiz_not_found_404(client):
    """update quiz with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/quiz/update/id/1000/", json={
        "text": "Hola"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_quiz_success(client):
    """delete quiz with id 6 and expect statuscode 204."""

    response = client.delete("/quiz/delete/id/6/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_quiz_not_found(client):
    """delete quiz with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/quiz/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
