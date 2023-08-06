import sys, os

sys.path.append(os.getcwd() + "/gus")

import __main__, args, const, out, urls

STATUS = {"url": "test", "code": 400, "desc": "FAIL"}


def test_std_output():
    assert out.std_format(STATUS) == "[FAIL] [400] test"


def test_json_output():
    assert out.json_format(STATUS) == '{"url": \'test\', "status": 400}'


def test_rtf_output():
    assert out.rtf_format(STATUS) == "\cf3 [400] [FAIL] test"


def test_get_status_good():
    status = urls.get_status("https://realpython.com/python-testing/")
    assert status["desc"] == "GOOD"


def test_get_status_fail():
    status = urls.get_status("http://badbad.bad")
    assert status["desc"] == "FAIL"


class TestCheckNested:
    def test_one(self):
        assert urls.check_nested("[http://test.com]") == "http://test.com"

    def test_two(self):
        assert urls.check_nested("http://test.com]") == "http://test.com]"

    def test_three(self):
        assert urls.check_nested("[http://test.com]]") == "http://test.com]"
