
import numbers
from . import jalali
from django.utils import timezone

def numbers_perions_converter(mystr):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        mystr = mystr.replace(e, p)

    return mystr

def jalali_converter(time):
    jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
               "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

    # Ensure the time is converted to local time
    time = timezone.localtime(time)

    # Format the time to a string
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    
    # Convert Gregorian date to Jalali date
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    
    # Convert the tuple to a list for mutability
    time_to_list = list(time_to_tuple)
    
    # Replace month number with Persian month name
    time_to_list[1] = jmonths[time_to_list[1] - 1]

    # Format the output string
    output = "{},{},{} ،ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute,
    )

    # Convert English numerals to Persian numerals
    return numbers_perions_converter(output)