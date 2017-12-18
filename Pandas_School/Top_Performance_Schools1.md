

```python
import pandas as pd 
import numpy as np
```


```python
#Read csv
# Create a path for the CSV file desired
csv_students = "./students_complete.csv"

# Read the CSV into a Pandas DataFrame
students_df = pd.read_csv(csv_students)
```


```python
#Read csv
# Create a reference the CSV file desired
csv_schools = "./schools_complete.csv"

# Read the CSV into a Pandas DataFrame
schools_df = pd.read_csv(csv_schools)
```


```python
#Rename columns in data frames to be more descriptive
schools_df_renamed = schools_df.rename(columns ={"name": "School Name",
                                                 "type": "School Type",
                                                 "size": "School Size",
                                                 "budget": "School Budget"})
students_df_renamed = students_df.rename(columns={"name": "Student Name",
                                                  "gender":"Student Gender",
                                                  "grade": "Student Grade",
                                                  "school": "School Name",
                                                  "reading_score": "Student Reading Score",
                                                  "math_score": "Student Math Score"})

```


```python
# Find number of schools
unique_schools = len(schools_df_renamed["School Name"])
#Find number of students
num_students = len(students_df_renamed["Student Name"])
#Find total schools' budget
total_budget = schools_df_renamed["School Budget"].sum()
#Find average math score
avg_math = students_df_renamed["Student Math Score"].mean()
#Find average reading score
avg_read = students_df_renamed["Student Reading Score"].mean()   
#Find percent passed math
student_math = students_df_renamed[students_df_renamed["Student Math Score"] >= 70]
stu_passed_math = (len(student_math) / len(students_df_renamed)) * 100
#Find percent passed reading
student_reading = students_df_renamed[students_df_renamed["Student Reading Score"] >= 70]
stu_passed_reading = (len(student_reading) / len(students_df_renamed)) * 100   
#Find percent passed overall
overall_pass = (stu_passed_reading + stu_passed_math) / 2
```


```python
#***Create District Summary Table 
district_summary = pd.DataFrame(
    {"Total Schools": [unique_schools],
     "Total Students": [num_students],
     "Total Budget": [total_budget],
     "Average Math Score": [avg_math],
     "Average Reading Score": [avg_read],
     "% Passing Math": [stu_passed_math],
     "% Passing Reading": [stu_passed_reading],
     "% Overall Passing Rate": [overall_pass]})

column_names = ["Total Schools", "Total Students","Total Budget", "Average Math Score", 
                "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing Rate"]

district_summary = district_summary[column_names]
district_summary = district_summary.set_index(["Total Schools"])
district_summary
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Total Schools</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>15</th>
      <td>39170</td>
      <td>24649428</td>
      <td>78.985371</td>
      <td>81.87784</td>
      <td>74.980853</td>
      <td>85.805463</td>
      <td>80.393158</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Merge schools_df_renamed and students_df_renamed
merge_table = pd.merge(schools_df_renamed, students_df_renamed, on="School Name")
#Set index to school name
merge_table =merge_table.set_index("School Name")
```


```python
merge_table_reset = merge_table.reset_index()
```


```python
#Get school type, size, budget grouped by school
school_type = pd.DataFrame(schools_df_renamed.set_index(["School Name"])["School Type"])
school_type = school_type.reset_index()
school_size = pd.DataFrame(schools_df_renamed.set_index(["School Name"])["School Size"])
school_size = school_size.reset_index()
school_budget = pd.DataFrame(schools_df_renamed.set_index(["School Name"])["School Budget"])
school_budget = school_budget.reset_index()
```


```python
#Find average reading score for each school
avg_reading_score = merge_table.groupby(["School Name"])["Student Reading Score"].mean()
avg_reading_score = pd.DataFrame(avg_reading_score)
avg_reading_score = avg_reading_score.rename(columns ={"Student Reading Score": "Average Student Reading Score"})
avg_reading_score = avg_reading_score.reset_index()
#Find Average Math Score by School
avg_math_score = merge_table.groupby(["School Name"])["Student Math Score"].mean()
avg_math_score = pd.DataFrame(avg_math_score)
avg_math_score = avg_math_score.rename(columns ={"Student Math Score": "Average Student Math Score"})
avg_math_score = avg_math_score.reset_index()
```


