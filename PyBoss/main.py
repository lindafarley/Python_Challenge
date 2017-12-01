#Modules
import os 
import csv
#Import datetime
from datetime import datetime

#Define path to file - path not working
employee_data1 = "./employee_data2.csv"

#State abbreviation dictionary
us_state_abbrev = {
	    'Alabama': 'AL',
	    'Alaska': 'AK',
	    'Arizona': 'AZ',
	    'Arkansas': 'AR',
	    'California': 'CA',
	    'Colorado': 'CO',
	    'Connecticut': 'CT',
	    'Delaware': 'DE',
	    'Florida': 'FL',
	    'Georgia': 'GA',
	    'Hawaii': 'HI',
	    'Idaho': 'ID',
	    'Illinois': 'IL',
	    'Indiana': 'IN',
	    'Iowa': 'IA',
	    'Kansas': 'KS',
	    'Kentucky': 'KY',
	    'Louisiana': 'LA',
	    'Maine': 'ME',
	    'Maryland': 'MD',
	    'Massachusetts': 'MA',
	    'Michigan': 'MI',
	    'Minnesota': 'MN',
	    'Mississippi': 'MS',
	    'Missouri': 'MO',
	    'Montana': 'MT',
	    'Nebraska': 'NE',
	    'Nevada': 'NV',
	    'New Hampshire': 'NH',
	    'New Jersey': 'NJ',
	    'New Mexico': 'NM',
	    'New York': 'NY',
	    'North Carolina': 'NC',
	    'North Dakota': 'ND',
	    'Ohio': 'OH',
	    'Oklahoma': 'OK',
	    'Oregon': 'OR',
	    'Pennsylvania': 'PA',
	    'Rhode Island': 'RI',
	    'South Carolina': 'SC',
	    'South Dakota': 'SD',
	    'Tennessee': 'TN',
	    'Texas': 'TX',
	    'Utah': 'UT',
	    'Vermont': 'VT',
	    'Virginia': 'VA',
	    'Washington': 'WA',
	    'West Virginia': 'WV',
	    'Wisconsin': 'WI',
	    'Wyoming': 'WY',
	}

#For header titles given in instructions, create empty lists to store data
Emp_ID = []
First_Name = []
Last_Name = []
DOB = []
SSN = []
State = []

#Open the file using "read" mode
#When opening the file related to the csvpath defined above as employee_data1 
with open(employee_data1, newline="") as csvfile:
	#Set csvreader equal to the function of opening the csvfile 
	csvreader = csv.reader(csvfile, delimiter=",")

	#Skip header row
	next(csvreader)
	
	for row in csvreader:

		#Add rows to above lists
		#Add data from first column to Emp_ID
		Emp_ID.append(row[0])

		#Split column 2 by a space
		Name_Split = row[1].split(" ")
		#Add first names to First_Name
		First_Name.append(Name_Split[0])
		#Add last names to Last_Name
		Last_Name.append(Name_Split[1])

		#Change format from oldformat to new format
		#Define old format
		oldformat = row[2]
		datetimeobject = datetime.strptime(oldformat, "%Y-%m-%d")
		#Create new format
		newformat = datetimeobject.strftime("%d-%m-%Y")
		#Add the formatted DOB into DOB list
		DOB.append(newformat)

		#Split column 4 by dashes
		SSN_Split = (row[3].split("-"))
		#Add the third index (last 4 digits of social) to SSN list
		SSN.append(SSN_Split[2])

		#Use column 5 as key for dictionary. Add value from dictionary to State list
		State.append(us_state_abbrev[row[4]])

#Zip lists together
cleaned_csv = zip(Emp_ID, First_Name, Last_Name, DOB, SSN, State)

#Set variable for output file
output_file = "./employee_data2_new.csv"
#Open the output file
with open(output_file, "w", newline="") as datafile:
	writer = csv.writer(datafile)
	#Write the first row (column headers)
	writer.writerow(["Emp ID", "First Name", "Last Name", "DOB", "SSN", "State"])
	
	#Write rows
	writer.writerows(cleaned_csv)
