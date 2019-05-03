from setuptools import setup

setup(
    name="telegram-odyssey",
    version="0.1.0",
    scripts=["./telegram-odyssey"],
    include_package_data=True,
    package_data={"": ["odysseia/*.txt"]},
    install_requires=["python-telegram-bot"],
)
