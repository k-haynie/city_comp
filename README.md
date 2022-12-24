This flask application is my CS50 final project submission. The program uses API keys I signed up for (for security reasons, not saved to this repository) to query data about places of residence across the United States. Listed information includes local and state populations, median income, and completed state-level COVID vaccinations.

In running the searches, the user can compare up to 5 locations at once, not needing to worry about case sensitivity or empty values.

I had fun creating this, and I hope you have fun running queries and discovering the numbers behind magnificent and miniscule locations. Enjoy!

All of the APIs the app uses are publicly available and/or only require registration to use, so I would recommend you sign up for them and then create a `.env` file using your keys from the linked sites:
>`fbi_api={`[FBI database key](https://crime-data-explorer.fr.cloud.gov/pages/home)`}`
>`covid_api={`[COVID Act Now database key](https://covidactnow.org/data-api)`}`
>`census_api={`[Census database key](https://www.census.gov/data/developers/data-sets/acs-5year.html))`}`