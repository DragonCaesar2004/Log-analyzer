from src.project_types import InputArgs 
from src.parsers.url_parser import UrlParser
from src.parsers.file_parser import FileParser
from src.log_object import LogObject

class Manager:
    
    def __init__(self,input_args: InputArgs):
        self.input_args = input_args
        self.logs_count=0
        self.frequenses ={} #TODO
        
          
    def create_report(self)->None:
        parser = UrlParser()
        # Используем метод log_stream и итерируемся по результатам
        for url in self.input_args.urls:
            for log_object in parser.log_stream( url):
                # Теперь log_object - это экземпляр LogObject
                if self.check_filter(log_object):
                    pass

        parser = FileParser()
        print(self.input_args.filter_value)
        for file in self.input_args.files:
            for log_object in parser.log_stream(file):
                 if self.check_filter(log_object):
                    print(log_object ) 
                    pass
            
            
    def check_filter(self, log_object: LogObject)->bool:
        
        conditions =[]

        if self.input_args.from_date :
            conditions.append( self.input_args.from_date  <= log_object['local_time'])  # проверить 
        if self.input_args.to_date:
            conditions.append( self.input_args.to_date  >= log_object['local_time'])  # проверить 
        
        if self.input_args.filter_field:
            for filter_value in self.input_args.filter_value:
                conditions.append(filter_value == log_object[self.input_args.filter_field])
                     
        
        return all(conditions)