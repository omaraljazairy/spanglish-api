import logging

logger = logging.getLogger('test')


def test_post_quizquestion_body_success_201(client):
    """create a new quizquestion body. expect response 201."""

    response = client.post("/quizquestion/", json={
        "quiz_id": 2,
        "word_id": 3,
        "question": "Who said"
    })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_quizquestion_without_question_success_201(client):
    """create a new quizquestion without the question. expect
    it to have the default question and response 201.
    """

    response = client.post("/quizquestion/", json={
        "quiz_id": 3,
        "word_id": 5
    })
    response_data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response_data}")

    assert response.status_code == 201
    assert response_data['question'] == 'What is the meaning of'


def test_post_quizquestion_exists_409(client):
    """post an existing quizquestion, should get back 409 error"""

    response = client.post("/quizquestion/", json={
        "quiz_id": 1,
        "word_id": 1
        })
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_get_all_quizquestions_list_success(client):

    response = client.get("/quizquestion/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_patch_quizquestion_question_success(client):
    """update quizquestion with id 5 with new question."""

    response = client.patch(
        "/quizquestion/update/id/5/",
        json={
            "question": 'How to understand latinas'
        })
    data = response.json()
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert data['question'] == 'How to understand latinas'


def test_patch_quizquestion_not_found_404(client):
    """update quizquestion with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/quizquestion/update/id/1000/", json={
        "text": "Hola"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_quizquestion_success(client):
    """delete quizquestion with id 6 and expect statuscode 204."""

    response = client.delete("/quizquestion/delete/id/6/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_quizquestion_not_found(client):
    """delete quizquestion with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/quizquestion/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
