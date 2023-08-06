Pyramid Captcha
===============

This Python package provides a captcha implementation for use with the
`Pyramid Web Framework <https://docs.pylonsproject.org/projects/pyramid/en/latest/>`__.
It is based on the `captcha <https://pypi.org/project/captcha/>`__ library and uses
Pyramid sessions for captcha validation. Please refer to the
`documentation <https://geo-bl-ch.gitlab.io/pyramid-captcha>`__ for further information.

.. note:: Development builds of this package can be found at https://test.pypi.org/project/pyramid-captcha/.

Usage
-----

To generate a captcha, you have to import the class :code:`Captcha`.

.. code-block:: python

    from pyramid_captcha import Captcha

The simplest solution is to use this class directly in your
view definition.

.. code-block:: python

    config.add_route('captcha_generate', '/captcha')
    config.add_view(
        Captcha,
        attr='generate',
        route_name='captcha_generate',
        request_method='GET'
    )

In this case, the route :code:`/captcha` will return a captcha image
with the default length of 6 characters. If you want to adjust the
captcha properties, you have to wrap it into a view callable, for
example to change the number of characters.

.. code-block:: python

    def generate(request):
        return Captcha(request, length=4).generate()

The generated captcha value is stored in the current session. It
can be checked against a submitted form value using the
:code:`validate()` method.

.. code-block:: python

    try:
        Captcha(request).validate()
    except CaptchaError as e:
        raise HTTPForbidden(e)

Demo
----

You can check out the code and run a little demo by calling
:code:`make serve`.