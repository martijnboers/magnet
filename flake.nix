{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";

  outputs = {
    self,
    nixpkgs,
    poetry2nix,
  }: let
    supportedSystems = ["x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin"];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (system: {
      default = pkgs.${system}.mkShellNoCC {
        packages = with pkgs.${system}; [
          (python34.withPackages (python-pkgs: with python-pkgs; [cython pip black]))
          alejandra
        ];
      };
    });
  };
}
