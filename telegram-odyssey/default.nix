{ fetchFromGitHub, buildPythonApplication, python-telegram-bot }:
buildPythonApplication rec {
  pname = "telegram-odyssey";
  version = "0.1.0";
  src = ./.;
  propagatedBuildInputs = [ python-telegram-bot ];
}
