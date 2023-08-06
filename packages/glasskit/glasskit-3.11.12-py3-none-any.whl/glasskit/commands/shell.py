from . import Command
import os


class Shell(Command):

    DESCRIPTION = "Run shell (using IPython if available)"

    def run(self):
        rcfile = ".shellrc.py"
        if not os.path.isfile(rcfile):
            rcfile = os.path.join(self.app.base_dir, ".shellrc.py")
        if os.path.isfile(rcfile):
            with open(rcfile) as rcf:
                try:
                    exec(rcf.read())
                except:
                    from traceback import print_exc

                    print("Error running .shellrc.py script!")
                    print_exc()
        try:
            # trying IPython if installed...
            from IPython import embed

            embed(using=False)
        except ImportError:
            # ... or python default console if not
            try:
                # optional readline interface for history if installed
                import readline  # pylint: disable=possibly-unused-variable
            except ImportError:
                pass
            import code

            variables = globals().copy()
            variables.update(locals())
            shell = code.InteractiveConsole(variables)
            shell.interact()
