"""Provide the main function."""

from synthizer import Context, initialized
from wx import App

from .gui.reverb import ReverbFrame


def reverb_main() -> None:
    """Provide the main entry point."""
    with initialized():
        a: App = App()
        ctx: Context = Context()
        f: ReverbFrame = ReverbFrame(ctx)
        f.Show(show=True)
        f.Maximize(maximize=True)
        a.MainLoop()


if __name__ == '__main__':
    reverb_main()
