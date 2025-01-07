{ pkgs }: {
  deps = [
    pkgs.python3Full
    pkgs.python310Packages.pip
    pkgs.replitPackages.prybar-python310
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.python310Full
    ];
    PYTHONBIN = "${pkgs.python310Full}/bin/python3.10";
    LANG = "en_US.UTF-8";
  };
}
