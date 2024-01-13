import requests
import pandas as pd
import csv
import time
import argparse
from datetime import datetime
from utils import *

parser = argparse.ArgumentParser(
    description="Script to automate the sending of messages extracted from an Excel file."
)
parser.add_argument(
    "--initial-row",
    type=int,
    nargs="?",
    default=None,
    help="The initial_row parameter indicates the starting point from which the script will begin to read the data from the Excel file before sending it. Default 1",
)
parser.add_argument(
    "--country-code",
    type=str,
    nargs="?",
    default=None,
    help="The country_code parameter indicates the country code to concatenate with the phone number. Default value: 591. Empty value set ''",
)
parser.add_argument(
    "--sleep",
    type=int,
    nargs="?",
    default=None,
    help="The country_code The parameter indicates the time in seconds that the script will wait before sending the next message. It is recommended to use a time equal to or greater than 10 seconds. Default value: 10 sec.",
)
parser.add_argument(
    "--test",
    type=str,
    nargs="?",
    default=None,
    help="The test number send message",
)
args = parser.parse_args()

base_url = "http://localhost:5004"
filename = "lista.xlsx"
columns = ["name", "phone", "content"]
count_records = 0
initial_row = args.initial_row if args.initial_row is not None else 1
country_code = args.country_code if args.country_code is not None else 591
sleep = args.sleep if args.sleep is not None else 10

test = args.test


def init():
    if test is not None:
        print_info(
            f"Sending test message to {test}...",
            end="",
            flush=True,
        )
        data = {"phone": test, "message": "Test message from script"}
        try:
            r = requests.post(base_url + "/message/send", data=data)
            status = r.json()["status"]
            print_info(f"[{status}]", flush=True)
        except Exception as e:
            print_error(f"[{e}]", flush=True)
            status = "FAILED"
        print_success("-------------------")
        print_success(f"[{datetime.now().time()}] Script Terminated")
        print_success("-------------------")
    else:
        read_excel()


def read_excel():
    if initial_row <= 0:
        print_error("Initial row must be greater than or equal to 1")
        return
    print_warning("You can use -h for more information.")
    time.sleep(1)
    print_success(f"[VAR] initial_row config value => {initial_row}")
    time.sleep(1)
    print_success(f"[VAR] country_code config value => {country_code}")
    time.sleep(1)
    print_success(f"[VAR] sleep config value => {sleep}")
    time.sleep(1)
    print_info("----------------")
    print_success("Starting script")
    print_info("----------------")
    time.sleep(1)
    try:
        print_info(f"[1] check excel file '{filename}'", end="")
        df = pd.read_excel(filename, skiprows=range(1, initial_row))
        print_info("...[Ok]", flush=True)
        time.sleep(1)
    except Exception as e:
        print_error("...[ERR]", flush=True)
        print_error(f"Failed read excel: {e}")
        return
    print_info(f"[2] check columns {columns}")
    for column in columns:
        if column in df.columns:
            print_info(f"[*] Column '{column}' has {len(df[column])} records")
            count_records = len(df[column])
            time.sleep(1)
        else:
            print_error(f"[FAIL] '{column}' not exists")
            return

    if initial_row > count_records:
        print_error(
            f"[ERR] 'initial_row' cannot exceed the number of records in the Excel file ({initial_row} > {count_records})"
        )
        return

    print_info("----------------")
    print_success(
        f"Starting sending from record number {initial_row}/{count_records} messages."
    )
    print_info("----------------")
    time.sleep(1)
    with open("record.csv", mode="w", newline="") as archivo_csv:
        csv_file = csv.writer(archivo_csv)
        csv_file.writerows([["#", "time"] + columns + ["status"]])
        for index, row in df.iterrows():
            name = row[columns[0]]
            phone = str(country_code) + str(row[columns[1]])
            content = row[columns[2]]
            print_info(
                f"[{datetime.now().time()} - {(index + initial_row)}/{count_records}] {phone} sending...",
                end="",
                flush=True,
            )
            content_parse = content.replace("\\n", "\n")
            data = {"phone": phone, "message": content_parse}
            try:
                r = requests.post(base_url + "/message/send", data=data)
                status = r.json()["status"]
                print_info(f"[{status}]", flush=True)
            except Exception as e:
                print_error(f"[{e}]", flush=True)
                status = "FAILED"
            csv_file.writerows(
                [
                    [
                        (index + initial_row),
                        datetime.now().time(),
                        name,
                        phone,
                        content,
                        status,
                    ]
                ]
            )
            time.sleep(sleep)
    print_success("-------------------")
    print_success(f"[{datetime.now().time()}] Script Terminated")
    print_success("-------------------")


init()
