# school_data.py
# LONG NGUYEN
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.


import numpy as np
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, \
    year_2021, year_2022

# Declare any global variables needed to store the data here

# Create a list of all arrays from the 'given_data' file
all_years = [year_2013, year_2014, year_2015, year_2016, year_2017,
             year_2018, year_2019, year_2020, year_2021, year_2022]

# Concatenate the data of all years into one single array
combined_data = np.concatenate(all_years)

# Reshape the data into a 3D array with the dimension that we want: (10 years, 20 schools, 3 grades)
reshaped_data = combined_data.reshape(10, 20, 3)

# My personal check: Print the array after reshaping to make sure the combined array is good as expected
# print(reshaped_data)

# Create a list of school names from the CSV dataset
school_names = ["Centennial High School", "Robert Thirsk School", "Louise Dean School",
                "Queen Elizabeth High School", "Forest Lawn High School", "Crescent Heights High School",
                "Western Canada High School", "Central Memorial High School", "James Fowler High School",
                "Ernest Manning High School", "William Aberhart High School", "National Sport School",
                "Henry Wise Wood High School", "Bowness High School", "Lord Beaverbrook High School",
                "Jack James High School", "Sir Winston Churchill High School", "Dr. E. P. Scarlett High School",
                "John G Diefenbaker High School", "Lester B. Pearson High School"]

# Create a list of school codes from the CSV dataset
school_codes = [1224, 1679, 9626, 9806, 9813, 9815, 9816, 9823, 9825, 9826,
                9829, 9830, 9836, 9847, 9850, 9856, 9857, 9858, 9860, 9865]

# Dictionary to map school codes to school names
school_dict = {code: name for code, name in zip(school_codes, school_names)}


# You may add your own additional classes, functions, variables, etc.
def get_school_index(school_input):
    """
    Get the index of the school based on the school names or codes.

    Parameters:
    school_input (str): The school name or code provided by the user.

    Returns:
    int: The index of the school in the list of schools.

    Raises:
    ValueError: If the school name or code is not valid.
    """
    if school_input.isdigit():
        school_code = int(school_input)
        if school_code in school_dict:
            return school_codes.index(school_code)
        else:
            raise ValueError("You must enter a valid school name or code.")
    else:
        if school_input in school_names:
            return school_names.index(school_input)
        else:
            raise ValueError("You must enter a valid school name or code.")


def get_school_stats(school_index):
    """
    Calculate and print the statistics of a speccific school.

    Parameters:
    school_index (int): The index of the school in the list of schools.

    Returns:
    None
    """
    school_name = school_names[school_index]
    school_code = school_codes[school_index]
    school_data = reshaped_data[:, school_index, :]  # Subarray view: extract the specific school in the 3D array

    # Use NaN-safe aggregation functions to ignore missing values to avoid runtime errors
    mean_enrollment_grade10 = np.floor(np.nanmean(school_data[:, 0])).astype(int)
    mean_enrollment_grade11 = np.floor(np.nanmean(school_data[:, 1])).astype(int)
    mean_enrollment_grade12 = np.floor(np.nanmean(school_data[:, 2])).astype(int)
    highest_enrollment = np.nanmax(school_data).astype(int)
    lowest_enrollment = np.nanmin(school_data).astype(int)
    total_enrollment_each_year = np.nansum(school_data, axis=1).astype(int)
    total_ten_year_enrollment = np.nansum(total_enrollment_each_year).astype(int)
    mean_total_yearly_enrollment = np.floor(np.nanmean(total_enrollment_each_year)).astype(int)

    # Check if any enrollment numbers were over 500
    over_500_enrollment = school_data[school_data > 500]  # Masking operation
    if over_500_enrollment.size == 0:
        error_message = "No enrollments over 500."
    else:
        over_500_median = np.nanmedian(over_500_enrollment).astype(int)

    print(f"School Name: {school_name}, School Code: {school_code}")
    print(f"Mean enrollment for Grade 10: {mean_enrollment_grade10}")
    print(f"Mean enrollment for Grade 11: {mean_enrollment_grade11}")
    print(f"Mean enrollment for Grade 12: {mean_enrollment_grade12}")
    print(f"Highest enrollment for a single grade: {highest_enrollment}")
    print(f"Lowest enrollment for a single grade: {lowest_enrollment}")
    for year, enrollment in zip(range(2013, 2023), total_enrollment_each_year):
        print(f"Total enrollment for {year}: {enrollment}")
    print(f"Total ten year enrollment: {total_ten_year_enrollment}")
    print(f"Mean total enrollment over 10 years: {mean_total_yearly_enrollment}")
    if over_500_enrollment.size == 0:
        print(error_message)
    else:
        print(f"For all enrollments over 500, the median value was: {over_500_median}")


def get_general_stats():
    """
    Calculate and print general statistics for all schools.

    Parameters:
    None

    Returns:
    None
    """
    mean_enrollment_2013 = np.floor(np.nanmean(reshaped_data[0])).astype(int)  # index 0 pointing to the first array
    mean_enrollment_2022 = np.floor(np.nanmean(reshaped_data[-1])).astype(int)  # index -1 pointing to the last array
    total_graduates_2022 = np.nansum(reshaped_data[-1, :, 2]).astype(int)  # graduating class == Grade 12
    highest_enrollment_all_schools = np.nanmax(reshaped_data).astype(int)
    lowest_enrollment_all_schools = np.nanmin(reshaped_data).astype(int)

    print(f"Mean enrollment in 2013: {mean_enrollment_2013}")
    print(f"Mean enrollment in 2022: {mean_enrollment_2022}")
    print(f"Total graduating class of 2022: {total_graduates_2022}")
    print(f"Highest enrollment for a single grade: {highest_enrollment_all_schools}")
    print(f"Lowest enrollment for a single grade: {lowest_enrollment_all_schools}")


def main():
    print("ENSF 692 School Enrollment Statistics")

    # Print Stage 1 requirements here
    print("Shape of full data array: ", reshaped_data.shape)
    print("Dimensions of full data array: ", reshaped_data.ndim)

    # Prompt for user input
    school_input = input("Please enter the high school name or school code: ")

    # Print Stage 2 requirements here
    print("\n***Requested School Statistics***\n")

    # Exception handling: If there is no ValueError, then it will call the functions defined above.
    try:
        school_index = get_school_index(school_input)
        get_school_stats(school_index)
    except ValueError as e:
        print(e)

    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")
    # Call the function defined above to get all schools' general statistics.
    get_general_stats()


if __name__ == '__main__':
    main()
