from src.project_types import InputArgs, AdressTypes
from src.config import LogFields
from src.parsers.url_parser import url_log_stream
from src.parsers.file_parser import file_log_stream
from src.log_object import LogObject

class Manager:
    
    def __init__(self,input_args: InputArgs):
        self.input_args = input_args
        self.logs_count=0
        self.resource_frequency ={} #TODO
        
          
    def create_report(self)->None:
 
        for adress_type, adress_value in self.input_args.adresses:
            match adress_type:
                case AdressTypes.URL:
                    log_stream = url_log_stream
                case AdressTypes.FILE:
                    log_stream = file_log_stream
                case _:
                    pass # TODO

            for log_object in log_stream(adress_value):
                 
                if self._check_filter(log_object):
                    print(log_object)
                     
        
        
            
            
    def _check_filter(self, log_object: LogObject)->bool:
        
        conditions =[]

        if self.input_args.from_date :
            conditions.append( self.input_args.from_date  <= log_object[LogFields.LOCAL_TIME])  

        if self.input_args.to_date:
            conditions.append( self.input_args.to_date  >= log_object[LogFields.LOCAL_TIME])   
        
        if self.input_args.filter_field:
            filter_match = [filter_value == log_object[self.input_args.filter_field]  for filter_value in self.input_args.filter_value]
            conditions.append(any(filter_match))
         
        return all(conditions)
    

    # def _calculate_statistics(self,log_object:LogObject)->None:
    #     self.logs_count+=1
    #     if log_object[LogFields.RESOURCE]