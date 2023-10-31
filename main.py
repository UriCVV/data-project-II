import src.encapsulation as extraction
import src.visualization as viz
import getpass

if __name__ == "__main__":
    # Prompt the user to choose a year for analysis and enter an API key for currency conversion
    year_1 = input("Choose the year to be analyzed (2008, 2010, 2012, 2014, 2016, 2018): ")
    year_2 = input("Choose another (2008, 2010, 2012, 2014, 2016, 2018): ")
    api_key = getpass.getpass("Enter your currencyapi token: ")

    # Call the extraction function to process data
    data_path_1 = extraction.main(year_1, api_key)
    data_path_2 = extraction.main(year_2, api_key)

    # Call the visualization function to visualize the data
    viz.visualize_smoking_data(data_path_1, data_path_2, year_1, year_2)
