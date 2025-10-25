{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{

  packages = [
    pkgs.black
    pkgs.ninja
    pkgs.nixfmt
    pkgs.python3Packages.plyvel
  ];

  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        amulet-nbt
      '';
    };
  };

}
