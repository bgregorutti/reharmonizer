class ReharmonizerException(Exception):
    """Base exception for reharmonizer application."""

    pass


class ChordNotFoundError(ReharmonizerException):
    """Raised when a chord is not found."""

    pass


class KeySignatureNotFoundError(ReharmonizerException):
    """Raised when a key signature is not found."""

    pass


class InvalidChordSymbolError(ReharmonizerException):
    """Raised when an invalid chord symbol is provided."""

    pass


class Music21Error(ReharmonizerException):
    """Raised when music21 library encounters an error."""

    pass
