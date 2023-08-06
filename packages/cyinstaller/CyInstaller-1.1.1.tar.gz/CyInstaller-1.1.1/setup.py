# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cyinstaller']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'pyinstaller>=4.1,<5.0']

entry_points = \
{'console_scripts': ['CyInstaller = CyInstaller.__main__:build_command']}

setup_kwargs = {
    'name': 'cyinstaller',
    'version': '1.1.1',
    'description': 'A cli tool to package application with Cython & PyInstaller.',
    'long_description': "CyInstaller\n===========\n\nCyInstaller is a lightweight CLI tools to compile and package your application\nto a single executable file with related distribution files.\n\nCyInstaller use `Cython`_ to compile application's source codes, then package\nfiles with `PyInstaller`_.\n\nInstalling\n----------\n\nInstall and update using `pip`_:\n\n.. code-block:: text\n\n    pip install -U CyInstaller\n\nQuickstart\n----------\n\nAdd a `setup.yml` in your project, then execute the `CyInstaller` cli command:\n\n.. code-block:: text\n\n    CyInstaller\n\nCyInstaller default use `setup.yml` as the config file. If use another file,\njust execute the `CyInstaller` command with it as a parameter.\n\n.. code-block:: text\n\n    CyInstaller 'path/to/the/file'\n\nConfiguration\n-------------\n\nA yaml configration may looks like:\n\n.. code-block:: yaml\n\n    setup:\n      app: CyInstallerApp\n      root: .\n      modules:\n        - base: Common\n          package: common\n          package_from_base: false\n          compiles:\n            - ...\n          packages:\n            - ...\n          binaries:\n            - ...\n          datas:\n            - ...\n          relates:\n        - base: Backend\n          ...\n      compiles:\n          - ...\n      packages:\n          - ...\n      datas:\n        - ...\n      relates:\n        - ...\n      cython_binaries: true/false\n      hiddenimports:\n        - ...\n      auto_hiddenimports: true/false\n      entrypoint: app.py\n\n      stage:\n        path: _build\n        debug: true/false\n        cython:\n          path: cython\n          path_tmp: compile\n          options:\n            ...\n        pyinstaller:\n          path: package\n          template: setup.spec\n\n      dist: target\n\nDetail for each options see the `configration guidelines`_.\n\n.. _configration guidelines: https://github.com/solardiax/cyinstaller/blob/master/docs/configuration.rst\n\nLinks\n-----\n\n* Releases: https://pypi.org/project/CyInstaller/\n* Code: https://github.com/solardiax/cyinstaller\n* Issue tracker: https://github.com/solardiax/cyinstaller/issues\n\n.. _Cython: https://cython.org/\n.. _PyInstaller: https://www.pyinstaller.org/\n.. _pip: https://pip.pypa.io/en/stable/quickstart/\n",
    'author': 'SolardiaX',
    'author_email': 'solardiax@hotmail.com',
    'maintainer': 'SolardiaX',
    'maintainer_email': 'solardiax@hotmail.com',
    'url': 'https://github.com/SolardiaX/CyInstaller',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
