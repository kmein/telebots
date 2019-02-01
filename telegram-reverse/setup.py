from setuptools import setup

setup(
    name="telegram-reverse",
    version="0.2.0",
    scripts=["./telegram-reverse"],
    install_requires=["pillow", "pydub", "python-telegram-bot"],
)
