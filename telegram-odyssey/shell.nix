{ pkgs ? import <nixpkgs> {} }:
(pkgs.python3.withPackages (py: [py.python-telegram-bot])).env // {
  TELEGRAM_ODYSSEY_TOKEN = builtins.readFile ./Tokenfile;
}
