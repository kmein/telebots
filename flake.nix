{
  description = "Collection of Telegram bots";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
  };

  outputs =
    { self, nixpkgs }:
    let
      lib = nixpkgs.lib;
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
      ];
      eachSupportedSystem = lib.genAttrs supportedSystems;
      pkgsFor =
        system:
        import nixpkgs {
          inherit system;
          config.permittedInsecurePackages = [
            "python3.9-poetry-1.1.12"
          ];
        };
    in
    {
      defaultPackage = eachSupportedSystem (system: self.packages.${system}.telebots);
      packages = eachSupportedSystem (system: {
        telebots = (pkgsFor system).callPackage ./. { };
      });
    };
}
