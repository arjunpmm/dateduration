# -*- coding : utf-8 -*-
import datetime
import re

hashmonths = {
    'january': 1, 'jan': 1, '01': 1, '1': 1,
    'february': 2, 'feb': 2, '02': 2, '2': 2,
    'march': 3, 'mar': 3, '03': 3, '3': 3,
    'april': 4, 'apr': 4, '04': 4, '4': 4,
    'may': 5, '05': 5, '5': 5,
    'june': 6, 'jun': 6, '06': 6, '6': 6,
    'july': 7, 'jul': 7, '07': 7, '7': 7,
    'august': 8, 'aug': 8, '08': 8, '8': 8,
    'september': 9, 'sept': 9, 'sep': 9, '09': 9, '9': 9,
    'october': 10, 'oct': 10, '10': 10,
    'november': 11, 'nov': 11, '11': 11,
    'december': 12, 'dec': 12, '12': 12
}

def create_datedict(text):
    """

    :param text: the text containing a date range in the form <start date> to/- <end date>. The <start date> and <end date> can be either of the form:

    1) month(space or "'" or "." or "\")year 2) only year
    month can take the values from the hashmonths dictionary
    and year can be a 4 digit number between 1900-2099 or a 2 digit number:
    yy eg: 99, 04 etc
    yyyy eg: 1970, 2015 etc
    Supported for years between 1960 to 2059
    :return:
    month_found: boolean variable set to True if month is mentioned else False
    datedict["start_year"] : 4 digit starting year. Type: int
    datedict["end_year"] : 4 digit starting year. Type: int
    datedict["start_month"] : encoded month into an integer (ony returned if both start and end month are present in text)
    datedict["end_month"] : encoded month into an integer (ony returned if both start and end month are present in text)
    """
    #regex to detect year of the form 19xx and 20xx
    complete_year = "(19\d{2}|20\d{2})"
    tiny_year = "(\d{2})"
    year = "(" + complete_year + "|" + tiny_year + ")"
    regex_year = re.compile(year, re.IGNORECASE)

    datedict = {}
    _end = re.split("(" + year + "[ ]*(-|to)[ ]*)", text)[-1]
    _start = re.split("([ ]*(-|to)[ ]*)", text)[0]
    _end = _end.lower()
    _start = _start.lower()

    month_found = True
    try:
        start_month = re.split(r'[\s\'//\.]{1,}', _start)[0].lower()
        try:
            if start_month < 13 and start_month > 0:
                datedict["start_month"] = int(start_month)
        except:
            datedict["start_month"] = hashmonths[start_month]
    except:
        month_found = False

    if month_found:
        try:
            datedict["start_year"] = int(re.split(r'[\s\'//\.]{1,}', _start)[1])
        except:
            datedict["start_year"] = int(regex_year.search(_start).group(1))

    else:
        datedict["start_year"] = int(regex_year.search(_start).group(0))

    if re.match(r'present|now|current', _end):
        now = datetime.datetime.now()
        if month_found == True:
            datedict["end_month"] = int(now.month)
        datedict["end_year"] = int(now.year)

    else:

        if month_found:
            end_month = re.split(r'[\s\'//\.]{1,}', _end)[0].lower()
            try:
                if end_month < 13 and end_month > 0:
                    datedict["end_month"] = int(end_month)
            except:
                datedict["end_month"] = hashmonths[end_month]

        elif month_found == False and re.split(r'[\s\'//\.]{1,}', _end)[0].lower():
            end_month = re.split(r'[\s\'//\.]{1,}', _end)[0].lower()
            try:
                datedict["end_month"] = int(end_month)
            except:
                datedict["end_month"] = hashmonths[end_month]

        datedict["end_year"] = int(re.split(r'[\s\'//\.]{1,}', _end)[-1])

    if datedict["start_year"] < 60:
        datedict["start_year"] = 2000 + datedict["start_year"]
    elif datedict["start_year"] < 100:
        datedict["start_year"] = 1900 + datedict["start_year"]

    if datedict["end_year"] < 60:
        datedict["end_year"] = 2000 + datedict["end_year"]
    elif datedict["end_year"] < 100:
        datedict["end_year"] = 1900 + datedict["end_year"]

    if datedict["end_year"] > datedict["start_year"]:
        return datedict, month_found
    else:
        return None, None


def calculate(datedict):
    """

    :param datedict: a datedict containing the keys - start_year, end_year, start_month(optional), end_month(optional)
    :return: a total_months key added into the datedict and returned
    """
    datedict["total_months"] = 0
    if datedict["end_year"] > datedict["start_year"]:
        datedict["total_months"] += 12 * (datedict["end_year"] - datedict["start_year"])
    elif datedict["end_year"] < datedict["start_year"]:
        datedict["total_months"] += 12 * (datedict["end_year"] + (100 - datedict["start_year"]))

    try:
        if datedict["start_month"] < datedict["end_month"]:
            datedict["total_months"] += datedict["end_month"] - datedict["start_month"]
        elif datedict["start_month"] > datedict["end_month"]:
            datedict["total_months"] -= datedict["start_month"] - datedict["end_month"]

    except:
        pass
    return datedict

def duration(text):

    derived_daterange, month_found = create_datedict(text)
    if derived_daterange is not None:
        derived_daterange = calculate(derived_daterange)

    return derived_daterange


def months(text):
    try:
        return duration(text)["total_months"]
    except:
        return None

def years(text):
    try:
        return duration(text)["total_months"]/12
    except:
        return None

def year_start(text):
    try:
        return duration(text)["start_year"]
    except:
        return None

def year_end(text):
    try:
        return duration(text)["end_year"]
    except:
        return None

def month_start(text):
    try:
        return duration(text)["start_month"]
    except:
        return None

def month_end(text):
    try:
        return duration(text)["end_month"]
    except:
        return None

