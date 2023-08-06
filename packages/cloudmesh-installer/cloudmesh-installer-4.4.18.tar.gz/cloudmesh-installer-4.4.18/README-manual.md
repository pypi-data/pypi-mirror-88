cloudmesh-installer -- a helper to install cloudmesh from source for developers.

Usage:
  cloudmesh-installer git key [LOCATION] [--benchmark]
  cloudmesh-installer git [clone|pull|status|authors] [BUNDLES...] [--benchmark]
  cloudmesh-installer get [BUNDLES...] [--benchmark]
  cloudmesh-installer update [BUNDLELES...] [--benchmark]
  cloudmesh-installer install [BUNDLES...] [--venv=ENV | -e] [--benchmark]
  cloudmesh-installer list [BUNDLE] [--short | --git]
  cloudmesh-installer version
  cloudmesh-installer info [BUNDLE] [--verbose]
  cloudmesh-installer clean --dir=DIR [--force]
  cloudmesh-installer clean --venv=ENV [--force]
  cloudmesh-installer new VENV [BUNDLES...] [--python=PYTHON]
  cloudmesh-installer release [REPOS...] [--benchmark]


A convenient program called `cloudmesh-installer` to download and install
cloudmesh from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos
  ENV         the name of the venv
  DIR         the directory form where to start the search

Options:
  -h --help
  --force   force the execution of the command. This command could delete files.

Description:

    cloudmesh-installer list

        Cloudmesh has a number of bundles. Bundles are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

        This command lists all available bundles

    cloudmesh-installer list bundle

        lists the information about a particular bundle.

    cloudmesh-installer list [BUNDLE] --git

        Shows the location of the repositories in a bundle.

    cloudmesh-installer info

        The info command gives some very basic information about the version
        numbers of cloudmesh on your system, github, and pypi. THis helps
        identifying if you may run an odlder version.

        In addition we try to check if you do use venv

    cloudmesh-installer git key [LOCATION]

        This command only works if you use ssh keys to authenticate with github.
        This command makes uploading the key easy as it checks for your key and
        provides via the web browser automatic pageloads to github for the
        key upload. You do not have tou use this command. It is intenden for
        novice users.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer update [BUNDLE]
    cloudmesh-installer get [BUNDLE]

        For each repository in the bundle it clones it and also pulls.
        Thus the command can easly be used to get a new bundle element, but
        also get the new code for already existing bundles elements.

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer clean --dir=. --force

       removes the egs in the current directory tree

    cloudmesh-installer clean --venv=ENV --force

        removes the venv in ~/ENV

    Examples:

        let us assume you like to work on storage, than you need to do the following

            mkdir cm
            cd cm
            cloudmesh-installer git clone storage
            cloudmesh-installer install storage
            cloudmesh-installer info
