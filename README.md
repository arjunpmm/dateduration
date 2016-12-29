# dateduration
derives the duration of months/years when a date range is given as string input

input a string that contains a range of dates
the text containing a date range in the form <start date> to/- <end date>. The <start date> and <end date> can be either of the form:

    1) month(space or "'" or "." or "\")year 2) only year
    month can take the values from the hashmonths dictionary
    and year can be a 4 digit number between 1900-2099 or a 2 digit number:
    yy eg: 99, 04 etc
    yyyy eg: 1970, 2015 etc
    Supported for years between 1960 to 2059
    
Returns:

        month_found: boolean variable set to True if month is mentioned else False
        datedict["start_year"] : 4 digit starting year. Type: int
        datedict["end_year"] : 4 digit starting year. Type: int
        datedict["total_months"]: total number of months
        datedict["start_month"] : encoded month into an integer (ony returned if both start and end month are present in text)
        datedict["end_month"] : encoded month into an integer (ony returned if both start and end month are present in text)
    
