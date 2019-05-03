{ fetchFromGitHub, buildPythonApplication, pillow, python-telegram-bot, pydub, ffmpeg }:
buildPythonApplication rec {
  pname = "telegram-reverse";
  version = "0.2.0";

  src = ./.;

  propagatedBuildInputs = [ pillow python-telegram-bot pydub ffmpeg ];
}
