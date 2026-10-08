from dataclasses import dataclass
from datetime import datetime
from streamstats.errors import UnsupportedTimestampFormatError, IncorrectEventError


levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

@dataclass
class Event:
    timestamp: datetime
    level: str
    source: str
    message: str

    @staticmethod
    def get_event_from_dict(data):
        # Метод класса для валидации словаря данных и его преобразования в экземпляр класса
        required_fields = ["timestamp", "level", "source", "message"]  # Обязательные поля
        if not (any(field in data for field in required_fields)): # Если хотя бы 1 обязательного поля нет вызываем ошибку
            raise IncorrectEventError(f"Missing required event field")
        level = data["level"]
        if level not in levels: # Если уровень не находится в списке возможных уровней, вызываем ошибку
            raise IncorrectEventError(f"Invalid level: {level}")
        source = data["source"]
        if source.strip() == "": # Если source пустой, вызываем ошибку
            raise IncorrectEventError(f"Source is empty")
        timestamp = data["timestamp"]
        try:
            data_and_time = datetime.fromisoformat(timestamp) # Пытаемся обработать timestamp, если возникает ошибка, вызываем свой особый тип ошибки
        except ValueError:
            raise UnsupportedTimestampFormatError(f"Invalid timestamp: {timestamp}")
        message = data["message"]
        return Event(data_and_time, level, source, message) # Если все хорошо, возвращаем экземпляр класса