class TwigError(Exception):
    """
    Base class for all Twig errors.
    """

    pass


class CompilerError(TwigError):
    """
    Raised when an error occurs during compilation.
    """

    pass
