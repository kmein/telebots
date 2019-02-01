{ pkgs ? import <nixpkgs> {} }:
let
  pygtrie =
    with pkgs.python3Packages;
    buildPythonPackage rec {
      pname = "pygtrie";
      version = "2.3";
      src = fetchPypi {
        inherit pname version;
        sha256 = "00x7q4p9r75zdnw3a8vd0d0w0i5l28w408g5bsfl787yv6b1h9i8";
      };
      doCheck = false;
    };
  betacode =
    with pkgs.python3Packages;
    buildPythonPackage rec {
      pname = "betacode";
      version = "0.2";
      src = fetchPypi {
        inherit pname version;
        sha256 = "08fnjzjvnm9m6p4ddyr8qgfb9bs2nipv4ls50784v0xazgxx7siv";
      };
      propagatedBuildInputs = [ pygtrie ];
      doCheck = false;
    };
in (pkgs.python3.withPackages (py: [py.python-telegram-bot betacode])).env
