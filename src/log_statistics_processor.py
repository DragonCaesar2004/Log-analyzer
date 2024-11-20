from collections import Counter

from src.config import percentile_ratio
from src.log_object import LogObject
from src.project_types import LogStatistics


class LogStatisticsProcessor:
    '''
    Класс для обработки статистики логов. Анализирует и собирает метрики 
    на основе объектов логов, такие как количество записей, частота ресурсов, коды статусов, 
    уникальные пользователи и статистики по размеру ответа.
    '''
    def __init__(self)-> None:
        self.logs_count:int = 0 # Общее количество обработанных логов.
        self.resource_frequency:Counter[str] = Counter() # Частота запросов к ресурсам.
        self.status_code_frequency:Counter[int] = Counter() #Частота встречаемости HTTP-кодов статуса.
        self.weights_all_logs:list[int] = []  # Список размеров всех ответов (в байтах).
        self.unique_users:set[str] = set() # Множество уникальных IP-адресов.

    def calculate_statistics(self, log_object: LogObject) -> None:
        '''
        Обновляет статистику на основе нового объекта лога.
        Параметры:
            log_object (LogObject): Лог для анализа.
        Возвращаемое значение:
            None
        '''
        self.logs_count += 1
        self.resource_frequency[log_object.resource] += 1
        self.status_code_frequency[log_object.status_code] += 1
        self.weights_all_logs.append(log_object.body_bytes_sent)
        self.unique_users.add(log_object.ip_addr)

    def _calculate_percentile(self)-> int:
        '''
        Вычисляет 95-й перцентиль по размерам ответов.
        Возвращаемое значение:
            int: Значение перцентиля или -1, если данных недостаточно.
        '''
        if len(self.weights_all_logs)==0: return -1 # Обозначение, что перцентиля не существует  
        self.weights_all_logs.sort()
        percentile_index = int(
            percentile_ratio * (len(self.weights_all_logs) - 1)
        )   

        percentile_value = self.weights_all_logs[percentile_index]
        return percentile_value

    def get_statistics(self) -> LogStatistics:
        '''
        Возвращает собранную статистику.
        Возвращаемое значение:
            LogStatistics: Объект со всеми вычисленными метриками.
        '''
        percentile = self._calculate_percentile()
        
        return LogStatistics(
            logs_count=self.logs_count,
            resource_frequency=self.resource_frequency,
            status_code_frequency=self.status_code_frequency,
            percentile=percentile,
            unique_users_number=len(self.unique_users),
            average_response_size=round(
                sum(self.weights_all_logs) / self.logs_count, 2
            ) if self.logs_count else -1,
        )
