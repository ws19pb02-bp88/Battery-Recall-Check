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
        request = requests.post(url = 'https://qualityprograms.apple.com/snlookup/062019', data = data, headers = headers)
        response = json.loads(request.text)
        if response["status"] == "E00":
            dict = {"Serial": serial,
                    "Computer_Name": row["Computer Name"],
                    "Status": "Eligible"
                    }
            computer_list.append(dict)
        elif response["status"] == "E01":
            dict = {"Serial": serial,
                    "Computer_Name": row["Computer Name"],
                    "Status": "Ineligible"
                    }
            computer_list.append(dict)
        elif response["status"] == "E99":
            dict = {"Serial": serial,
                    "Computer_Name": row["Computer Name"],
                    "Status": "Web Error"
                    }
            computer_list.append(dict)
        elif response["status"] == "FE01":
            dict = {"Serial": None,
                    "Computer_Name": row["Computer Name"],
                    "Status": "Empty Serial"
                    }
            computer_list.append(dict)
        elif response["status"] == "FE03":
            dict = {"Serial": serial,
                    "Computer_Name": row["Computer Name"],
                    "Status": "Invalid Serial"
                    }
            computer_list.append(dict)

for computer in computer_list:
    if computer["Status"] == "Eligible":
        print("Computer Name: {}").format(computer["Computer_Name"])
        print("Serial Number: {}").format(computer["Serial"])
        print("===================")

