{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
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
in (pkgs.python3.withPackages (py: [py.pytz telepot])).env // {
  TELEGRAM_HOROSCOPE_TOKEN = builtins.readFile ./Tokenfile;
  GOOGLE_MAPS_API_KEY = builtins.readFile ./horobot.key;
}
