# calgary_dogs.py
# LONG NGUYEN
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd


def main():
    # Stage 1: DataFrame creation
    # Import data here
    df = pd.read_excel("CalgaryDogBreeds.xlsx")

    # # Check the first 5 rows of DF
    # print(df.head())

    # # My personal check: a quick EDA of the dataset
    # print(df.info())              # Check the info of the dataframe
    # print(df['Year'].unique())    # Check the unique values in the column Year
    # print(df['Month'].unique())   # Check the unique values in the column Month
    # print(df['Breed'].unique())   # Check the unique values in the column Breed
    # print(df['Breed'].nunique())  # Check the number of unique values in the column Breed
    # print(df.isnull().sum())      # Check the total number of unique values in all columns

    # Set and sort the multi-index for the DF
    # I chose the column 'Breed' as the primary index since it's easier for data access and analysis in the next step.
    df.set_index(['Breed', 'Year', 'Month'], inplace=True)
    df.sort_index(inplace=True)

    # # Check the DataFrame after setting the multi-index if needed
    # print(df.head())

    print("\nENSF 692 Dogs of Calgary")

    # Stage 2: User input stage
    user_input = get_user_input(df)

    # Stage 3: Data analysis stage
    calculate_breed_stats(df, user_input)


def get_user_input(df):
    """

    :param df:
    :return:
    """
    while True:
        try:
            # Take the user input and convert it to uppercase
            user_input = input("Please enter a dog breed: ").upper()
            # Check if the breed exists in the index
            if user_input in df.index.get_level_values('Breed'):
                return user_input
            else:
                # If the dog breed is not found, raise a KeyError exception
                raise KeyError
        except KeyError as e:
            print("Dog breed not found in the data. Please try again.")


def calculate_breed_stats(df, breed):
    """

    :param df:
    :param breed:
    """
    # Extract the specific breed name
    breed_data = df.loc[pd.IndexSlice[breed, :, :]]

    # Find all the years from the 'year' index of the breed input
    breed_years = ", ".join(map(str, breed_data.index.get_level_values('Year').unique()))
    # Find and print all years if he selected breed was found
    print(f"The {breed} was found in the top breeds for years: {breed_years}. ")

    # Calculate and print the total number of registrations of the selected breed found
    total_breed_found = breed_data['Total'].sum()
    print(f"There have been {total_breed_found} {breed} dogs registered total.")

    # Calculate and print the percentage of selected breed registrations for each year
    # Create a list of the years from the original DF in the Excel file
    years = [2021, 2022, 2023]
    # Iterate over the list of years to calculate the total/percentage of the selected breed
    for year in years:
        try:
            total_dogs_per_year = df.loc[pd.IndexSlice[:, year, :], 'Total'].sum()
            selected_breed_per_year = breed_data.loc[pd.IndexSlice[:, year, :], 'Total'].sum()
            percentage_breed_per_year = (selected_breed_per_year / total_dogs_per_year) * 100
            print(f"The {breed} was {percentage_breed_per_year:.5f}% of top breeds in {year}.")
        except KeyError as e:
            print(f"Error accessing data for the year {year}: {e}")


if __name__ == '__main__':
    main()
