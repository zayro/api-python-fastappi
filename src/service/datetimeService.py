from datetime import datetime, timedelta


# Example
# timedelta(days=270, hours=9, minutes=18)


def time_to_seconds(**kwargs):
    set_time = timedelta(**kwargs)
    return round(set_time.total_seconds() * 1000)

rs = time_to_seconds(minutes=2)
print(rs)

def time_print():
    current_date_and_time = datetime.now()
    print("The current year is ", current_date_and_time.year)  # Output: The current year is  2022
    print("The current month is ", current_date_and_time.month)  # Output: The current month is  3
    print("The current day is ", current_date_and_time.day)  # Output: The current day is  19
    print("The current hour is ", current_date_and_time.hour)  # Output: The current hour is  10
    print("The current minute is ", current_date_and_time.minute)  # Output: The current minute is  49
    print("The current second is ", current_date_and_time.second)  # Output: The current second is  18


# convert from datetime to timestamp
# rs = datetime.timestamp(datetime.now())

# convert the timestamp to a datetime object in the local timezone
# dt_object = datetime.fromtimestamp(timestamp)
 

def convert_timestamp_to_date(sec: int):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    print("seconds value in hours:", hour)
    print("seconds value in minutes:", min)
    return "%02d:%02d:%02d" % (hour, min, sec)
