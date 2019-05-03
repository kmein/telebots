from setuptools import setup
import glob

setup(
    name="telegram_odyssey",
    version="0.1.0",
    scripts=["telegram-odyssey"],
    data_files=[("odysseia", glob.glob("odysseia/*.txt"))],
    install_requires=["python-telegram-bot"],
)
