# Mock Data Generator
___
### Description
The purpose of this tool is to take in three CSV files and generate python objects and json files which can be used throughout the project.

The tool takes in three CSV files, (stored in the [input_csv_files](/mock_data_generator/input_csv_files) directory), and generates two json files, (stored in the output_json_files directory which will be created if it doesn't exist). 

Each input CSV file contains a first row of information (not used in the script) detailing the expected data types, a second row detailing the field names, and all remaining rows containing data.


### Usage 
###### Tested with Python 3.9
1. Fill in rows three and on with data as required in [course_data.csv](/mock_data_generator/input_csv_files/course_data.csv), [professor_data.csv](/mock_data_generator/input_csv_files/professor_data.csv), and [course_preferences.csv](/mock_data_generator/input_csv_files/course_preferences.csv).
2. Run [mock_data_generator.py](/mock_data_generator/mock_data_generator.py) with the following command to generate output json files:
  ```
  python mock_data_generator.py
  ```
3. Two json files will be created and saved in mock_data_generator/output_json_files/ which can be used as needed.
  - One file will be named professor_object.json and the other will be named professor_object.json.
  - Both json files adhere to the algorithm specification document corresponding to the two objects in SchedulerInput (a Professor[] list and a Schedule object).
