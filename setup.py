import io
import os
import re
import setuptools

project = 'py2annotate'
author = "Patrick Kidger"
copyright = "2019, {}".format(author)
author_email = "contact@kidger.site"
url = "https://github.com/patrick-kidger/py2annotate"
license = "Apache-2.0"
python_requires = ">=3.6"
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
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3.7",
               "Programming Language :: Python :: 3.8",
               "Programming Language :: Python :: 3 :: Only",
               "Topic :: Documentation",
               "Topic :: Documentation :: Sphinx",
               "Topic :: Internet :: WWW/HTTP :: Site Management",
               "Topic :: Software Development :: Documentation"]


# for simplicity we actually store the version in the __version__ attribute in the source
with io.open(os.path.join(os.path.dirname(__file__), project, '__init__.py')) as f:
    meta_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if meta_match:
        version = meta_match.group(1)
    else:
        raise SystemExit("Unable to find __version__ string.")


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
