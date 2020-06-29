from datetime import datetime, timedelta

class TheTime:  
    """
    處理 TodayStock 裡面的 StartDateTime, EndDateTime
    StartDateTime --> 轉為今日 14:00:00
    EndDateTime --> 轉為明日 13:59:59
    """
    def __init__(self):   
 
        # strftime 2 strptime --> type = datetime
        self.start_date_time = self.__strdateConverter(self.__objdateConverter(datetime.now().date(), case=1))
        self.end_date_time = self.__strdateConverter(self.__objdateConverter(datetime.now().date(), case=2))

    def __objdateConverter(self, obj_date, case=1):
        """
        date 物件轉 strftime + 指定時間
        """
        if case == 1:
            return obj_date.strftime("%Y%m%d") + "15:30:00:00"
        elif case == 2:
            return (obj_date + timedelta(days=1)).strftime("%Y%m%d") + "15:29:59:00"
        else:
            return False

    def __strdateConverter(self, str_datetime):
        """
        strftime 轉 strptime 
        """
        return datetime.strptime(str_datetime, "%Y%m%d%H:%M:%S:%f")