
import pytest
import unittest.mock as mock

from acondbs.misc import githubauth

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def mock_requests(monkeypatch):
    y = mock.Mock()
    monkeypatch.setattr("acondbs.misc.githubauth.requests", y)
    yield y


##__________________________________________________________________||
def test_success(app, mock_requests):

    token = 'token-xxx'

    viewer = {
        "login": "octocat",
        "name": "monalisa octocat",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif"
    }
    r = {'data': {'viewer': viewer}}

    mock_requests.post().json.return_value = r
    with app.app_context():
        user = githubauth.get_user(token)

    assert viewer == user

##__________________________________________________________________||
def test_error(app, mock_requests):

    token = 'token-xxx'

    r = {'message': 'Bad credentials', 'documentation_url': 'https://docs.github.com/graphql'}
    mock_requests.post().json.return_value = r
    with app.app_context():
        user = githubauth.get_user(token)

    assert user is None

##__________________________________________________________________||
