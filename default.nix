{ pkgs ? import <nixpkgs> {} }:
let
in
  pkgs.mkShell {
    buildInputs = [
      pkgs.python312
    ];

}
