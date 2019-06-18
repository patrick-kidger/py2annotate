import importlib
import inspect
import mypy.stubgen as stubgen
import mypy.util as mypy_util
import os
import shutil
import sphinx.ext.autodoc as autodoc
import sys


__version__ = "1.1.0"


# Adapated from https://github.com/python/mypy/blob/master/mypy/stubgen.py to run not from command line
def stubgen_main(opts):
    mypy_util.check_python_version('stubgen')
    # Make sure that the current directory is in sys.path so that
    # stubgen can be run on packages in the current directory.
    if not ('' in sys.path or '.' in sys.path):
        sys.path.insert(0, '')
    options = stubgen.parse_options(opts)
    stubgen.generate_stubs(options)


class DocumenterAnnotator(autodoc.Documenter):
    def import_object(self):
        ret = super(DocumenterAnnotator, self).import_object()

        # get its file if possible. This will fail for builtins and such, so just in case we'll try/except.
        try:
            filepath_py = os.path.abspath(inspect.getsourcefile(self.object))
            module = inspect.getmodule(self.object)
        except TypeError:
            print(self.object)
            print('\n\n\n\n')
            return ret

        filepath = os.path.splitext(filepath_py)[0]
        filepath_pyi = '{}i'.format(filepath_py)
        filepath_py2annotate_py = filepath + '_py2annotate.py'

        # generate py2annotate file...
        if not os.path.isfile(filepath_py2annotate_py):
            # ...by copying a .pyi file if it exists...
            if os.path.isfile(filepath_pyi):
                shutil.copy(filepath_pyi, filepath_py2annotate_py)
            # ...or by creating it from stubgen if it doesn't.
            else:
                opts = []
                if self.env.config.py2annotate_no_import:
                    opts.append('--no-import')
                if self.env.config.py2annotate_parse_only:
                    opts.append('--parse-only')
                if self.env.config.py2annotate_ignore_errors:
                    opts.append('--ignore-errors')
                if self.env.config.py2annotate_include_private:
                    opts.append('--include-private')
                outdir = os.path.dirname(filepath_py)
                while os.path.isfile(os.path.join(outdir, '__init__.py')):
                    outdir, _ = os.path.split(outdir)
                opts.append('--output')
                opts.append(outdir)
                opts.append(filepath_py)
                stubgen_main(opts)
                os.rename(filepath_pyi, filepath_py2annotate_py)
            self.env.app.py2annotate_files.add(filepath_py2annotate_py)

        # import the corresponding object from the py2annotate file and copy its annotations
        with autodoc.mock(self.env.config.autodoc_mock_imports):
            obj = importlib.import_module(module.__name__ + '_py2annotate')
        for o in self.object.__qualname__.split('.'):
            obj = getattr(obj, o)
        self.object.__annotations__ = obj.__annotations__
        if self.objtype == 'class':
            self.object.__init__.__annotations__ = obj.__init__.__annotations__

        return ret


def inject_base(cls):
    if cls != DocumenterAnnotator:
        orig_bases = list(cls.__bases__)
        if DocumenterAnnotator not in orig_bases:
            documenter_base = orig_bases.index(autodoc.Documenter)
            orig_bases[documenter_base] = DocumenterAnnotator
            cls.__bases__ = tuple(orig_bases)


def on_finished(app, exception):
    for pyi_filepath in app.py2annotate_files:
        os.remove(pyi_filepath)
    # delete the cache if we created it.
    # it may not be created if things don't need updating though
    if not app.py2annotate_cache_exists:
        try:
            shutil.rmtree('.mypy_cache')
        except FileNotFoundError:
            pass


def setup(app):
    # First inject our new base class into the MRO for every current subclass of autodoc.Documenter
    for documenter in autodoc.Documenter.__subclasses__():
        inject_base(documenter)

    # Then ensure that every new subclass of autodoc.Documenter gets the injection as well

    # autodoc.Documenter doesn't have an __init_subclass__, but juuuust in case someone else is trying similar levels of
    # stupid hackery, then we'll make sure we don't overwrite it here
    try:
        orig__init_subclass__ = autodoc.Documenter.__dict__['__init_subclass__']  # to avoid superclass lookups
    except KeyError:
        def orig__init_subclass__(cls, *args, **kwargs):
            super(autodoc.Documenter, cls).__init_subclass__(*args, **kwargs)

    def __init_subclass__(cls, *args, **kwargs):
        orig__init_subclass__(cls, *args, **kwargs)
        inject_base(cls)
    autodoc.Documenter.__init_subclass__ = __init_subclass__

    # Remember the files we create during runtime, to clean up at the end.
    app.py2annotate_files = set()
    app.py2annotate_cache_exists = os.path.isdir('.mypy_cache')

    app.add_config_value('py2annotate_no_import', False, False)
    app.add_config_value('py2annotate_parse_only', False, False)
    app.add_config_value('py2annotate_ignore_errors', False, False)
    app.add_config_value('py2annotate_include_private', False, False)

    app.connect('build-finished', on_finished)
