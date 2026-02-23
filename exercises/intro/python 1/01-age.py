#!/usr/bin/python3
from datetime import date

current_date = date.today()
current_year = current_date.year

year = int(input("Enter birth year: "))
month = int(input("Enter birth month: "))
day = int(input("Enter birth day: "))
birthday = date(year, month, day)

age = current_year - birthday.year

century = 100

print("You are currently", age)
print("In 100 years you'll be", age + century)
print("You'll turn 100 in the year", birthday.year + 100)
