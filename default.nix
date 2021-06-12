{ poetry2nix, python38 }:
poetry2nix.mkPoetryScriptsPackage {
    projectDir = ./.;
    python = python38;
}
