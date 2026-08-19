{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;

mkShell {
  buildInputs = [
    python314
    uv
  ];

  shellHook = ''
    unset TEMP TMP TEMPDIR TMPDIR
  '';
}
