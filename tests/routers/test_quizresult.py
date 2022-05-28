import logging

logger = logging.getLogger('test')


def test_post_quizresult_body_success_201(client):
    """create a new quizresult body. expect response 201."""

    response = client.post("/quizresult/", json={
        "quizquestion_id": 5,
        "attempts": 2,
        "user_id": 2
    })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_quizresult_non_existed_question_404(client):
    """post a non existing quizquestion, should get back 404 error"""

    response = client.post("/quizresult/", json={
        "quizquestion_id": 15,
        "attempts": 6,
        "user_id": 2
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_post_quizresult_non_existed_user_404(client):
    """post a non existing user, should get back 404 error"""

    response = client.post("/quizresult/", json={
        "quizquestion_id": 2,
        "attempts": 4,
        "user_id": 19
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_get_all_quizresults_list_success(client):

    response = client.get("/quizresult/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_patch_quizresult_attempts_success(client):
    """update quizresult with id 5 with new attempts."""

    response = client.patch(
        "/quizresult/update/id/5/",
        json={
            "attempts": 8
        })
    data = response.json()
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert data['attempts'] == 8


def test_patch_quizresult_not_found_404(client):
    """update quizresult with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/quizresult/update/id/1000/", json={
        "text": "Hola"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_quizresult_success(client):
    """delete quizresult with id 6 and expect statuscode 204."""

    response = client.delete("/quizresult/delete/id/6/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_quizresult_not_found(client):
    """delete quizresult with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/quizresult/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
