import pandas as pd
import requests
import getpass
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(year, api_key):
    def read():
        # Read data from a CSV file for the selected year
        df = pd.read_csv(f"data/SmokingAndTobaccoData{year}.csv")
        
        # List of columns to drop if they exist in the DataFrame
        columns_to_drop = ["CheapestBrandCigaretteCurrency", "BanOnEducationalFacilites", "PremiumBrandCigarettePrice", "BanOnGovernmentFacilites", "BanOnHealthcareFacilites", "BanOnIndoorOffices", "BanOnPublicTransport", "BanOnPubsAndBars", "BanOnRestaurants", "BanOnUniversities", "RegulationsOnSmokeFreeEnvironments"]

        # Check if the columns to drop exist in the DataFrame
        columns_to_drop = [col for col in columns_to_drop if col in df.columns]

        if columns_to_drop:
            # Remove unnecessary columns from the DataFrame
            df = df.drop(columns=columns_to_drop)
        
        # Rename the 'Location' column to 'Country'
        df = df.rename(columns={'Location': 'Country'})
        df = df.rename(columns={'HealyWarningsOnSmoking': 'HealthWarningsOnSmoking'})
        
        # Convert cdolumns to numeric values, handle errors by converting to NaN or 0
        df["MostSoldBrandCigarettePrice"] = pd.to_numeric(df["MostSoldBrandCigarettePrice"], errors='coerce')

        # Clean percentage columns
        df['CigaretteSmokingPrevalence'] = df['CigaretteSmokingPrevalence'].str.extract(r'(\d+\.\d+)')
        df['TobaccoSmokingPrevalence'] = df['TobaccoSmokingPrevalence'].str.extract(r'(\d+\.\d+)')
        df['TobaccoUsePrevalance'] = df['TobaccoUsePrevalance'].str.extract(r'(\d+\.\d+)')
        
        return df


    df = read()


    # Define a function to perform currency conversion
    def currency_conversion(currency, amount):
        # Construct the URL for the currency conversion API request
        base_url = f"https://api.currencyapi.com/v3/convert?apikey={api_key}"
        endpoint = f"&date={year}-06-01&base_currency={currency}&currencies=USD&value={amount}"
        url_for_request = base_url + endpoint
        
        # Send a request to the currency conversion API
        res = requests.get(url_for_request)
        
        try:
            # Extract and round the converted amount from the API response
            result = round(res.json()["data"]["USD"]["value"], 2)
            return result
        except:
            # Handle errors by printing an error message and returning NaN
            print(f"couldn't convert from {currency}, {url_for_request}")
            return np.nan


    # Apply the currency_conversion function to each row in the DataFrame to calculate prices in USD
    df["MostSoldBrandCigarettePriceInUSD"] = df.apply(lambda x: currency_conversion(x["MostSoldBrandCigaretteCurrency"], x["MostSoldBrandCigarettePrice"]), axis=1)


    def access_browser_via_selenium(url):
        # Set up the WebDriver (for Chrome)
        driver = webdriver.Chrome(executable_path='src/chromedriver.exe')

        # Navigate to the webpage
        driver.get(url)

        # Wait for the dynamic content to load (using an explicit wait with a 30-second timeout)
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody')))

        # Extract the table data
        table_data = driver.find_element(By.CSS_SELECTOR, 'tbody').text

        # Close the browser
        driver.quit()

        return table_data


    def get_deaths():
        # Construct the URL with the selected 'year' variable to access data for that year
        table_data = access_browser_via_selenium(f"https://ourworldindata.org/grapher/number-of-deaths-by-risk-factor?tab=table&time={year}")

        # Split the data into lines
        lines = table_data.split('\n')

        # Create a list of dictionaries to store the data
        data_list = []

        for line in lines:
            values = line.split()
            if len(values) >= 17:  # Check if there are at least 17 values in the list
                country_parts = []
                numbers = []
                for value in values:
                    if value.isalpha():
                        country_parts.append(value)
                    else:
                        numbers.append(value)
                country = ' '.join(country_parts)  # Join the word parts to form the country name
                deaths_by_smoking = numbers[13]  # Assuming you want the 13th value (0-based index) from the numbers
                data_list.append({'Country': country, 'DeathsBySmoking': deaths_by_smoking})

        # Create a DataFrame from the list of dictionaries
        sub_df_deaths = pd.DataFrame(data_list)

        return sub_df_deaths


    def get_gdp():
        # Construct the URL with the selected 'year' variable to access data for that year
        table_data = access_browser_via_selenium(f"https://ourworldindata.org/grapher/gdp-per-capita-maddison?tab=table&time={year}")


        # Split the data into lines
        lines = table_data.split('\n')

        # Initialize lists for countries and GDP values
        countries = []
        gdp_values = []

        # Regular expression pattern to match GDP values with dollar signs and commas
        gdp_pattern = r'\$([\d,]+)'

        # Iterate through the lines and extract country names and GDP values. Last 21 values not valuable data because they refer to continents and general GDP
        for i in range(0, len(lines) -21, 2):
            country = lines[i]
            gdp_match = re.search(gdp_pattern, lines[i + 1])
            
            if gdp_match:
                gdp = int(gdp_match.group(1).replace(',', ''))
            else:
                gdp = None
            
            countries.append(country)
            gdp_values.append(gdp)

        # Create a DataFrame
        sub_df_gdp = pd.DataFrame({'Country': countries, 'GDPinUSD': gdp_values})
        
        return sub_df_gdp


    def get_population():
        # Construct the URL with the selected 'year' variable to access data for that year
        table_data = access_browser_via_selenium(f"https://www.populationpyramid.net/population-size-per-country/{year}/")

        # Define a regular expression pattern to capture the rank, country name, and population
        pattern = re.compile(r'(\d+)\n(.+?)\s([0-9,]+)')

        matches = re.findall(pattern, table_data)

        data_list = []

        for match in matches:
            rank = match[0]
            country = match[1]
            population = match[2].replace(',', '')  # Remove commas from the population number
            data_list.append({'Rank': rank, 'Country': country, 'Population': population})

        # Create a DataFrame from the list of dictionaries
        sub_df_population = pd.DataFrame(data_list)

        #drop rank column
        sub_df_population.drop(columns=['Rank'], inplace=True)

        return sub_df_population


    def merge_clean_export(df):
        # Retrieve death, gdp, and population data for the selected year
        sub_df_deaths = get_deaths()
        sub_df_gdp = get_gdp()
        sub_df_population = get_population()

        # Merge new information
        df = df.merge(sub_df_deaths, on='Country', how='left')
        df = df.merge(sub_df_gdp, on='Country', how='left')
        df = df.merge(sub_df_population, on='Country', how='left')

        # Columns not useful anymore
        df.drop(columns=['MostSoldBrandCigaretteCurrency', 'MostSoldBrandCigarettePrice'], inplace=True)

        # Change column order
        df = df[["Country",	"CigaretteSmokingPrevalence",	"TobaccoSmokingPrevalence",	"TobaccoUsePrevalance", "DeathsBySmoking",	"HealthWarningsOnSmoking",	"TreatmentInHealthFacilities",	"MostSoldBrandCigarettePriceInUSD",	"GDPinUSD",	"Population"]]

        df['DeathsBySmoking'] = df['DeathsBySmoking'].str.replace(',', '').astype(float)

        df.to_csv(f"data/SmokingAndTobaccoData{year}-enhanced.csv", index=False)

        # Return data path so visualization can start


    merge_clean_export(df)

    return f"data/SmokingAndTobaccoData{year}-enhanced.csv"
