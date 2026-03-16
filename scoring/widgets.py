from django import forms

class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'
 
YEAR_CHOICES = [("", "Select a year"),]
YEAR_CHOICES = YEAR_CHOICES + [(year, year) for year in range(1940, 2035)]
    