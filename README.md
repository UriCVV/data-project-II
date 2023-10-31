# Project: Smoking and Tobacco Data Analysis

This project aims to analyze smoking and tobacco-related data from two different years. The analysis includes examining the prevalence of cigarette smoking, its correlation with various factors, and comparing the impact of health warnings and treatment in health facilities on deaths caused by smoking.

## Dataset / Data Source

The datasets used in this project was obtained from kaggle:

- [WHO Tobacco and Smoking Data 2008-2018](https://www.kaggle.com/datasets/ozgurdogan646/who-tobacco-and-smoking-data-20082018)

These datasets provide information on various aspects of smoking, including cigarette smoking prevalence, tobacco use, GDP, population, and more for different countries.

Currency Api

- [currencyapi.com](https://app.currencyapi.com/)

Some other data was extracted from web scraping in:

- [populationpyramid.net](https://www.populationpyramid.net/population-size-per-country/2018/)
- [Our World in Data (number of deaths by risk, data from: IHME, Global Burden of Disease (2019))](https://ourworldindata.org/grapher/number-of-deaths-by-risk-factor?tab=table&time=2018)
- [Our World in Data (GDP per country, data from: Maddison Project Database 2020)](https://ourworldindata.org/grapher/number-of-deaths-by-risk-factor?tab=table&time=2018)

## Workflow / Methodology

The project workflow and methodology include several key steps:

1. **Data Extraction and Preprocessing**: Data is loaded from CSV files and preprocessed to handle missing values and format columns properly. Some columns are dropped for simplicity.

2. **Currency Conversion**: Currency conversion is performed to calculate cigarette prices in USD using an API (CurrencyAPI). The API key is entered by the user.

3. **Web Scraping with Selenium**: Data on deaths caused by smoking, GDP, and population is obtained by scraping web pages. Selenium is used to navigate and extract data.

4. **Merging and Data Enhancement**: The scraped data is merged with the original dataset to enrich it. The dataset is further cleaned, and the order of columns is adjusted.

5. **Export Enhanced Data**: The enhanced dataset is exported to a new CSV file for analysis.

## Goals / Hypothesis

The main goals of this project are to:

- Compare cigarette smoking prevalence in 2008 and 2018.
- Analyze the correlation between smoking prevalence and various factors.
- Investigate the impact of health warnings and treatment in health facilities on deaths caused by smoking.
- Examine the relationship between cigarette prices and smoking prevalence.

## Analysis

The analysis reveals insights into the changes in cigarette smoking prevalence over the years, correlations between smoking prevalence and GDP, as well as the impact of health warnings and treatment in health facilities on deaths by smoking. We also explore the relationship between cigarette prices and smoking prevalence.

## Results

The results of the analysis are presented in several visualizations, including bar charts, scatter plots, a correlation heatmap, and a geospatial map, to provide a comprehensive view of the smoking and tobacco-related data.

## Conclusion

In conclusion, this project provides valuable insights into smoking and tobacco-related data, shedding light on trends, correlations, and the impact of various factors. The analysis can be useful for policymakers, health organizations, and researchers interested in understanding and addressing smoking-related issues.

## Links

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Plotly Express Documentation](https://plotly.com/python/plotly-express/)
- [CurrencyAPI](https://currencyapi.com/)
- [selenium](https://www.selenium.dev/documentation/)