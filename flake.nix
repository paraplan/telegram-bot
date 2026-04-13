{
  description = "Paraplan development shell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      flake-utils,
      nixpkgs,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.uv
            pkgs.gnumake
          ];
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
          ];
          shellHook = ''
            export UV_PYTHON_DOWNLOADS=never
            export UV_PYTHON=${pkgs.python314}/bin/python3
            printf '\nWelcome to paraplan project!\n'
            printf 'Run: make\n\n'
          '';
        };
      }
    );
}
