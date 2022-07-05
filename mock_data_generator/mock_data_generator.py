import csv
import pprint
import json
import os


# A function to print a python object with a readable structure.
def pretty_print(object):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(object)
    print()


# A helper function to convert an input CSV string to a boolean.
def string_to_bool(string):
    return string.lower() in ("true", "1", "yes", "t")


# Converts the input course data CSV to a python object matching the algorithm spec.
def process_course_data(course_csv_name):
    schedule_object = {
        "fall": [],
        "spring": [],
        "summer": []
    }
    with open(course_csv_name) as course_data_csv:
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
                            "fall": string_to_bool(row[3]) if row[3] != "" else None,
                            "spring": string_to_bool(row[4]) if row[4] != "" else None,
                            "summer": string_to_bool(row[5]) if row[5] != "" else None
                        },
                        "yearRequired": int(row[6])
                    },
                    "sections": [
                        {
                            "professor": {
                                "id": int(row[7]) if row[7] != "" else None,
                                "name": row[8] if row[8] != "" else None
                            },
                            "capacity": int(row[9]) if row[9] != "" else None,
                            "timeslots": parse_timeslots(row[10], row[11]) if row[10] != "" and row[11] != "" else []
                        }
                    ]
                }
                schedule_object[row[0]].append(offering)
            line_count += 1
    return schedule_object


def parse_timeslots(days, timeRange):
    daySpreads = {
        "TWF": ["TUESDAY", "WEDNESDAY", "FRIDAY"],
        "MTh": ["MONDAY", "THURSDAY"],
        "M": ["MONDAY"],
        "T": ["TUESDAY"],
        "W": ["WEDNESDAY"],
        "Th": ["THURSDAY"],
        "F": ["FRIDAY"]
    }

    return [{"dayOfWeek": day, "timeRange": parse_time_ranges(timeRange)[0]} for day in daySpreads[days]]


# A helper function used to parse the time ranges.
def parse_time_ranges(time_ranges):
    if time_ranges == "":
        return [None]
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
        return coursePreferences if len(coursePreferences) > 0 else None


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
                        "fall": int(row[20]) if row[20] != "" else None,
                        "spring": int(row[21]) if row[21] != "" else None,
                        "summer": int(row[22]) if row[22] != "" else None
                    },
                    "preferredNonTeachingSemester": row[23] if row[23] != "" else None,
                    "preferredCourseDaySpreads": row[24].split('&') if row[24] != "" else None
                }
                professors_object.append(professor)
            line_count += 1
        return professors_object


# A function used to generate a json file from a python object.
def obj_to_json_file(object, output_name):
    if not (os.path.exists("./output_json_files")):
        os.mkdir("./output_json_files")
    json_filename = 'output_json_files/' + output_name + '.json'
    with open(json_filename, 'w') as outfile:
        json.dump(object, outfile, indent=6)


if __name__ == '__main__':
    # Convert the course data CSV to a python object.
    schedule_object = process_course_data('input_csv_files/schedule.csv')
    # Create a json file from the object.
    obj_to_json_file(schedule_object, "schedule_object")
    # Print the object with a nicer format.
    pretty_print(schedule_object)

    # Convert the professor data CSV and professor preferences CSV to a single python object.
    professor_object = process_professor_data('input_csv_files/professors.csv', 'input_csv_files'
                                                                                '/professor_course_preferences.csv')
    # Create a json file from the object.
    obj_to_json_file(professor_object, "professor_object")
    # Print the object with a nicer format.
    pretty_print(professor_object)
