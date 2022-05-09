import logging

logger = logging.getLogger('test')


def test_get_main_success_200(client):

    response = client.get("/")
    logger.debug(f"response: {response}")

    assert response.status_code == 200
