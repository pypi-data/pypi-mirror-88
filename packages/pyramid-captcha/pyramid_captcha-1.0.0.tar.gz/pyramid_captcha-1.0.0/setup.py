import codecs
import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'captcha'
]

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    description = f.read()

with codecs.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    description += '\n\n'
    description += f.read()


setup(
    name='pyramid_captcha',
    version='1.0.0',
    description='Pyramid Captcha',
    long_description=description,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP'
    ],
    author='Karsten Deininger',
    author_email='karsten.deininger@bl.ch',
    url='https://gitlab.com/geo-bl-ch/pyramid-captcha',
    keywords='web pyramid captcha',
    install_requires=requires,
    packages=find_packages(exclude=['demo', 'test*']),
    include_package_data=True
)
