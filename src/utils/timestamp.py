from datetime import datetime,timedelta
from logging import getLogger

logger = getLogger(__name__)

class AcceptedTimeRanges:
    mins = [5,15,30]
    hours = [1,6,12]
    days = [1,3]
    weeks = [1,2]
    months = [1,3,6]
    years = [1]

class QueryTimeRangeEnum:
    mins = "min"
    hours = "h"
    days = "d"
    weeks = "w"
    months = "m"
    years = "y"

class TimeRangeUtil:
    def __init__(self):
        self.valid_time_ranges = ["min","h","d","w","m","y"]
    
    def is_valid_time_range(self,str_time_range:str) -> bool:
        for time_range in self.valid_time_ranges:
            if not str_time_range.endswith(time_range):
                continue
            
            time_range_val = str(str_time_range.split(time_range)[0])
            if not time_range_val.isnumeric():
                return False
            
            time_range_val = int(time_range_val)

            if time_range == QueryTimeRangeEnum.mins and time_range_val in AcceptedTimeRanges.mins:
                return True
            elif time_range == QueryTimeRangeEnum.hours and time_range_val in AcceptedTimeRanges.hours:
                return True
            elif time_range == QueryTimeRangeEnum.days and time_range_val in AcceptedTimeRanges.days:
                return True
            elif time_range == QueryTimeRangeEnum.weeks and time_range_val in AcceptedTimeRanges.weeks:
                return True
            elif time_range == QueryTimeRangeEnum.months and time_range_val in AcceptedTimeRanges.months:
                return True
            elif time_range == QueryTimeRangeEnum.years and time_range_val in AcceptedTimeRanges.years:
                return True
            else:
                return False
        return False
    
                
    def get_time_val(self,str_time_range:str):
        if not self.is_valid_time_range(str_time_range):
            print("Not a valid time range!!!!!!!!!!!!!!")
            return {}
        
        for str_time_stamp in self.valid_time_ranges:
            if str_time_range.endswith(str_time_stamp):
                return {
                    "time_range_type": str_time_stamp,
                    "time_range_val": int(str_time_range.split(str_time_stamp)[0])
                }
        return {}

    def get_timedelta(self,str_time_range:str):
        time_val = self.get_time_val(str_time_range)

        if time_val == {}:
            raise Exception(f"Invalid time_range provided! {str_time_range}")
        
        time_range_type = time_val['time_range_type']
        time_range_val = time_val['time_range_val']

        if time_range_type == QueryTimeRangeEnum.mins:
            return timedelta(minutes=time_range_val)
        elif time_range_type == QueryTimeRangeEnum.hours:
            return timedelta(hours=time_range_val)
        elif time_range_type == QueryTimeRangeEnum.days:
            return timedelta(days=time_range_val)
        elif time_range_type == QueryTimeRangeEnum.weeks:
            return timedelta(weeks=time_range_val)
        elif time_range_type == QueryTimeRangeEnum.months:
            return timedelta(days=30*time_range_val)
        elif time_range_type == QueryTimeRangeEnum.years:
            return timedelta(days=365*time_range_val)
        else:
            raise Exception(f"Invalid time_range provided: {str_time_range}. Not in range!")
    
    def get_last_utc_time_stamp(self,str_time_range:str):
        return datetime.utcnow() - self.get_timedelta(str_time_range)