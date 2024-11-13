from src.project_types import InputArgs 
from src.parsers.url_parser import UrlParser
from src.parsers.file_parser import FileParser

class Manager:
    
    def __init__(self,input_args: InputArgs):
        self.input_args = input_args
        self.logs_count=0
        self.frequenses ={} #TODO
        
          
    def create_report(self)->None:
        parser = UrlParser()
        # log_url='https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs'
        # log_url='logs/logs1.txt'
    # Используем метод log_stream и итерируемся по результатам
        for url in self.input_args.urls:
            for log_object in parser.log_stream( url):
                # Теперь log_object - это экземпляр LogObject
                if self.check_filter(log_object):

                    print(log_object )  

        parser = FileParser()
        for file in self.input_args.files:
            for log_object in parser.log_stream(file):
                # Теперь log_object - это экземпляр LogObject
                print(log_object ) 
                print()
            
    def check_filter(self, log_object)->bool:
        log_after_from_date = ...
        log_until_to_date = ...
        