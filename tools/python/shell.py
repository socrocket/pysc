import pysc
import code
import os
import sys

def help_text(*k, **kw):
    import webbrowser
    print "SoCRocket - The Space TLM Framework"
    webbrowser.open('http://socrocket.github.io/')
    help(*k, **kw)
def credits_text():
    print "Thomas Schuster, Rolf Meyer, Jan Wagner"
def copyright_text():
    print "(c) Copyright 2010-2014 TU-Braunschweig c3e"
def license_text():
    print "All rights reserved"

CONSOLE = None

def load(*k, **kw):
    """Load initial model configuration"""
    from tools.python.arguments import parser
    parser.add_argument('-s', '--startupconsole', dest='option', action='store_true', help='Execute an interactive python console right after start of the sc_main')

class Console(code.InteractiveConsole):
    """Closely emulate the behavior of the interactive Python interpreter.

    This class builds on InteractiveInterpreter and adds prompting
    using the familiar sys.ps1 and sys.ps2, and input buffering.
    As Code.InteractiveConsole but extend it with a stop function.

    """

    def __init__(self, locals=None, filename="<console>"):
        """Constructor.

        The optional locals argument will be passed to the
        InteractiveInterpreter base class.

        The optional filename argument should specify the (file)name
        of the input stream; it will show up in tracebacks.

        """
        code.InteractiveConsole.__init__(self, locals)
        self.filename = filename
        self.run = True
        self.resetbuffer()

    def interact(self, banner=None):
        """Closely emulate the interactive Python console.

        The optional banner argument specify the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter,
        followed by the current class name in parentheses (so as not
        to confuse this with the real interpreter -- since it's so
        close!).

        """
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if banner is None:
            self.write("Python %s on %s\n%s\n(%s)\n" %
                       (sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        else:
            self.write("%s\n" % str(banner))
        more = 0
        while self.run:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input(prompt)
                    # Can be None if sys.stdin was redefined
                    encoding = getattr(sys.stdin, "encoding", None)
                    if encoding and not isinstance(line, unicode):
                        line = line.decode(encoding)
                    if not self.run:
                        break
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0
    def stop(self):
          self.run = False

def start(*k, **kw):
    histfile = os.path.join(os.environ["HOME"], ".socrocket_history")
    rcfile = os.path.join(os.environ["HOME"], ".socrocketrc")

    try:
        import rlcompleter
        import readline

    except ImportError:
        rlcompleter = None
        readline = None
        print "Python shell enhancement modules not available."

    else:
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")

        if os.path.isfile(histfile):
            readline.read_history_file(histfile)

        if os.path.isfile(rcfile):
            readline.read_init_file(rcfile)

        print "Python shell history and tab completion are enabled."

    sys.modules['__main__'].__dict__.update({
      "help": help_text,
      "credits": credits_text,
      "copyright": copyright_text,
      "license": license_text
    })
    global CONSOLE
    CONSOLE = Console(sys.modules['__main__'].__dict__)
    sys.modules['__main__'].__dict__['CONSOLE'] = CONSOLE
    #code.interact(local=sys.modules['__main__'].__dict__, banner='')
    #print CONSOLE
    CONSOLE.interact('')

    if readline:
        readline.write_history_file(histfile)

def stop(*k, **kw):
    import sys
    global CONSOLE
    sys.modules['__main__'].CONSOLE.stop()


def install():
    #load()
    pysc.on("pause_of_simulation")(start)
    start()

install()

if __name__ == "__main__":
    install()

