# import abc
# from src.log_object import LogObject

# class LogParser(abc.ABC):
#     '''
#     LogParser - интерфес для парсеров. Так как они могут парсить через URL, либо из локальных файлов 
#     '''
#     @abc.abstractmethod
#     def log_stream(path:str)->LogObject:
#         '''
#         Функция для осуществления потоковой обработки данных
#         '''
#         ...