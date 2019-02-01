from setuptools import setup

setup(
    name="telegram-betacode",
    version="0.1.0",
    scripts=["./telegram-betacode"],
    install_requires=["betacode", "python-telegram-bot"],
)
