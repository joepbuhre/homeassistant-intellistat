{ pkgs ? import <nixpkgs> {} }:
let
in
  pkgs.mkShell {
    buildInputs = [
      pkgs.python313
      pkgs.poetry
      pkgs.outils
    ];

}
