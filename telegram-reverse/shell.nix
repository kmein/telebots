{ pkgs ? import <nixpkgs> {} }:
(pkgs.python3.withPackages (py: [py.pillow py.pydub py.python-telegram-bot])).env
