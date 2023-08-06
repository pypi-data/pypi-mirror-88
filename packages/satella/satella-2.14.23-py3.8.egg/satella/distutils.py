import typing as tp
import multiprocessing

__all__ = ['monkey_patch_parallel_compilation']

# shamelessly ripped from
# https://stackoverflow.com/questions/11013851/speeding-up-build-process-with-distutils


def monkey_patch_parallel_compilation(cores: tp.Optional[int] = None) -> None:
    """
    This monkey-patches distutils to provide parallel compilation, even if you have
    a single extension built from multiple .c files.

    Invoke in your setup.py file

    :param cores: amount of cores. Leave at default (None) for autodetection.
    """
    if cores is None:
        cores = multiprocessing.cpu_count()

    # monkey-patch for parallel compilation
    def parallelCCompile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0,
                         extra_preargs=None, extra_postargs=None, depends=None):
        # those lines are copied from distutils.ccompiler.CCompiler directly
        macros, objects, extra_postargs, pp_opts, build = self._setup_compile(output_dir, macros,
                                                                              include_dirs, sources,
                                                                              depends,
                                                                              extra_postargs)
        cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
        # parallel code
        N = 2  # number of parallel compilations
        import multiprocessing.pool
        def _single_compile(obj):
            try:
                src, ext = build[obj]
            except KeyError:
                return
            self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        # convert to list, imap is evaluated on-demand
        list(multiprocessing.pool.ThreadPool(cores).imap(_single_compile, objects))
        return objects

    import distutils.ccompiler
    distutils.ccompiler.CCompiler.compile = parallelCCompile
