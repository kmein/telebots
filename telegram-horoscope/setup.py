from setuptools import setup

setup(
    name="telegram-horoscope",
    version="0.1.0",
    scripts=["./telegram-horoscope"],
    install_requires=["telepot", "pytz"],
)
