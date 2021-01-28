import pytest
import requests_mock

from howfairis import Repo, Config, Checker
from howfairis.Compliance import Compliance
from howfairis.Readme import Readme


@pytest.fixture
def badghurl_checker():
    repo = Repo('https://github.com/fair-software/does-not-exist')
    config = Config(repo)

    with requests_mock.Mocker() as m:
        m.get('https://raw.githubusercontent.com/fair-software/does-not-exist/master/README.md', status_code=404)
        m.get('https://raw.githubusercontent.com/fair-software/does-not-exist/master/README.rst', status_code=404)
        checker = Checker(config, repo)
        return checker


def test_checker_badghurl_emptyreadme(badghurl_checker: Checker):
    readme = badghurl_checker.readme

    expected = Readme(filename=None, text=None, fmt=None)
    assert readme == expected


def test_checker_check_five_recommendations(badghurl_checker: Checker):
    compliance = badghurl_checker.check_five_recommendations().compliance

    expected = Compliance(repository=False, license_=False, registry=False, citation=False, checklist=False)
    assert compliance == expected
