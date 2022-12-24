import requests
import urllib.parse

class queryState():
    def __init__(self, city, state, states, fips, fbi_api, covid_api, census_api):
        self.city = city
        self.state = state
        self.abbr = "{:0>2}".format(int(fips[(states.index(state))]))
        self.gov_api = fbi_api
        self.cov_api = covid_api
        self.census_api = census_api
        self.state_pop = self.get_pop()
        self.place = 0

    def get_pop(self):
        url = f"https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:{self.abbr}&key={self.census_api}"
        response = requests.get(url)
        response = response.json()
        return int(response[1][1])


    def get_answer(self):
        answer = {}
        answer["Population"] = self.query_state()
        answer["State Population"] = self.state_pop
        answer["Murder Rate"] = self.query_murder()
        answer["Car Theft Rate"] = self.query_car_theft()
        answer["Covid Deaths"] = self.query_covid()
        return answer

    # queries and parses the census.gov api for the relevant state
    def query_state(self):
        # name, pop, income, rent, house
        url = f"https://api.census.gov/data/2019/acs/acs5?get=NAME,B01003_001E,B19013_001E,B25064_001E,B25107_001E&for=place:*&in=state:{self.abbr}&key={self.census_api}"
        response = requests.get(url).json()
        response.pop(0)
        cityname = self.city.upper().strip()
        x = self.recursive_find(sorted(response), cityname)
        return x

    # does a binary search on a sorted API response
    def recursive_find(self, response, cityname):
        length = int(len(response)-1)
        half = length // 2 + 1

        lenvalue = self.name(response[0])

        if half > length:
            halfvalue = lenvalue
        else:
            halfvalue = self.name(response[half])


        added = cityname + " CITY"
        rmvd = cityname.replace(" CITY", "")

        if lenvalue == cityname or lenvalue == added or lenvalue == rmvd:
            return response[0]
        if halfvalue == cityname or halfvalue == added or halfvalue == rmvd:
            return response[half]
        elif lenvalue > cityname or self.name(response[length]) < cityname or length == 1:
            return ["Not found", "Not found", "Not found", "Not found", "Not found"]
        elif halfvalue > cityname:
            return self.recursive_find(response[:half], cityname)
        elif halfvalue < cityname:
            return self.recursive_find(response[-half:], cityname)

    # removes nametags from search values
    def name(self, value):
        if "CDP," in value[0]:
            return value[0].rpartition("CDP,")[0].strip().upper()
        elif "city," in value[0]:
            return value[0].rpartition("city,")[0].strip().upper()
        elif "borough," in value[0]:
            return value[0].rpartition("borough,")[0].strip().upper()
        elif "town," in value[0]:
            return value[0].rpartition("town,")[0].strip().upper()
        elif "village," in value[0]:
            return value[0].rpartition("village,")[0].strip().upper()
        elif "/" in value[0]:
            return value[0].rpartition("/")[0].strip().upper()
        else:
            return value[0].strip().upper()

    # queries and averages the murder rate in the relevant state for years > 2010
    def query_murder(self):
        state = urllib.parse.quote_plus(self.state)
        url = f"https://api.usa.gov/crime/fbi/sapi/api/data/nibrs/murder-and-nonnegligent-manslaughter/offense/states/{state}/count?api_key={self.gov_api}"
        response = requests.get(url)
        quote = response.json()
        offenses = 0
        years = 0
        for q in quote["results"]:
            if q["data_year"] > 2010:
                offenses += q["offense_count"]
                years += 1
        try:
            ratio = offenses/years
        except:
            return "~"

        ratio /= self.state_pop
        ratio *= 100000
        return round(ratio, 2)

    # queries and averages the car theft rate in the relevant state for years > 2010
    def query_car_theft(self):
        state = urllib.parse.quote_plus(self.state)
        url = f"https://api.usa.gov/crime/fbi/sapi/api/data/nibrs/motor-vehicle-theft/offense/states/{state}/count?api_key={self.gov_api}"
        response = requests.get(url)
        quote = response.json()
        offenses = 0
        years = 0
        for q in quote["results"]:
            if q["data_year"] > 2010:
                offenses += q["offense_count"]
                years += 1
        try:
            ratio = offenses/years
        except:
            return "~"

        ratio /= self.state_pop
        ratio *= 100000
        return round(ratio, 2)

    # queries and parses the covid death rate in the relevant state
    def query_covid(self):
        state = urllib.parse.quote_plus(self.state)
        url = f"https://api.covidactnow.org/v2/state/{state}.json?apiKey={self.cov_api}"
        response = requests.get(url)
        quote = response.json()
        stats = [quote["actuals"]["deaths"], quote["actuals"]["cases"], quote["actuals"]["vaccinationsCompleted"]]
        return stats