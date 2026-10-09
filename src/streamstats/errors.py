class StreamStatsError(Exception):
    pass


class UnsupportedFileFormatError(StreamStatsError): # Неподдерживаемый формат файла
    """
    Occurs when an unsupported file type is specified.
    """
    pass


class UnsupportedTimestampFormatError(StreamStatsError): # Неверный формат временной метки
    """
    Occurs when an unsupported timestamp format is specified.
    """
    pass


class IncorrectEventError(StreamStatsError): # Ошибка в определенном событии
    """
    Occurs when not all required arguments for events are specified, or when one of the arguments does not meet the protocol requirements.
    """
    pass


class CLIConfigureError(StreamStatsError): # Ошибка в CLI
    """
    Occurs due to CLI configuration errors or invalid arguments.
    """
    pass