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

        next(csv_reader) # Row 1 Header
        next(csv_reader) # Row 2 Header

        line_count = 0
        for row in csv_reader:
            sections = []

            # Section 1
            sections.append({
                "professor": {
                    "id": int(row[8]) if row[8] != "" else None,
                    "name": row[9] if row[9] != "" else None
                } if row[8] != "" and row[9] != "" else None,
                "capacity": int(row[10]) if row[10] != "" else None,
                "timeSlots": parse_timeslots(row[11], row[12]) if row[11] != "" and row[12] != "" else []
            })

            # Section 2
            if int(row[7]) > 1:
                sections.append({
                    "professor": {
                        "id": int(row[13]) if row[13] != "" else None,
                        "name": row[14] if row[14] != "" else None
                    } if row[13] != "" and row[14] != "" else None,
                    "capacity": int(row[15]) if row[15] != "" else None,
                    "timeSlots": parse_timeslots(row[16], row[17]) if row[16] != "" and row[17] != "" else []
                })

            offering = {
                "course": {
                    "code": row[1],
                    "title": row[2],
                    "pengRequired": {
                        "fall": string_to_bool(row[3]) if row[3] != "" else False,
                        "spring": string_to_bool(row[4]) if row[4] != "" else False,
                        "summer": string_to_bool(row[5]) if row[5] != "" else False
                    },
                    "yearRequired": int(row[6])
                },
                "sections": sections
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
    fall = times[0] != "" and times[1] != "" and times[2] != "" and times[3] != "" and times[4] != ""
    spring = times[5] != "" and times[6] != "" and times[7] != "" and times[8] != "" and times[9] != ""
    summer = times[10] != "" and times[11] != "" and times[12] != "" and times[13] != "" and times[14] != ""
    preferredTimes = {
        "fall": {
            "monday": parse_time_ranges(times[0]) if times[0] != "" else [],
            "tuesday": parse_time_ranges(times[1]) if times[1] != "" else [],
            "wednesday": parse_time_ranges(times[2]) if times[2] != "" else [],
            "thursday": parse_time_ranges(times[3]) if times[3] != "" else [],
            "friday": parse_time_ranges(times[4]) if times[4] != "" else []
        } if fall else None,
        "spring": {
            "monday": parse_time_ranges(times[5]) if times[5] != "" else [],
            "tuesday": parse_time_ranges(times[6]) if times[6] != "" else [],
            "wednesday": parse_time_ranges(times[7]) if times[7] != "" else [],
            "thursday": parse_time_ranges(times[8]) if times[8] != "" else [],
            "friday": parse_time_ranges(times[9]) if times[9] != "" else []
        } if spring else None,
        "summer": {
            "monday": parse_time_ranges(times[10]) if times[10] != "" else [],
            "tuesday": parse_time_ranges(times[11]) if times[11] != "" else [],
            "wednesday": parse_time_ranges(times[12]) if times[12] != "" else [],
            "thursday": parse_time_ranges(times[13]) if times[13] != "" else [],
            "friday": parse_time_ranges(times[14]) if times[14] != "" else []
        } if summer else None
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
                    preferences[course_names[i - 2]] = int(row[i])
                coursePreferences[row[0]] = preferences
            line_count += 1
        return coursePreferences if len(coursePreferences) > 0 else None

def parse_course_prefs_into_list(course_prefs):
    prefs_list = []
    for k, v in course_prefs.items():
        prefs_list.append({"courseCode": k, "enthusiasmScore": v})
    
    return prefs_list

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
                    "id": int(row[0]),
                    "name": row[1],
                    "isPeng": string_to_bool(row[2]),
                    "facultyType": row[3].upper(),
                    "teachingObligations": int(row[4]),
                    "coursePreferences": parse_course_prefs_into_list(coursePreferences[row[0]]),
                    "preferredTimes": parse_preferred_times(row[5:20]),
                    "preferredCoursesPerSemester": {
                        "fall": int(row[20]) if row[20] != "" else None,
                        "spring": int(row[21]) if row[21] != "" else None,
                        "summer": int(row[22]) if row[22] != "" else None
                    },
                    "preferredNonTeachingSemester": row[23].upper() if row[23] != "" else None,
                    "preferredCourseDaySpreads": row[24].split('&') if row[24] != "" else []
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
