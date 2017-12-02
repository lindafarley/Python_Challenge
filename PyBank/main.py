#Modules
import os
import csv

#Define path to file
budget_data_2 = "./budget_data_2.csv"

#Create lists for rows 1 and 2
months = []
revenue = []
revenue_change = []
highest_increase_date = ""
highest_decrease_date = ""

#Read file
with open(budget_data_2, newline="") as csvfile:
	csvreader = csv.reader(csvfile, delimiter=",")

	#Skip header row
	next(csvreader)

	#Loop through rows to append columns to lists created
	for row in csvreader:
		
		#Add first column to months list
		months.append(row[0])
		#create variable for length of months list
		months_number = len(months)

		#Add row 2 to revenue list
		revenue.append(int(row[1]))
		revenue_sum = sum(revenue)

	#Set index to 0
	index = 0

	#Loop through revenue list
	for value in revenue:

		#If the index is less than the length of the list
		if index + 1 < len(revenue):
			#For each index in revenueu list, subtract the value of that index from the value of the next index.
			change = revenue[index+1] - revenue[index]
			#Add the difference to revenue_change list
			revenue_change.append(change)

			if change == max(revenue_change):
				highest_increase_date = months[index]

			if change == min(revenue_change):
				highest_decrease_date = months[index]

			#Add 1 to index 
			index = index + 1

	#Average the list
	mean_change = sum(revenue_change)/len(revenue_change)

	#Find the greatest increase in the list:
	highest_increase = max(revenue_change)

	#Find the greatest decrease in the list:
	highest_decrease = min(revenue_change)



print("Financial Analysis")
print("------------------")
print("Total Months: " + str(months_number))
print("Total Revenue: " + str(revenue_sum))
print("Average Revenue Change: " + str(mean_change))
print("Greatest Increase in Revenue: " + str(highest_increase_date) + " " + str(highest_increase))
print("Greatest Decrease in Revenue: " + str(highest_decrease_date) + " " + str(highest_decrease))

#Write to a txt file
file = open("./budget_data_2_new.txt", "w")

file.write("Financial Analysis\r\n")
file.write("------------------\r\n")
file.write("Total Months: " + str(months_number) + "\r\n")
file.write("Total Revenue: " + str(revenue_sum) + "\r\n")
file.write("Average Revenue Change: " + str(mean_change) + "\r\n")
file.write("Greatest Increase in Revenue: " + str(highest_increase_date) + " " + str(highest_increase) + "\r\n")
file.write("Greatest Decrease in Revenue: " + str(highest_decrease_date) + " " + str(highest_decrease) + "\r\n")