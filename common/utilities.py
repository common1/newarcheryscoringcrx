from datetime import date, timedelta
import calendar

DAYS_OF_WEEK = {
    "monday": 0,
    "maandag": 0,
    "tuesday": 1,
    "dinsdag": 1,
    "wednesday": 2,
    "woensdag": 2,
    "thursday": 3,
    "donderdag": 3,
    "friday": 4,
    "vrijdag": 4,
    "saturday": 5,
    "zaterdag": 5,
    "sunday": 6,
    "zondag": 6,
}

def get_rounds_info(prefix, distance, unit, year, day):
    # Start a januari 1 of the given year
    d = date(year, 1,1)

    # look for the first 'day'
    d += timedelta(days=(DAYS_OF_WEEK[day]) % 7)
    
    day_strings = []
    # Loop through the year, as long as we are in the same year
    while d.year == year:
        day_string = f"{prefix} {distance} {unit} {day} {d.day} {calendar.month_name[d.month]} {d.year}"
        day_strings.append(day_string)
        d += timedelta(days = 7) # Add a week

    return day_strings

if __name__ == "__main__":
    day_strings = get_rounds_info("Indoor", 18, "meter", 2026, 'donderdag')
    
    for day in day_strings:
        print(day)        