```python
#Find percent passing reading and math

#Define function name and variable names
def passing_grade(df, column, school_name):
    #no_passing = the number of items in the the identified merge_table column if they are >= 70 and are part of the unique school name in the for loop
    no_passing = len(df[(df[column] >= 70) & (df['School Name'] == school_name)])
    #total_students = the number of rows in which that school name appears
    total_students = len(df[df['School Name'] == school_name])
    #pct_passing = the number of students who passed divided by the total number of students
    pct_passing = (no_passing/total_students) * 100
    #return a dictionary containing the school name: and the percent passed
    return {school_name:pct_passing} 

#Create new dictionary to hold lists of school names and percent passed per school
passed_reading_dict = {"School Name":[],"Percent Passed Reading": []}
#loop through the unique values in the school name column in merge_table
for school_name in merge_table_reset['School Name'].unique():
    #Run the passing_grade function on the Student Reading Score column of the merge_table
    temp_return = passing_grade(merge_table_reset, 'Student Reading Score', school_name)
    #Loop through temp_return
    for key in temp_return:
        #append each school name to the school name list in the dictionary
        passed_reading_dict["School Name"].append(key)
        #append each percentage to the "Percent Passed Reading" list in the dictionary
        passed_reading_dict["Percent Passed Reading"].append(temp_return[key])
#Put the columns in order
columns_reading = ["School Name", "Percent Passed Reading"]
#Create dataframe
passed_reading_school = pd.DataFrame(passed_reading_dict)[columns_reading]

#Create new dictionary to hold lists of school names and percent passed per school
passed_math_dict = {"School Name":[],"Percent Passed Math": []}
#loop through the unique values in the school name column in merge_table
for school_name in merge_table_reset['School Name'].unique():
    #Run the passing_grade function on the Student Reading Score column of the merge_table
    temp_return = passing_grade(merge_table_reset, 'Student Math Score', school_name)
    #Loop through temp_return
    for key in temp_return:
        #append each school name to the school name list in the dictionary
        passed_math_dict["School Name"].append(key)
        #append each percentage to the "Percent Passed Reading" list in the dictionary
        passed_math_dict["Percent Passed Math"].append(temp_return[key])
#Put the columns in order
columns_math = ["School Name", "Percent Passed Math"]
#Create dataframe
passed_math_school = pd.DataFrame(passed_math_dict)[columns_math]
```


```python
#Merge: School Type, School Size, School Budget
school_summary = school_type.merge(school_size,on=["School Name"]).merge(school_budget,on=["School Name"])
#Add new column for Per Student Budget
school_summary["Per Student Budget"] = school_summary["School Budget"] / school_summary["School Size"]
#Merge in Average Reading Score and Average Math Score
school_summary = school_summary.merge(avg_reading_score,on=["School Name"]).merge(avg_math_score,on=["School Name"])
#Merge in % Passed Reading
school_summary = school_summary.merge(passed_reading_school,on=["School Name"])
#Merge in Percent Passed Math
school_summary = school_summary.merge(passed_math_school,on=["School Name"])
#Add new column for % Overall Passed
school_summary["Overall Passing Rate"] = (school_summary["Percent Passed Reading"] + school_summary["Percent Passed Math"]) / 2
school_summary = school_summary.set_index(["School Name"])
school_summary
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>School Size</th>
      <th>School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Student Reading Score</th>
      <th>Average Student Math Score</th>
      <th>Percent Passed Reading</th>
      <th>Percent Passed Math</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Name</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>81.182722</td>
      <td>76.629414</td>
      <td>81.316421</td>
      <td>65.683922</td>
      <td>73.500171</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>81.158020</td>
      <td>76.711767</td>
      <td>80.739234</td>
      <td>65.988471</td>
      <td>73.363852</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1761</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>83.725724</td>
      <td>83.359455</td>
      <td>95.854628</td>
      <td>93.867121</td>
      <td>94.860875</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>80.934412</td>
      <td>77.289752</td>
      <td>80.862999</td>
      <td>66.752967</td>
      <td>73.807983</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>83.816757</td>
      <td>83.351499</td>
      <td>97.138965</td>
      <td>93.392371</td>
      <td>95.265668</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>83.989488</td>
      <td>83.274201</td>
      <td>96.539641</td>
      <td>93.867718</td>
      <td>95.203679</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>83.975780</td>
      <td>83.061895</td>
      <td>97.039828</td>
      <td>94.133477</td>
      <td>95.586652</td>
    </tr>
    <tr>
      <th>Bailey High School</th>
      <td>District</td>
      <td>4976</td>
      <td>3124928</td>
      <td>628.0</td>
      <td>81.033963</td>
      <td>77.048432</td>
      <td>81.933280</td>
      <td>66.680064</td>
      <td>74.306672</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>83.814988</td>
      <td>83.803279</td>
      <td>96.252927</td>
      <td>92.505855</td>
      <td>94.379391</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>84.044699</td>
      <td>83.839917</td>
      <td>95.945946</td>
      <td>94.594595</td>
      <td>95.270270</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1800</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>83.955000</td>
      <td>83.682222</td>
      <td>96.611111</td>
      <td>93.333333</td>
      <td>94.972222</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>80.744686</td>
      <td>76.842711</td>
      <td>80.220055</td>
      <td>66.366592</td>
      <td>73.293323</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>80.966394</td>
      <td>77.072464</td>
      <td>81.222432</td>
      <td>66.057551</td>
      <td>73.639992</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>80.746258</td>
      <td>77.102592</td>
      <td>79.299014</td>
      <td>68.309602</td>
      <td>73.804308</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>Charter</td>
      <td>1635</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>83.848930</td>
      <td>83.418349</td>
      <td>97.308869</td>
      <td>93.272171</td>
      <td>95.290520</td>
    </tr>
  </tbody>
</table>
</div>




```python
#***Top 5 Performing Schools 
#sort School Summary Table by descending "% Overall Passing Rate"
top_5 = school_summary.sort_values(["Overall Passing Rate"], ascending = False)
top_5.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>School Size</th>
      <th>School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Student Reading Score</th>
      <th>Average Student Math Score</th>
      <th>Percent Passed Reading</th>
      <th>Percent Passed Math</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Name</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>83.975780</td>
      <td>83.061895</td>
      <td>97.039828</td>
      <td>94.133477</td>
      <td>95.586652</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>Charter</td>
      <td>1635</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>83.848930</td>
      <td>83.418349</td>
      <td>97.308869</td>
      <td>93.272171</td>
      <td>95.290520</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>84.044699</td>
      <td>83.839917</td>
      <td>95.945946</td>
      <td>94.594595</td>
      <td>95.270270</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>83.816757</td>
      <td>83.351499</td>
      <td>97.138965</td>
      <td>93.392371</td>
      <td>95.265668</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>83.989488</td>
      <td>83.274201</td>
      <td>96.539641</td>
      <td>93.867718</td>
      <td>95.203679</td>
    </tr>
  </tbody>
