import csv
import pprint
import json


# A function to print a python object with a readable structure.
def pretty_print(object):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(object)
    print()


# A helper function to convert an input CSV string to a boolean.
def string_to_bool(string):
    return string.lower() in ("true", "1", "yes", "t")


# Converts the input course data CSV to a python object matching the algorithm spec.
def process_course_data(csv_name):
    schedule_object = {
        "fall": [],
        "spring": [],
        "summer": []
    }
    with open(csv_name) as course_data_csv:
        csv_reader = csv.reader(course_data_csv, delimiter=',')
        next(csv_reader)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                offering = {
                    "course": {
                        "code": row[1],
                        "title": row[2],
                        "pengRequired": {
                            "fall": string_to_bool(row[3]),
                            "spring": string_to_bool(row[4]),
                            "summer": string_to_bool(row[5])
                        },
                        "yearRequired": int(row[6])
                    },
                    "sections": [
                        {
                            "professor": {},
                            "capacity": int(row[7]) if row[7] != "" else None,
                            "timeslots": []
                        }
                    ]
                }
                schedule_object[row[0]].append(offering)
            line_count += 1

        return schedule_object


# A helper function used to parse the time ranges.
def parse_time_ranges(time_ranges):
    if time_ranges == "":
        return []
    time_range_list = time_ranges.split('&')
    for index, time_range in enumerate(time_range_list):
        split_range = time_range.split('~')
        time_range_list[index] = (split_range[0], split_range[1])
    return time_range_list


# A helper function used to process preferred times.
def parse_preferred_times(times):
    preferredTimes = {
        "fall": {
            "monday": parse_time_ranges(times[0]),
            "tuesday": parse_time_ranges(times[1]),
            "wednesday": parse_time_ranges(times[2]),
            "thursday": parse_time_ranges(times[3]),
            "friday": parse_time_ranges(times[4])
        },
        "spring": {
            "monday": parse_time_ranges(times[5]),
            "tuesday": parse_time_ranges(times[6]),
            "wednesday": parse_time_ranges(times[7]),
            "thursday": parse_time_ranges(times[8]),
            "friday": parse_time_ranges(times[9])
        },
        "summer": {
            "monday": parse_time_ranges(times[10]),
            "tuesday": parse_time_ranges(times[11]),
            "wednesday": parse_time_ranges(times[12]),
            "thursday": parse_time_ranges(times[13]),
            "friday": parse_time_ranges(times[14])
        }
    }
    return preferredTimes


# Converts the input professor preferences CSV to a python object matching the algorithm spec.
def parse_course_preferences(preferences_csv_name):
    coursePreferences = {}
    with open(preferences_csv_name) as preferences_data_csv:
        preferences_csv_reader = csv.reader(preferences_data_csv, delimiter=',')
        course_names = []
        line_count = 0
        for row in preferences_csv_reader:
            if line_count == 0:
                course_names = row[2:len(row)]
            else:
                preferences = {}
                for i in range(2, len(row)):
                    preferences[course_names[i - 2]] = row[i]
                coursePreferences[row[0]] = preferences
            line_count += 1
        return coursePreferences


# Converts the input professor data CSV to a python object matching the algorithm spec.
def process_professor_data(csv_name, preferences_csv_name):
    coursePreferences = parse_course_preferences(preferences_csv_name)

    professors_object = []
    with open(csv_name) as professor_data_csv:
        csv_reader = csv.reader(professor_data_csv, delimiter=',')
        next(csv_reader)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                professor = {
                    "id": row[0],
                    "name": row[1],
                    "isPeng": string_to_bool(row[2]),
                    "facultyType": row[3],
                    "teachingObligations": int(row[4]),
                    "coursePreferences": coursePreferences[row[0]],
                    "preferredTimes": parse_preferred_times(row[5:20]),
                    "preferredCoursesPerSemester": {
                        "fall": int(row[20]),
                        "spring": int(row[21]),
                        "summer": int(row[22])
                    },
                    "preferredNonTeachingSemester": row[23],
                    "preferredCourseDaySpreads": row[24].split('&')
                }
                professors_object.append(professor)
            line_count += 1
        return professors_object


# A function used to generate a json file from a python object.
def obj_to_json_file(object, output_name):
    json_filename = 'output_json_files/' + output_name + '.json'
    with open(json_filename, 'w') as outfile:
        outfile.write(json.dumps(object))


if __name__ == '__main__':
    # Convert the course data CSV to a python object.
    schedule_object = process_course_data('input_csv_files/course_data.csv')
    # Create a json file from the object.
    obj_to_json_file(schedule_object, "schedule_object")
    # Print the object with a nicer format.
    pretty_print(schedule_object)

    # Convert the professor data CSV and professor preferences CSV to a single python object.
    professor_object = process_professor_data('input_csv_files/professor_data.csv', 'input_csv_files'
                                                                                    '/course_preferences.csv')
    # Create a json file from the object.
    obj_to_json_file(professor_object, "professor_object")
    # Print the object with a nicer format.
    pretty_print(professor_object)