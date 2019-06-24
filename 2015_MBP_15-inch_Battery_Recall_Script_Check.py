"""
https://support.apple.com/15-inch-macbook-pro-battery-recall
Check a CSV containing the serial numbers of MacBook Pros against the
Apple Battery Recall.
The CSV must contain two columns: "Serial Number" and "Computer Name".
"""


import requests
import json
import uuid
import csv

file = "/path/to/serials.csv"

computer_list = []

with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        serial = row["Serial Number"]
        guid = str(uuid.uuid4())
        data = json.dumps({'serial': serial, 'GUID': guid})
        headers = {'content-type': 'application/json'}
        request = requests.post(url='https://qualityprograms.apple.com/snlookup/062019', data=data, headers=headers)
        response = json.loads(request.text)
        if response["status"] == "E00":
            status = "Eligible"
        elif response["status"] == "E01":
            status = "Ineligible"
        elif response["status"] == "E99":
            status = "Web Error"
        elif response["status"] == "FE01":
            status = "Empty Serial"
        elif response["status"] == "FE03":
            status = "Invalid Serial"
        dict = {"Serial": serial,
                "Computer_Name": row["Computer Name"],
                "Status": status
                }
        computer_list.append(dict)

for computer in computer_list:
    if computer["Status"] == "Eligible":
        print("Computer Name: {}").format(computer["Computer_Name"])
        print("Serial Number: {}").format(computer["Serial"])
        print("===================")
