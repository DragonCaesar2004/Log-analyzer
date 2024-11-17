from collections import Counter

from src.config import percentile_ratio
from src.log_object import LogObject
from src.project_types import LogStatistics


class LogStatisticsProcessor:

    def __init__(self):
        self.logs_count = 0
        self.resource_frequency = Counter()
        self.status_code_frequency = Counter()
        self.weights_all_logs = []  # измеряется в байтах
        self.unique_users = set()

    def calculate_statistics(self, log_object: LogObject) -> None:
        self.logs_count += 1
        self.resource_frequency[log_object.resource] += 1
        self.status_code_frequency[log_object.status_code] += 1
        self.weights_all_logs.append(log_object.body_bytes_sent)
        self.unique_users.add(log_object.ip_addr)

    def _calculate_percentile(self):
        self.weights_all_logs.sort()
        percentile_index = int(
            percentile_ratio * (len(self.weights_all_logs) - 1)
        )  # Вычисляем индекс для 95% перцентиля
        percentile_value = self.weights_all_logs[percentile_index]
        return percentile_value

    def get_statistics(self) -> LogStatistics:
        percentile = self._calculate_percentile()
        return LogStatistics(
            logs_count=self.logs_count,
            resource_frequency=self.resource_frequency,
            status_code_frequency=self.status_code_frequency,
            percentile=percentile,
            unique_users_number=len(self.unique_users),
            average_response_size=round(
                sum(self.weights_all_logs) / self.logs_count, 2
            ),
        )
