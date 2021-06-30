import yfinance as yfc
import datetime
import pyperclip
from sys import exit

def grab_inputs():
    try:
        date = datetime.datetime.strptime(input("Input Date (MM/DD/YYYY) >>> "), "%m/%d/%Y")
    except ValueError:
        print("Invalid Date Format, relaunch program and try again.")
    extra_date = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if date.weekday() == 0:
        date = date - datetime.timedelta(days=2)
    elif date.weekday() == 6 or date.weekday() == 7:
        print("Day Invalid: Weekend - Program will Exit now.")
        exit()
    date = date.strftime("%Y-%m-%d")
    tickers = input("Input comma separated list of tickers >>>").upper().replace(" ", "").split(",")
    return date, extra_date, tickers

def get_data():
    output_raw = []
    date, extra_date, tickers = grab_inputs()
    try:
        for n in tickers:
            data = yfc.Ticker(n).history(start=date, end=extra_date)
            output_raw.append([round(j, 2) for j in [data.iat[0, 3], data.iat[1, 0], data.iat[1, 3], data.iat[1, 1], data.iat[1, 2], data.iat[1, 4]]])
    except IndexError:
        print("Data Issue - Check if Yahoo Finance has Data on this day and whether the markets were open.")
        exit()
    return output_raw

def copy_clipboard():
    output_raw = get_data()
    text = ""
    for i in output_raw:
        text += ",".join(map(str, i)) + "\r\n"
    pyperclip.copy(text)

def execute():
    copy_clipboard()

execute()