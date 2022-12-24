This flask application was my CS50 final project submission in Summer of 2021. The program uses API keys to query data about places of residence across the United States, handling up to 5 locations at a time. Queried information includes local and state populations, median income, and completed state-level COVID vaccinations. I used Flask to handle Python scripting for the logic side of the application in tandem with a small dose of Jinja for general templating. 

All of the APIs the app uses are publicly available and/or only require registration to use, so I would recommend you sign up for them and then create a `.env` file using your keys from the linked sites in order to run this program yourself:  
fbi_api={[FBI database key](https://crime-data-explorer.fr.cloud.gov/pages/home)}  
covid_api={[COVID Act Now database key](https://covidactnow.org/data-api)}  
census_api={[Census database key](https://www.census.gov/data/developers/data-sets/acs-5year.html))}
