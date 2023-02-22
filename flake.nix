{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system: let
    pkgs = import nixpkgs {
      inherit system;
      config.permittedInsecurePackages = [
        "python3.9-poetry-1.1.12"
      ];
    };
  in {
    defaultPackage = self.packages.${system}.telebots;
    packages.telebots = pkgs.callPackage ./. {};
  });
}
