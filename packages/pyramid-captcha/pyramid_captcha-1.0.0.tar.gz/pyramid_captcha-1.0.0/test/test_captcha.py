# -*- coding: utf-8 -*-
import filetype
import pytest
from captcha.image import ImageCaptcha
from pyramid.testing import DummyRequest

from pyramid_captcha import Captcha
from pyramid_captcha.exception import CaptchaError, CaptchaMissingError, CaptchaMismatchError


def test_init(mock_request):
    captcha = Captcha(mock_request)
    assert isinstance(captcha._request, DummyRequest)
    assert isinstance(captcha._captcha, ImageCaptcha)
    assert captcha._session_key == 'captcha'
    assert captcha._form_key == 'captcha'
    assert captcha._length == 6


def test_init_with_custom_keys(mock_request):
    captcha = Captcha(mock_request, session_key='foo', form_key='bar')
    assert isinstance(captcha._request, DummyRequest)
    assert isinstance(captcha._captcha, ImageCaptcha)
    assert captcha._session_key == 'foo'
    assert captcha._form_key == 'bar'


def test_generate(mock_request):
    captcha = Captcha(mock_request)
    response = captcha.generate()
    assert filetype.guess_mime(bytearray(response.body)) == 'image/png'
    assert isinstance(mock_request.session[captcha._session_key], str)
    assert len(mock_request.session[captcha._session_key]) == 6


@pytest.mark.parametrize('length', [4, 5, 7])
def test_generate_custom_length(mock_request, length):
    captcha = Captcha(mock_request, length=length)
    captcha.generate()
    assert isinstance(mock_request.session[captcha._session_key], str)
    assert len(mock_request.session[captcha._session_key]) == length


@pytest.mark.parametrize('session_value,form_value,param,error_class,message', [
    (None, None, None, CaptchaMissingError, Captcha._ERROR_MISSING_SESSION),
    ('abcdef', None, None, CaptchaMissingError, Captcha._ERROR_MISSING_FORM),
    (None, 'abcdef', None, CaptchaMissingError, Captcha._ERROR_MISSING_SESSION),
    ('abcdef', 'foo', None, CaptchaMismatchError, Captcha._ERROR_MISMATCH),
    ('abcdef', None, 'foo', CaptchaMismatchError, Captcha._ERROR_MISMATCH),
    ('abcdef', 'abcdef', 'foo', CaptchaMismatchError, Captcha._ERROR_MISMATCH)
])
def test_validate_raise(mock_request, session_value, form_value, param, error_class, message):
    captcha = Captcha(mock_request)
    if session_value:
        mock_request.session[captcha._session_key] = session_value
    if form_value:
        mock_request.POST[captcha._form_key] = form_value
    with pytest.raises(CaptchaError) as e:
        captcha.validate(value=param)
        assert isinstance(e, error_class)
        assert e.message == message


def test_validate_form(mock_request):
    captcha = Captcha(mock_request)
    mock_request.session[captcha._session_key] = 'abcdef'
    mock_request.POST[captcha._form_key] = 'abcdef'
    captcha.validate()


def test_validate_value(mock_request):
    captcha = Captcha(mock_request)
    mock_request.session[captcha._session_key] = 'abcdef'
    captcha.validate(value='abcdef')