</table>
</div>




```python
#***Bottom 5 Performing Schools
#sort School Summary Table by ascending "% Overall Passing Rate"
bottom_5 = school_summary.sort_values(["Overall Passing Rate"])
bottom_5.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>School Size</th>
      <th>School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Student Reading Score</th>
      <th>Average Student Math Score</th>
      <th>Percent Passed Reading</th>
      <th>Percent Passed Math</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Name</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>80.744686</td>
      <td>76.842711</td>
      <td>80.220055</td>
      <td>66.366592</td>
      <td>73.293323</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>81.158020</td>
      <td>76.711767</td>
      <td>80.739234</td>
      <td>65.988471</td>
      <td>73.363852</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>81.182722</td>
      <td>76.629414</td>
      <td>81.316421</td>
      <td>65.683922</td>
      <td>73.500171</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>80.966394</td>
      <td>77.072464</td>
      <td>81.222432</td>
      <td>66.057551</td>
      <td>73.639992</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>80.746258</td>
      <td>77.102592</td>
      <td>79.299014</td>
      <td>68.309602</td>
      <td>73.804308</td>
    </tr>
  </tbody>
</table>
</div>




```python
#***Create table that lists the average math score for students of each grade level
math_by_grade = merge_table_reset.drop(["School ID", "School Type", "School Size", "School Budget", 
                                  "Student ID", "Student Name", "Student Gender", "Student Reading Score"], axis=1)
math_by_grade = math_by_grade.rename(columns ={"Student Math Score": "Average Student Math Score"})
math_by_grade = math_by_grade.groupby(["School Name", "Student Grade"]).mean()
math_by_grade.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Average Student Math Score</th>
    </tr>
    <tr>
      <th>School Name</th>
      <th>Student Grade</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Bailey High School</th>
      <th>10th</th>
      <td>76.996772</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>77.515588</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>76.492218</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>77.083676</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <th>10th</th>
      <td>83.154506</td>
    </tr>
  </tbody>
</table>
</div>




```python
#***Create table that lists the average reading score for students of each grade level
reading_by_grade = merge_table_reset.drop(["School ID", "School Type", "School Size", "School Budget", 
                                  "Student ID", "Student Name", "Student Gender", "Student Math Score"], axis=1)
reading_by_grade = reading_by_grade.rename(columns ={"Student Reading Score": "Average Student Reading Score"})
reading_by_grade = reading_by_grade.groupby(["School Name", "Student Grade"]).mean()
reading_by_grade.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Average Student Reading Score</th>
    </tr>
    <tr>
      <th>School Name</th>
      <th>Student Grade</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Bailey High School</th>
      <th>10th</th>
      <td>80.907183</td>
    </tr>
    <tr>
      <th>11th</th>
      <td>80.945643</td>
    </tr>
    <tr>
      <th>12th</th>
      <td>80.912451</td>
    </tr>
    <tr>
      <th>9th</th>
      <td>81.303155</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <th>10th</th>
      <td>84.253219</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Find lowest per student budget
lowest_budget = school_summary.sort_values(["Per Student Budget"])
#Find highest per student budget
highest_budget = school_summary.sort_values(["Per Student Budget"], ascending = False)
```


