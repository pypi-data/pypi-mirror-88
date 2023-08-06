#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'bsb_backend_pack',
        version = '2.1',
        description = '',
        long_description = '',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = '',

        url = '',
        project_urls = {},

        scripts = [
            'scripts/current-value-holdings.py',
            'scripts/driver.py',
            'scripts/testScript.py'
        ],
        packages = [],
        namespace_packages = [],
        py_modules = ['logic'],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'alpaca_trade_api',
            'datetime',
            'numpy',
            'pandas',
            'yfinance'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
