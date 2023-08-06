# define variables
# dont change
fdd = 79
daynames = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنج شنبه', 'جمعه']
monthname = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
grgdayofmonthleap = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
grgdayofmonth = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]


# check leap year
def isleap(year):
    if ((year % 100 == 0) and (year % 400 == 0)) or ((year % 100 != 0) and (year % 4 == 0)):
        return True
    else:
        return False


# convert gregorian date to persian(shamsi) date
# @param year is gregorian year
# @param month is gregorian month
# @param day is gregorian day
# return persian(shamsi) date in dict format
def topersia(year, month, day):
    if isleap(year):
        daycount = grgdayofmonthleap[month - 1] + day
    else:
        daycount = grgdayofmonth[month - 1] + day
    if isleap(year - 1):
        dd = 11
    else:
        dd = 10
    if daycount > fdd:
        daycount = daycount - fdd
        if daycount <= 186:
            if daycount % 31 == 0:
                prmonth = daycount / 31
                prday = 31
            else:
                prmonth = (daycount / 31) + 1
                prday = daycount % 31
            pryear = daycount - 621
        else:
            daycount = daycount - 186
            if daycount % 30 == 0:
                prmonth = (daycount / 30) + 6
                prday = 30
            else:
                prmonth = (daycount / 30) + 7
                prday = (daycount % 30)
            pryear = year - 621
    else:
        daycount = daycount + dd
        if daycount % 30 == 0:
            prmonth = (daycount / 30) + 9
            prday = (daycount % 30)
        else:
            prmonth = (daycount / 30) + 10
            prday = (daycount % 30)
        pryear = year - 622
    return {
        'year': pryear,
        'month': int(prmonth),
        'day': prday,
        'dayname': daynames[((prday % 7) - 1)],
        'monthname': monthname[(int(prmonth) - 1)]
    }
