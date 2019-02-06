{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
let
  pygtrie =
    buildPythonPackage rec {
      pname = "pygtrie";
      version = "2.3";
      src = fetchPypi {
        inherit pname version;
        sha256 = "00x7q4p9r75zdnw3a8vd0d0w0i5l28w408g5bsfl787yv6b1h9i8";
      };
      doCheck = false;
    };
  betacode = buildPythonPackage rec {
      pname = "betacode";
      version = "0.2";
      src = fetchPypi {
        inherit pname version;
        sha256 = "08fnjzjvnm9m6p4ddyr8qgfb9bs2nipv4ls50784v0xazgxx7siv";
      };
      preBuild = ''sed -i 's/[\d128-\d255]//g' ./README.rst'';
      propagatedBuildInputs = [ pygtrie ];
      doCheck = false;
    };
in (pkgs.python3.withPackages (py: [py.python-telegram-bot betacode])).env // {
  TELEGRAM_BETACODE_TOKEN = builtins.readFile ./Tokenfile;
}
