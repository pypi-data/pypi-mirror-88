"""
This module is built to be able to use multiple plotting backends in the same
way.
No matter, which backend you use, plotting should work with the steps shown in
the following
Examples:
    >>> import rna
    >>> import tfields

    Build a cube
    >>> cube = tfields.Mesh3D.grid(
    ...         (-1, 1, 2),
    ...         (-1, 1, 2),
    ...         (-5, -3, 2))
    >>> cube.maps[3].fields = [tfields.Tensors(list(range(len(cube.maps[3]))))]
    >>> map_index = 0
    >>> scalars = cube.maps[3].fields[map_index]

    Tell rna to use the pyqtgraph backend. Default is matplotlib
    >>> rna.plotting.use('pyqtgraph')

    Get an axes element
    >>> axes = rna.plotting.gca(3)

    Plot the cube
    >>> artist = rna.plotting.plot_mesh(cube, cube.maps[3], color=scalars,
    ...     cmap='plasma', axes=axes)

    Plot a colorbar
    >>> cbar = rna.plotting.set_colorbar(axes, artist)

    Show the app and start the loop. Commented for doctests
    # >>> rna.plotting.show()

    Switching back to default
    >>> rna.plotting.use('matplotlib')

"""
import logging
import importlib
import numpy as np
import rna.path
from . import base  # NOQA
from . import colors  # NOQA
from .plot_manager import PlotManager  # NOQA


backend_methods = [
    "axes_dim",
    "gca",
    "show",
    "clear",
    "plot_mesh",
    "plot_array",
    "plot_tensor_field",
    "set_colorbar",
    "_save",
    "set_style",
    "set_labels",
    "set_aspect_equal",
]
global _BACKEND_MOD
_BACKEND_MOD = None
for method_name in backend_methods:
    globals()[method_name] = None


def not_implemented_factory(_method_name):
    """
    Factory method for creating polymorphisms
    """

    def raising_method(*args, **kwargs):
        raise NotImplementedError(
            "Backend does not provide method '{_method_name}'".format(
                _method_name=_method_name
            )
        )

    return raising_method


def use(newbackend):
    """
    Activate a backend of you choice. Non specific methods will be exposed to
    the namespace of rna.plotting . Further methods are exposed to
    rna.plotting.backend
    Args:
        newbackend (str):
            The name of the backend to use.
    Examples:
        >>> import rna
        >>> rna.plotting.use('matplotlib')
        >>> mpl_show = rna.plotting.show
        >>> rna.plotting.use('pyqtgraph')
        >>> pqg_show = rna.plotting.show
        >>> assert callable(mpl_show)
        >>> assert callable(pqg_show)
        >>> assert mpl_show is not pqg_show
        >>> rna.plotting.use('matplotlib')

    """
    backend_name = "rna.plotting.backend_{}".format(newbackend.lower())

    backend_mod = importlib.import_module(backend_name)
    # build a new class Backend which gives it module like behaviour
    global backend
    backend = type("Backend", (base._Backend,), vars(backend_mod))
    logging.debug("Loaded backend %s.", newbackend)

    # expose backend_methods to global namespace of rna.plotting
    global _BACKEND_MOD
    _BACKEND_MOD = backend_mod
    for _method_name in backend_methods:
        if hasattr(backend, _method_name):
            # globals()[method_name] = getattr(backend, method_name)
            setattr(rna.plotting, _method_name, getattr(_BACKEND_MOD, _method_name))
        else:
            setattr(rna.plotting, _method_name, not_implemented_factory(_method_name))
    # Need to keep a global reference to the backend for compatibility reasons.
    # See https://github.com/matplotlib/matplotlib/issues/6092
    rna.plotting.active_backend = newbackend


def save(path, *fmts, **kwargs):
    """
    Args:
        path (str): path without extension to save to
        *fmts (str): format of the figure to save. If multiple are given,
            create that many files
        **kwargs:
            axes
            fig
    """
    if len(fmts) != 0:
        for fmt in fmts:
            if path.endswith("."):
                new_file_path = path + fmt
            elif "{fmt}" in path:
                new_file_path = path.format(**locals())
            else:
                new_file_path = path + "." + fmt
            save(new_file_path, **kwargs)
    else:
        path = rna.path.resolve(path)
        logging.info("Saving figure as %s", path)
        _save(  # noqa: E501,F821, pylint: disable=undefined-variable
            path, **dict(kwargs)
        )  # copy the dict before passing


def figsize(width_pt, scale=1.0, ratio=None):
    """
    Args:
        width_pt (float): figure width width in pt. Can be scaled by
            Get textwidth from latex using '\the\textwidth'
        scale (float)
        ratio (float | None):
            float: ratio of figure height / figure width
            None: golden ratio
    """
    inches_per_pt = 1.0 / 72.27  # Convert pt to inch
    if ratio is None:
        # golden ratio
        ratio = (np.sqrt(5.0) - 1.0) / 2.0
    fig_width = width_pt * inches_per_pt * scale  # fig_width in inches
    fig_height = fig_width * ratio  # height in inches
    fig_size = (fig_width, fig_height)
    return fig_size


if __name__ == "__main__":
    import doctest

    doctest.testmod()