```python
# Create the bins to sort budget data into groups
#Highest is $655 and lowest is $578

bins = [0, 600, 625, 650, 675]
# Create the names for the four bins
group_names = ["Less than $600", "$600 to $625", '$625 to $650', '$650 to $675']

# Cut school budget column and place the scores into bins
school_summary["Binned Budgets"] = pd.cut(school_summary["Per Student Budget"], bins, labels=group_names)
```


```python
#***Create a table that breaks down school performances based on average Spending Ranges (Per Student). 
binned_budgets = school_summary[["Binned Budgets", "Average Student Math Score", "Average Student Reading Score", "Percent Passed Math", "Percent Passed Reading", "Overall Passing Rate"]]
binned_budgets = binned_budgets.groupby(["Binned Budgets"])
binned_budgets.mean()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Student Math Score</th>
      <th>Average Student Reading Score</th>
      <th>Percent Passed Math</th>
      <th>Percent Passed Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Binned Budgets</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Less than $600</th>
      <td>83.436210</td>
      <td>83.892196</td>
      <td>93.541501</td>
      <td>96.459627</td>
      <td>95.000564</td>
    </tr>
    <tr>
      <th>$600 to $625</th>
      <td>83.595708</td>
      <td>83.930728</td>
      <td>93.993483</td>
      <td>96.542455</td>
      <td>95.267969</td>
    </tr>
    <tr>
      <th>$625 to $650</th>
      <td>78.032719</td>
      <td>81.416375</td>
      <td>71.112408</td>
      <td>83.453814</td>
      <td>77.283111</td>
    </tr>
    <tr>
      <th>$650 to $675</th>
      <td>76.959583</td>
      <td>81.058567</td>
      <td>66.218444</td>
      <td>81.089710</td>
      <td>73.654077</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Scores by School Size
#Find lowest school size
lowest_size = school_summary.sort_values(["School Size"])
#Find highest per student budget
highest_size = school_summary.sort_values(["School Size"], ascending = False)

# Create the bins to sort budget data into groups
#Highest is 4,976 and lowest is 427

size_bins = [0, 1000, 3000, 5000]
# Create the names for the four bins
size_group_names = ["Small", "Medium", "Large"]

# Cut school budget column and place the scores into bins
school_summary["Binned Sizes"] = pd.cut(school_summary["School Size"], size_bins, labels=size_group_names)
```


```python
#***Repeat the above breakdown, but this time group schools based on a reasonable approximation of school size (Small, Medium, Large).
binned_sizes = school_summary[["Binned Sizes", "Average Student Math Score", "Average Student Reading Score", "Percent Passed Math", "Percent Passed Reading", "Overall Passing Rate"]]
binned_sizes = binned_sizes.groupby(["Binned Sizes"])
binned_sizes.mean()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Student Math Score</th>
      <th>Average Student Reading Score</th>
      <th>Percent Passed Math</th>
      <th>Percent Passed Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Binned Sizes</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Small</th>
      <td>83.821598</td>
      <td>83.929843</td>
      <td>93.550225</td>
      <td>96.099437</td>
      <td>94.824831</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>81.176821</td>
      <td>82.933187</td>
      <td>84.649798</td>
      <td>91.316412</td>
      <td>87.983105</td>
    </tr>
    <tr>
      <th>Large</th>
      <td>77.063340</td>
      <td>80.919864</td>
      <td>66.464293</td>
      <td>81.059691</td>
      <td>73.761992</td>
    </tr>
  </tbody>
</table>
</div>




```python
#**Repeat the above breakdown, but this time group schools based on school type (Charter vs. District).
grouped_district = school_summary[["School Type", "Average Student Math Score", "Average Student Reading Score", "Percent Passed Math", "Percent Passed Reading", "Overall Passing Rate"]]
grouped_district = grouped_district.groupby(["School Type"])
grouped_district.mean()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Student Math Score</th>
      <th>Average Student Reading Score</th>
      <th>Percent Passed Math</th>
      <th>Percent Passed Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>93.620830</td>
      <td>96.586489</td>
      <td>95.103660</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>66.548453</td>
      <td>80.799062</td>
      <td>73.673757</td>
    </tr>
  </tbody>
</table>
</div>



Three observable trends in the data:
1. All five of the highest performing schools are charter while all 5 of the lowest performing schools are district.
3. The percentage of students who pass overall in charter schools is significantly higher than the percentage that passed math in district schools
2. Per student budget does not seem to have an affect on student scores. In conclusion, there must be a factor other than per student budget that makes charter school students more successful than district students.
