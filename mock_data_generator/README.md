# Mock Data Generator
*Any data stored in the CSV files does not represent real world data.*
___
### Description
The purpose of this tool is to take in three CSV files and generate python objects and json files which can be used throughout the project.

The tool takes in three CSV files, (stored in the [input_csv_files](/mock_data_generator/input_csv_files) directory), and generates two json files (stored in the output_json_files directory, which will be created if it doesn't already exist). 

In each input CSV file, the first row is used for information (not used in the script) describing the expected data types and sometimes a note, the second row is used for the field names, and all remaining rows contain data. Most columns map 1:1 to a field in an object in the spec, but for those that do not, they are described in the notes below and should hopefully be straightforward. If anything doesn't make sense, please feel free to ask the algorithm 1 team.


### Usage 
###### Tested with Python 3.9
1. Clone the repo
2. Edit the three CSV input files ([schedule.csv](/mock_data_generator/input_csv_files/schedule.csv), [professors.csv](/mock_data_generator/input_csv_files/professors.csv), [professor_course_preferences.csv](/mock_data_generator/input_csv_files/professor_course_preferences.csv)) as necessary
   * _schedule.csv_ contains all required courses for a SENG degree, except for technical electives, complementary studies electives, and natural science electives
       * This dataset is representative of a real dataset, but some values are randomized and thus this dataset should not be assumed to reflect historical calendar data
       * pengRequired.[semester] is left blank if the course is not offered that semester
       * professor.id and professor.name are only filled out for static courses (representative of actual input), but the data is fake
       * days and timeRange are parsed to create TimeSlot objects (in the spec)
       * days and timeRange are not filled out for _any_ courses, but they should be filled out for static courses in an actual input
   * _professors.csv_ contains all the professors we can assign to courses according to the data given to us by the teaching team
       * The dataset is representative of a real dataset, but the values are randomized and should not be assumed to be "real"
       * Preferred times (multi-column), preferred courses per semester (multi-column), preferredNonTeachingSemester, and preferredCourseDaySpreads are not filled out but should be in an actual input
   * _professor_course_preferences_ contains the mock data provided to us by the teaching team
       * The ids and names must correspond to rows in _professors.csv_
3. Run [mock_data_generator.py](/mock_data_generator/mock_data_generator.py) with the following command to generate output json files:
  ```
  python mock_data_generator.py
  ```
4. Two json files will be created and saved in mock_data_generator/output_json_files/ which can be used as needed
   * _schedule_object.json_ and _professor_object.json_
   * Both json files adhere to the [algorithm specification document](https://docs.google.com/document/d/163L7pv6w5Z38rUrl2EwRJq-A9ZLllCIO9uYbUkdxi2s/edit#), corresponding to the two objects in SchedulerInput: _professors_ and _schedule_
