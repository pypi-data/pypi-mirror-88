# -*- coding: utf-8 -*-


class CaptchaError(Exception):
    """
    Exception base class.
    """
    pass


class CaptchaMissingError(CaptchaError):
    """
    Raised if captcha data is missing in the session properties or the form data.
    """
    pass


class CaptchaMismatchError(CaptchaError):
    """
    Raised if the submitted captcha value does not match the value of the session.
    """
    pass
