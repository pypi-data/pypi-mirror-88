{
  pkgs ? import ../../nixpkgs.nix {}
, mkShell ? pkgs.mkShell
, python ? pkgs.python37
, synthpy ? import ./. { inherit python; }
, jupyterSrc ? import <nixpkgs/pkgs/applications/editors/jupyter>
, jupyter-kernel ? pkgs.jupyter-kernel
}:
let
  envPackages = pp: with pp; [
    ipykernel
    ipywidgets
    numpy
    pandas
    pygments
    google_cloud_dlp
  ];

  overridePythonEnv = pySuper: packages:
    let
      env = pySuper.withPackages packages;
      definitions = {
        python3 = {
          displayName = "Python 3 (OpenQuery)";
          argv = [
            "${env.interpreter}"
            "-m"
            "ipykernel_launcher"
            "-f"
            "{connection_file}"
          ];
          language = "python";
          logo32 = "${env.sitePackages}/ipykernel/resources/logo-32x32.png";
          logo64 = "${env.sitePackages}/ipykernel/resources/logo-64x64.png";
        };
      };
      jupyterKernelOverriden = jupyter-kernel // {
        default = definitions;
      };
    in pySuper.override {
      packageOverrides = self: super: {
        jupyter = jupyterSrc {
          python3 = self.python;
          jupyter-kernel = jupyterKernelOverriden;
        };

        pydata-sphinx-theme = with self; buildPythonPackage rec {
          pname = "pydata-sphinx-theme";
          version = "0.4.1";

          src = fetchPypi {
            inherit pname version;
            sha256 = "0fgynxpik18fdxxhpbbm3yrq3fzqghcvdkc9393sjjx6l3fd15af";
          };

          propagatedBuildInputs = [
            sphinx
          ];
        };

        lessCpy = with super; buildPythonPackage rec {
          pname = "lesscpy";
          version = "0.14.0";
          src = fetchPypi {
            inherit pname version;
            sha256 = "1klccjlcf6zqfryphl2fx464x53zn7cxc7czrjlay5lah5h4yrkv";
          };
          doCheck = false;
          propagatedBuildInputs = [
            six
            ply
          ];
        };

        jupyter-themes = with super; buildPythonApplication {
          pname = "jupyterthemes";
          version = "master";
          src = fetchGit {
            url = "https://github.com/dunovank/jupyter-themes.git";
            ref = "master";
            rev = "22b9358fd52cd852000a0095f491bddb49fe0f7e";
          };
          propagatedBuildInputs = [
            ipython
            notebook
            matplotlib
            self.lessCpy
            jupyter
          ];
        };

        cursor = with super; buildPythonPackage rec {
          pname = "cursor";
          version = "1.3.4";
          doCheck = false;
          doInstallCheck = false;
          src = fetchPypi {
            inherit pname version;
            sha256 = "0h49a0k8sybwhs9zzkd4z08v0aynvah029d94zylxh49fyhpkwik";
          };
        };

        spinners = with super; buildPythonPackage rec {
          pname = "spinners";
          version = "0.0.24";
          src = fetchPypi {
            inherit pname version;
            sha256 = "0zz2z6dpdjdq5z8m8w8dfi8by0ih1zrdq0caxm1anwhxg2saxdhy";
          };
          doCheck = false;
          doInstallCheck = false;
          propagatedBuildInputs = [
            tox
          ];
        };

        log-symbols = with super; buildPythonPackage rec {
          pname = "log-symbols";
          version = "0.0.14";
          format = "wheel";
          src = fetchPypi {
            pname = "log_symbols";
            inherit version;
            sha256 = "1jnwav7d3v86ki4ny27pxy24adx7diz2rpc1a1ysn1dnz1pi0lj9";
            format = "wheel";
            python = "py3";
          };
          doCheck = false;
          doInstallCheck = false;
          propagatedBuildInputs = [
            colorama
            tox
          ];
        };

        halo = with super; buildPythonPackage rec {
          pname = "halo";
          version = "0.0.31";
          src = fetchPypi {
            inherit pname version;
            sha256 = "1mn97h370ggbc9vi6x8r6akd5q8i512y6kid2nvm67g93r9a6rvv";            
          };
          doCheck = false;
          doInstallCheck = false;
          propagatedBuildInputs = with super; [
            termcolor
            six
            colorama
            self.cursor
            self.spinners
            self.log-symbols
          ];
        };
      };
    };

  pythonOverriden = overridePythonEnv python envPackages;

  pythonWithJupyter = pythonOverriden.withPackages (pp: [
    pp.jupyter
    pp.sphinx
    pp.nbsphinx
    pp.pydata-sphinx-theme
    pp.faker
    pp.jupyter-themes
    pp.halo
    pp.twine
    pp.pip
    pp.wheel
  ]);

in mkShell {
  name = "synthpy-workbench";

  buildInputs = [
    pythonWithJupyter
    pythonOverriden.pkgs.jupyter-themes
    synthpy
  ];
}
