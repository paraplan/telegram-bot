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
        lib = pkgs.lib;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.uv
            pkgs.gnumake
          ];
          LD_LIBRARY_PATH = lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
          ];
          shellHook = ''
            export UV_PYTHON_DOWNLOADS=never
            export UV_PYTHON=${lib.getExe pkgs.python314}
            printf '\nWelcome to paraplan project!\n'
            printf 'Run: make\n\n'
          '';
        };
      }
    );
}
