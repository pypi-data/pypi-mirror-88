import sys
from inspect import signature
from pathlib import Path
from . import singleton


class cli(object):
    def __init__(self, app_version=None, app_doc=None, app_name=None):
        if app_version is None:
            singleton.func()
        self.app_version = app_version
        self.app_doc = app_doc or "No help provided"
        self.app_name = app_name or Path(sys.argv[0]).name

    def __call__(self, func):
        def inner_func():
            original_argv = sys.argv[:]
            if self.check_version():
                return
            if self.check_help():
                return
            singleton.verbosity = self.check_verbose_flags()
            args = self.check_required_args(func)
            result = func(*args)
            sys.argv = original_argv
            return result

        singleton.func = inner_func
        return inner_func

    def check_help(self):
        if "--help" in sys.argv:
            print(f"{self.app_doc}")
            return True

    def check_version(self):
        if "--version" in sys.argv:
            print(f"{self.app_name} {self.app_version}")
            return True

    def check_verbose_flags(self):

        new_args = []
        verbose_count = 0

        for arg_value in sys.argv:
            if arg_value[0] == "-" and arg_value.strip("-v") == "":
                verbose_count = arg_value.count("v")
                continue
            new_args.append(arg_value)

        sys.argv = new_args
        return verbose_count

    def check_required_args(self, func):
        args = []
        i = 1
        sig = signature(func)
        param_str = " ".join([f"<{x}>" for x in sig.parameters])
        for i, param in enumerate(sig.parameters):
            if i >= len(sys.argv) - 1:
                print(
                    f"Missing required command line parameter '{param}' !",
                    file=sys.stderr,
                )
                print(f"Usage:\n  {self.app_name} {param_str}", file=sys.stderr)
                exit(1)
            args.append(sys.argv[i + 1])
        return args
