from __future__ import annotations

from typing import Any, Dict


class ScardException(Exception):
    _subs: Dict[int, ScardException] = {}

    def __init_subclass__(cls, code: int = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if code:
            cls._subs[code] = cls

    def __init__(self, msg):
        self.msg = msg

    @classmethod
    def create(cls, msg: Any, code: int) -> ScardException:
        try:
            return cls._subs[code](msg)
        except KeyError:
            return ScardExceptionUnknown(msg, code)


class ScardExceptionUnknown(ScardException):
    def __init__(self, msg: Any, code: int):
        super().__init__(msg)
        self.code = code

    def __str__(self):
        return f"code=0x{self.code:08X}, msg={self.msg!r}"

# https://docs.microsoft.com/en-us/previous-versions/aa924526(v=msdn.10)


class ScardFailureInternalError(ScardException, code=0x80100001):
    """
    An internal consistency check failed.
    """


class ScardErrorCancelled(ScardException, code=0x80100002):
    """
    The action was cancelled by a SCardCancel request.
    """


class ScardErrorInvalidHandle(ScardException, code=0x80100003):
    """
    The supplied handle was invalid.
    """


class ScardErrorInvalidParameter(ScardException, code=0x80100004):
    """
    One or more of the supplied parameters could not be properly interpreted.
    """


class ScardErrorInvalidTarget(ScardException, code=0x80100005):
    """
    Registry startup information is missing or invalid.
    """


class ScardErrorNoMemory(ScardException, code=0x80100006):
    """
    Not enough memory available to complete this command.
    """


class ScardFailureWaitedTooLong(ScardException, code=0x80100007):
    """
    An internal consistency timer has expired.
    """


class ScardErrorInsufficientBuffer(ScardException, code=0x80100008):
    """
    The data buffer to receive returned data is too small for the returned data.
    """


class ScardErrorUnknownReader(ScardException, code=0x80100009):
    """
    The specified reader name is not recognized.
    """


class ScardErrorTimeout(ScardException, code=0x8010000A):
    """
    The user-specified timeout value has expired.
    """


class ScardErrorSharingViolation(ScardException, code=0x8010000B):
    """
    The smart card cannot be accessed because of other connections outstanding.
    """


class ScardErrorNoSmartcard(ScardException, code=0x8010000C):
    """
    The operation requires a smart card, but no smart card is currently in the device.
    """


class ScardErrorUnknownCard(ScardException, code=0x8010000D):
    """
    The specified smart card name is not recognized.
    """


class ScardErrorCantDispose(ScardException, code=0x8010000E):
    """
    The system could not dispose of the media in the requested manner.
    """


class ScardErrorProtoMismatch(ScardException, code=0x8010000F):
    """
    The requested protocols are incompatible with the protocol currently in use with the smart card.
    """


class ScardErrorNotReady(ScardException, code=0x80100010):
    """
    The reader or smart card is not ready to accept commands.
    """


class ScardErrorInvalidValue(ScardException, code=0x80100011):
    """
    One or more of the supplied parameters values could not be properly interpreted.
    """


class ScardErrorSystemCancelled(ScardException, code=0x80100012):
    """
    The action was cancelled by the system, presumably to log off or shut down.
    """


class ScardFailureCommError(ScardException, code=0x80100013):
    """
    An internal communications error has been detected.
    """


class ScardFailureUnknownError(ScardException, code=0x80100014):
    """
    An internal error has been detected, but the source is unknown.
    """


class ScardErrorInvalidAtr(ScardException, code=0x80100015):
    """
    An ATR obtained from the registry is not a valid ATR string.
    """


class ScardErrorNotTransacted(ScardException, code=0x80100016):
    """
    An attempt was made to end a non-existent transaction.
    """


class ScardErrorReaderUnavailable(ScardException, code=0x80100017):
    """
    The specified reader is not currently available for use.
    """


class ScardPanicShutdown(ScardException, code=0x80100018):
    """
    The operation has been aborted to allow the server application to exit.
    """


class ScardErrorPciTooSmall(ScardException, code=0x80100019):
    """
    The PCI Receive buffer was too small.
    """


class ScardErrorReaderUnsupported(ScardException, code=0x8010001A):
    """
    The reader driver does not meet minimal requirements for support.
    """


class ScardErrorDuplicateReader(ScardException, code=0x8010001B):
    """
    The reader driver did not produce a unique reader name.
    """


class ScardErrorCardUnsupported(ScardException, code=0x8010001C):
    """
    The smart card does not meet minimal requirements for support.
    """


class ScardErrorNoService(ScardException, code=0x8010001D):
    """
    The Smart Card Resource Manager is not running.
    """


class ScardErrorServiceStopped(ScardException, code=0x8010001E):
    """
    The Smart Card Resource Manager has shut down.
    """


class ScardErrorUnexpected(ScardException, code=0x8010001F):
    """
    An unexpected card error has occurred.
    """


class ScardErrorIccInstallation(ScardException, code=0x80100020):
    """
    No primary provider can be found for the smart card.
    """


class ScardErrorIccCreateorder(ScardException, code=0x80100021):
    """
    The requested order of object creation is not supported.
    """


class ScardErrorUnsupportedFeature(ScardException, code=0x80100022):
    """
    This smart card does not support the requested feature.
    """


class ScardErrorDirNotFound(ScardException, code=0x80100023):
    """
    The identified directory does not exist in the smart card.
    """


class ScardErrorFileNotFound(ScardException, code=0x80100024):
    """
    The identified file does not exist in the smart card.
    """


class ScardErrorNoDir(ScardException, code=0x80100025):
    """
    The supplied path does not represent a smart card directory.
    """


class ScardErrorNoFile(ScardException, code=0x80100026):
    """
    The supplied path does not represent a smart card file.
    """


class ScardErrorNoAccess(ScardException, code=0x80100027):
    """
    Access is denied to this file.
    """


class ScardErrorWriteTooMany(ScardException, code=0x80100028):
    """
    The smart card does not have enough memory to store the information.
    """


class ScardErrorBadSeek(ScardException, code=0x80100029):
    """
    There was an error trying to set the smart card file object pointer.
    """


class ScardErrorInvalidChv(ScardException, code=0x8010002A):
    """
    The supplied PIN is incorrect.
    """


class ScardErrorUnknownResMng(ScardException, code=0x8010002B):
    """
    An unrecognized error code was returned from a layered component.
    """


class ScardErrorNoSuchCertificate(ScardException, code=0x8010002C):
    """
    The requested certificate does not exist.
    """


class ScardErrorCertificateUnavailable(ScardException, code=0x8010002D):
    """
    The requested certificate could not be obtained.
    """


class ScardErrorNoReadersAvailable(ScardException, code=0x8010002E):
    """
    Cannot find a smart card reader.
    """


class ScardErrorCommDataLost(ScardException, code=0x8010002F):
    """
    A communications error with the smart card has been detected. Retry the operation.
    """


class ScardErrorNoKeyContainer(ScardException, code=0x80100030):
    """
    The requested key container does not exist on the smart card.
    """


class ScardErrorServerTooBusy(ScardException, code=0x80100031):
    """
    The Smart Card Resource Manager is too busy to complete this operation.
    """


class ScardWarningUnsupportedCard(ScardException, code=0x80100065):
    """
    The reader cannot communicate with the card, due to ATR string configuration conflicts.
    """


class ScardWarningUnresponsiveCard(ScardException, code=0x80100066):
    """
    The smart card is not responding to a reset.
    """


class ScardWarningUnpoweredCard(ScardException, code=0x80100067):
    """
    Power has been removed from the smart card, so that further communication is not possible.
    """


class ScardWarningResetCard(ScardException, code=0x80100068):
    """
    The smart card has been reset, so any shared state information is invalid.
    """


class ScardWarningRemovedCard(ScardException, code=0x80100069):
    """
    The smart card has been removed, so further communication is not possible.
    """


class ScardWarningSecurityViolation(ScardException, code=0x8010006A):
    """
    Access was denied because of a security violation.
    """


class ScardWarningWrongChv(ScardException, code=0x8010006B):
    """
    The card cannot be accessed because the wrong PIN was presented.
    """


class ScardWarningChvBlocked(ScardException, code=0x8010006C):
    """
    The card cannot be accessed because the maximum number of PIN entry attempts has been reached.
    """


class ScardWarningEof(ScardException, code=0x8010006D):
    """
    The end of the smart card file has been reached.
    """


class ScardWarningCancelledByUser(ScardException, code=0x8010006E):
    """
    The action was cancelled by the user.
    """


class ScardWarningCardNotAuthenticated(ScardException, code=0x8010006F):
    """
    No PIN was presented to the smart card.
    """
