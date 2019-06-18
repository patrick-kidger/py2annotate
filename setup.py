import io
import os
import setuptools

project = 'py2annotate'
version = "1.0.1"
author = "Patrick Kidger"
copyright = "2019, {}".format(author)
author_email = "contact@kidger.site"
url = "https://github.com/patrick-kidger/py2annotate"
license = "Apache-2.0"
python_requires = ">=3.0"
keywords = "signature"
classifiers = ["Development Status :: 4 - Beta",
               "Environment :: Web Environment",
               "Framework :: Sphinx",
               "Framework :: Sphinx :: Extension",
               "Intended Audience :: Developers",
               "Intended Audience :: Education",
               "Intended Audience :: End Users/Desktop",
               "Intended Audience :: Science/Research",
               "Intended Audience :: System Administrators",
               "License :: OSI Approved :: Apache Software License",
               "Natural Language :: English",
               "Operating System :: OS Independent",
               "Programming Language :: Python :: 3",
               "Topic :: Documentation",
               "Topic :: Documentation :: Sphinx",
               "Topic :: Internet :: WWW/HTTP :: Site Management",
               "Topic :: Software Development :: Documentation"]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    readme = f.read()

description = readme.split('\n', maxsplit=4)[-2]

setuptools.setup(name=project,
                 version=version,
                 author=author,
                 author_email=author_email,
                 maintainer=author,
                 maintainer_email=author_email,
                 description=description,
                 long_description=readme,
                 url=url,
                 license=license,
                 keywords=keywords,
                 classifiers=classifiers,
                 zip_safe=False,
                 python_requires=python_requires,
                 packages=[project],
                 install_requires=['sphinx', 'mypy'])
