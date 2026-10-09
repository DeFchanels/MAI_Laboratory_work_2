from dataclasses import dataclass
from datetime import datetime, timezone
from streamstats.errors import UnsupportedTimestampFormatError, IncorrectEventError


levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

@dataclass
class Event: # Класс для события
    timestamp: datetime
    level: str
    source: str
    message: str

    @staticmethod
    def get_event_from_dict(data, file_path, line_number):
        # Метод класса для валидации словаря данных и его преобразования в экземпляр класса
        required_fields = ["timestamp", "level", "source", "message"]  # Обязательные поля
        if not (all(field in data for field in required_fields)): # Если хотя бы 1 обязательного поля нет вызываем ошибку
            raise IncorrectEventError(f"Missing required event field, file: {file_path}, line: {line_number}")
        level = data["level"]
        if level not in levels: # Если уровень не находится в списке возможных уровней, вызываем ошибку
            raise IncorrectEventError(f"Invalid level: {level}, file: {file_path}, line: {line_number}")
        source = data["source"]
        if source.strip() == "": # Если source пустой, вызываем ошибку
            raise IncorrectEventError(f"Source is empty, file: {file_path}, line: {line_number}")
        timestamp = data["timestamp"]
        try:
            timestamp = timestamp.replace('Z', '+00:00')
            data_and_time = datetime.fromisoformat(timestamp) # Пытаемся обработать timestamp, если возникает ошибка, вызываем свой особый тип ошибки
            if data_and_time.tzinfo is None: # Если timezone не указана, считаем, что это UTCs
                data_and_time = data_and_time.replace(tzinfo=timezone.utc)
        except ValueError:
            raise UnsupportedTimestampFormatError(f"Invalid timestamp: {timestamp}, file: {file_path}, line: {line_number}")
        message = data["message"]
        return Event(data_and_time, level, source, message) # Если все хорошо, возвращаем экземпляр класса