# -*- coding: utf-8 -*-
import io
from uuid import uuid4

from captcha.image import ImageCaptcha

from pyramid_captcha.exception import CaptchaMissingError, CaptchaMismatchError


class Captcha(object):

    _ERROR_MISSING_SESSION = 'Missing captcha value in session'  # type: str
    _ERROR_MISSING_FORM = 'No captcha value received in form data'  # type: str
    _ERROR_MISMATCH = 'Captcha mismatch'  # type: str

    def __init__(self, request, session_key='captcha', form_key='captcha', length=6):
        """
        The class Captcha provides methods for generating and validating captcha values. The generated
        captcha value is store in the session until validation.

        Args:
            request (pyramid.request.Request): The current Pyramid request object.
            session_key (str): The name of the session property to store the captcha value (Default:
                'captcha').
            form_key (str): The name of the form field with the submitted captcha value (Default: 'captcha').
            length (int): The number of captcha characters (Default: 6).
        """
        self._request = request
        self._captcha = ImageCaptcha()
        self._session_key = session_key
        self._form_key = form_key
        self._length = length

    def generate(self):
        """
        Generates a captcha image and returns it as Pyramid response.

        Returns:
            pyramid.response.Response: The response containing the generated captcha image.
        """
        value = uuid4().hex[:self._length]
        image = self._captcha.generate_image(value)
        self._request.session[self._session_key] = value
        response = self._request.response
        with io.BytesIO() as buffer:
            image.save(buffer, format='PNG')
            response.body = buffer.getvalue()
        response.content_type = 'image/png'
        response.content_length = len(response.body)
        return response

    def validate(self, value=None):
        """
        Validates the submitted captcha value against the value stored in the current session.

        Args:
            value (str or None): A captcha value to validate (Default: None). If the parameter is None, a
                value is expected to be found in the POST body of the request.

        Raises:
            pyramid_captcha.exception.CaptchaMissingError: Raised if one of the captcha values is missing.
            pyramid_captcha.exception.CaptchaMismatchError: Raised if the submitted value does not match the
                value stored in the session.
        """
        if self._session_key in self._request.session:
            session_value = self._request.session[self._session_key]
            del self._request.session[self._session_key]
            if value is not None:
                submitted_value = value
            else:
                if self._form_key in self._request.POST:
                    submitted_value = self._request.POST[self._form_key]
                else:
                    raise CaptchaMissingError(self._ERROR_MISSING_FORM)
            if session_value != submitted_value:
                raise CaptchaMismatchError(self._ERROR_MISMATCH)
        else:
            raise CaptchaMissingError(self._ERROR_MISSING_SESSION)
