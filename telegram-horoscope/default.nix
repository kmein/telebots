{ fetchFromGitHub, buildPythonApplication, buildPythonPackage, fetchPypi, aiohttp, urllib3, pytz }:
let
  telepot =
    buildPythonPackage rec {
      pname = "telepot";
      version = "12.7";
      src = fetchPypi {
        inherit pname version;
        sha256 = "1c587dmr71ppray0lzxgib1plnndmaiwal1kaiqx82rdwx4kw4ms";
      };
      propagatedBuildInputs = [ aiohttp urllib3 ];
      doCheck = false;
    };
in buildPythonApplication rec {
  pname = "telegram-horoscope";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = [ telepot pytz ];
}
