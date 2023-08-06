"""
Generate the API docs using pydoctor to be integrated into Sphinx build system.

This was designed to generate pydoctor HTML files as part of the
Read The Docs build process.

Inside the Sphinx conf.py file you need to define the following configuration options:

  - C{pydoctor_args} - a list with all the pydoctor command line arguments used to trigger the build.

The following format placeholders are resolved for C{pydoctor_args} at runtime:
  - C{{outdir}} - the Sphinx output dir

You must call pydoctor with C{--quiet} argument
as otherwise any extra output is converted into Sphinx warnings.
"""
from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.errors import ConfigError
from sphinx.util import logging

from pydoctor import __version__
from pydoctor.driver import main


logger = logging.getLogger(__name__)


def on_build_finished(app: Sphinx, exception: Exception) -> None:
    """
    Called when Sphinx build is done.
    """
    config: Config = app.config  # type: ignore[has-type]
    if not config.pydoctor_args:
        raise ConfigError("Missing 'pydoctor_args'.")

    placeholders = {
        'outdir': app.outdir,
        }

    args = []
    for argument in config.pydoctor_args:
        args.append(argument.format(**placeholders))

    logger.info("Bulding pydoctor API docs as:")
    logger.info('\n'.join(args))

    with StringIO() as stream:
        with redirect_stdout(stream):
            main(args=args)

        for line in stream.getvalue().splitlines():
            logger.warning(line)


def setup(app: Sphinx) ->  Dict[str, Any]:
    """
    Called by Sphinx when the extension is initialized.

    @return: The extension version and runtime options.
    """
    app.connect('build-finished', on_build_finished)
    app.add_config_value("pydoctor_args", [], "env")

    return {
        'version': str(__version__),
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
