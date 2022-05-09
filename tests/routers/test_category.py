import logging

logger = logging.getLogger('test')


def test_post_category_months_success_201(client):
    """create a new category Months. expect response 201."""

    response = client.post("/category/", json={"name": "Months"})
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 201


def test_post_category_exists_409(client):
    """post an existing category, should get back 409 error"""

    response = client.post("/category/", json={"name": "Verb"})
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 409


def test_get_all_categories_list_success(client):

    response = client.get("/category/all/")
    data = response.json()
    logger.debug(f"response: {response}")
    logger.debug(f"response content: {data}")

    assert response.status_code == 200
    assert len(data) >= 2


def test_patch_category_code_success(client):
    """update category with id 2 with with name Season."""

    response = client.patch("/category/update/id/2/", json={
        "name": "Season"
        }
    )
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 200


def test_patch_category_not_found_404(client):
    """update category with non existing id 1000. expect statuscode 404
    not found."""

    response = client.patch("/category/update/id/1000/", json={
        "name": "Country"
        })
    logger.debug(f"response from update: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404


def test_delete_category_success(client):
    """delete category with id 3 and expect statuscode 204."""

    response = client.delete("/category/delete/id/3/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 204


def test_delete_category_not_found(client):
    """delete category with unknown id 6666 and expect statuscode 404."""

    response = client.delete("/category/delete/id/6666/")
    logger.debug(f"response from delete: {response}")
    logger.debug(f"response content: {response.content}")

    assert response.status_code == 404
