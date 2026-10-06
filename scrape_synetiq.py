import requests
from bs4 import BeautifulSoup
import time
import random
from requests_html import HTMLSession
from cars_data import cars_list
from twilio.rest import Client
from datetime import datetime, timedelta
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

# 0=all, 7 = X, N = 5, S = 6

# Define the headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

cookies = {
    '_gcl_au': '1.1.1035601252.1716031519',
    '_fbp': 'fb.2.1716031518961.1009716101',
    '__zlcmid': '1LpmjAWPaEaUj1Z',
    'PHPSESSID': 'd7mptv1i6li5f1fperaau10cr1',
    'AuctionCookiePrefs': 'YTo2OntzOjc6IlNFU1NJT04iO3M6MToiMiI7czo0OiJDSEFUIjtzOjE6IjIiO3M6NzoiUFJFRlMyOCI7czoxOiIyIjtzOjI6IkdBIjtzOjE6IjIiO3M6MjoiSEoiO3M6MToiMiI7czoyOiJUQSI7czoxOiIyIjt9',
}

years = [
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024",
    "2025",
    "2026"
]

# -------------------  classes ------

class CarTooOldException(Exception):
    """Exception class to handle cars too old."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ERROR: {self.message}"

class NotAvailableOrdometerException(Exception):
    """Exception Class to handle not available ordometer."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ERROR: {self.message}"


class Car:
    def __init__(
            self, 
            year=None, 
            brand=None, 
            model=None, 
            odometer=None, 
            price=None,
            distance=None, 
            hours_left=None, 
            minutes_left=None, 
            link=None,
            engine_starts=None, 
            engine_drives=None, 
            avg_price=None, 
            avg_price_depreciated=None, 
            potential_earning=None,
            gearbox=None,
            engine=None
    ):
        self.year = year
        self.brand = brand
        self.model = model
        self.odometer = odometer
        self.price = price
        self.distance = distance
        self.hours_left = hours_left
        self.minutes_left = minutes_left
        self.car_link = link
        self.engine = engine
        self.engine_starts = engine_starts
        self.engine_drives = engine_drives
        self.avg_price = avg_price 
        self.avg_price_depreciated = avg_price_depreciated
        self.potential_earning = potential_earning
        self.gearbox = gearbox

    def __str__(self):
        return (f"Car Details:\n"
                f"Year: {self.year}\n"
                f"Brand: {self.brand}\n"
                f"Model: {self.model}\n"
                f"Odometer: {self.odometer} miles\n"
                f"Gearbox: {self.gearbox}\n"
                f"Price: ${self.price}\n"
                f"Distance: {self.distance} miles\n"
                f"Time Left: {self.hours_left} hours and {self.minutes_left} minutes\n"
                f"Link: {self.car_link}\n"
                f"Engine: {self.engine}\n"
                f"Engine Starts: {self.engine_starts}\n"
                f"Engine Drives: {self.engine_drives}\n"
                f"avg price: {self.avg_price}\n"
                f"avg price depreciated: {self.avg_price_depreciated}\n"
                f"potential earning: {self.potential_earning}\n")



# -------------------  FUNCTIONS ------
# if input 2, it will increase the day by 2 days
# if no parameters input, the default day will be today
def get_search_by_day(days):

    if days is None:
        return (datetime.today()).strftime("%Y%m%d") #today

    return (datetime.today() + timedelta(days=days)).strftime("%Y%m%d")

def get_synetic_url(search_string, car_category, search_any_day, day_to_search = None):

    car_categories_damage = {
        "ALL": 0,
        "X": 7,
        "N": 5,
        "S": 6
    }

    # search per car and year = fiesta+2018
    if search_any_day == True :
        return f"https://auctions.synetiq.co.uk/auction/items/?make=0&fuel=0&transmission=0&category={car_categories_damage[car_category]}&layout=r20&seller=0&location=0&distance=0&search={search_string}&sort=8&tab=1"
    return f"https://auctions.synetiq.co.uk/auction/items/?make=0&fuel=0&transmission=0&category={car_categories_damage[car_category]}&layout=r20&seller=0&location=0&time={get_search_by_day(day_to_search)}&distance=0&search={search_string}&sort=8&tab=1"


def get_html(url, request_headers, request_cookies, retry:True):
    session = HTMLSession()
    sitemap_response = session.get(url, headers=request_headers, cookies=request_cookies)
    # sitemap_response.html.render(sleep=0.1)  # Render JavaScript, with a delay of 3 seconds



    if sitemap_response.status_code == 200:
        return BeautifulSoup(sitemap_response.html.html, 'html.parser')
        
    if retry == True:
        get_html(url, request_headers, request_cookies, False) 

    
    print("ERROR TRYING TO SEARCH GAMES. SYNETIQ COULD BE DOWN, or request changed")

def calculateTotalFees(car_price):
    auction_fees = 0
    if car_price > 0 and car_price < 250:
        auction_fees = 150
    elif car_price >= 250 and car_price < 500:
        auction_fees = 170
    elif car_price >= 500 and car_price < 750:
        auction_fees = 220
    elif car_price >= 750 and car_price < 1000:
        auction_fees = 240
    elif car_price >= 1000 and car_price < 1500:
        auction_fees = 280
    elif car_price >= 1500 and car_price < 2000:
        auction_fees = 330
    elif car_price >= 2000 and car_price < 2500:
        auction_fees = 380
    elif car_price >= 2500 and car_price < 3000:
        auction_fees = 440
    elif car_price >= 3000 and car_price < 4000:
        auction_fees = 510
    elif car_price >= 4000 and car_price < 5000:
        auction_fees = 580
    elif car_price >= 5000 and car_price < 7500:
        auction_fees = 650
    elif car_price >= 7500 and car_price < 10000:
        auction_fees = 670
    elif car_price >= 10000 and car_price < 12500:
        auction_fees = 800
    elif car_price >= 12500 and car_price < 15000:
        auction_fees = 950
    elif car_price >= 15000:
        auction_fees = 1050
    else:
        auction_fees = 0  # Fallback case if car_price is invalid
    return auction_fees * 1.2


def loop_through_cars(list_of_vehicles, car_search_model, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only):

    print(f"THIS IS THE SIZE{len(list_of_vehicles)}")
    for vehicle_row in list_of_vehicles:
        car = Car()
        try:
            find_car_data(vehicle_row, car)
        except CarTooOldException as e:
            continue
        # except NotAvailableOrdometerException as e:
        #     continue
        except Exception as e:
            print("ERROR: CAR ROW ISSUE  ")
        print("  ----  ")

        try:
            total_fees = calculateTotalFees(car.price)            
            car_profit = ((cars_list[car_search_model][car.year]  * 0.75) - car.price - total_fees) - spent_on_repairs_parameter
            dont_invest_more_than_this = (cars_list[car_search_model][car.year]  * 0.75)  - total_fees - spent_on_repairs_parameter - 2000
            if is_the_car_an_opportunity(car, car_search_model, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, car_profit, automatic_only) :
                print(car) 
                print("the car is a good portunity")

                message = f"carName: {car.brand} - {car.model}\ncar price on the street: {car.avg_price}\ncar price depreciated: {car.avg_price_depreciated}\ncurrent bid price: {car.price}\nTotal bid price with fees: {car.price + total_fees}\navg bid price with delivery and repair:{car.price + total_fees + 1300}\npotential earning: {car.potential_earning}\nOdometer: {car.odometer}\nGearbox: {car.gearbox}\n\nDO NOT INVEST MORE THAN: {dont_invest_more_than_this} to earn {car_profit_parameter}\nthis car is a very good opportunity: \n{car.car_link}"
                
                try:

                    post_on_whatsapp("+447423162427", message)
                    post_on_whatsapp("+447465717175", message)
                    post_on_whatsapp("+447452881822", message)
                except Exception as e:
                    print("ERROR SENDING WHATS APP MESSAGE")
                    raise e

        except Exception as e:
            print("ERROR: ERROR CALCULATING AN OPPORTUNITY  ")
            print(e)
            print("ERROR:END END")
        # break

def is_the_car_an_opportunity(car:Car, car_search_model, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, car_profit, automatic_only):

    if (car.engine_drives.lower() == "yes" and 
        car.engine_starts.lower() == "yes" and 
        car_profit > car_profit_parameter and 
        car.odometer < maximum_milleage_parameter and 
        car.price < car_price_threshold and 
        (
            "petrol" in car.engine.lower() or 
            "diesel" in car.engine.lower()
        )
    ) :
        if automatic_only == True and "automatic" not in car.gearbox.lower():
            return False
        car.avg_price = cars_list[car_search_model][car.year]
        car.avg_price_depreciated = cars_list[car_search_model][car.year] * 0.75
        car.potential_earning = car_profit
        return True

    # print(False)
    return False

def post_on_whatsapp(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{phone_number}'
    )

    print(message.sid)


def find_car_data(car_row, car):
    car_title = car_row.find('div', class_='list_title')

    # synetic html tags
    car_a_tag = car_title.find('a', href=True)
    h2_tag = car_a_tag.find('h2') if car_a_tag else None
    car_title_text = h2_tag.text.strip().split()
    car_data_table_synetic = car_row.find_all('span', class_='list-group-text-item')
    car_price_synetic = car_row.find_all('span', class_='list_price_2')
    car_coundown_synetic = car_row.find_all('span', class_='countdown_time')


    # data extracted from html tags
    car.year = car_title_text[0].lower()
    car.brand = car_title_text[1].lower()
    car.model = car_title_text[2].lower()

    if int(car.year) < 2014 :
        raise CarTooOldException("error: car too old")

    try:
        car.odometer = int(car_data_table_synetic[3].text.replace(',', ''))
    except:
        # raise NotAvailableOrdometerException()
        car.odometer = 0

    

    car.price = int(car_price_synetic[0].text.replace('£', '').replace(',', ''))


    car.distance = car_data_table_synetic[5].text


    car.hours_left = car_coundown_synetic[1].text
    car.minutes_left = car_coundown_synetic[2].text
    car.car_link = "https://auctions.synetiq.co.uk" + car_a_tag['href']



    try:
        set_car_drives_from_car_page(car)
    except Exception as e:
        print("ERROR: there is an issue with the Car Page (not the search page)")


def set_car_drives_from_car_page(car):
    # get data from Car Page

    car_session = HTMLSession()
    car_sitemap_response = car_session.get(car.car_link, headers=headers)
    if car_sitemap_response.status_code == 200:
        car_soup = BeautifulSoup(car_sitemap_response.html.html, 'html.parser')
        car_data = car_soup.find_all('div', class_='info-on-two-lines d-flex justify-content-between align-items-center')

        car_engine_starts_key = car_data[17].find('span', class_='d-xl-inline-block').text
        car.engine_starts = car_data[17].find('span', class_='list-group-text-item').text
        car_engine_drives_key = car_data[18].find('span', class_='d-xl-inline-block').text
        car.engine_drives = car_data[18].find('span', class_='list-group-text-item').text
        car_gearbox_key = car_data[2].find('span', class_='d-md-inline-block').text
        car.gearbox = car_data[2].find('span', class_='list-group-text-item').text
        car_car_engine_key = car_data[1].find('span', class_='d-md-inline-block').text
        car.engine = car_data[1].find('span', class_='list-group-text-item').text


        if car_engine_starts_key.lower() != "Engine starts".lower() or car_engine_drives_key.lower() != "Drivetrain drives".lower():
            print("ENGINE STARTS html tag have changed")
            print(car_engine_starts_key)
            print(car_engine_drives_key)

        # ADD STATEMENT IN CASE PAGE BREAKS


# ------------------- execution code -----------



spent_on_repairs_parameter = 0
car_profit_parameter = 0
maximum_milleage_parameter = 70000
car_price_threshold = 1000
days_in_advance = 3
search_any_day = True #this ifnores cars in advance and will search for all cars at anytime
car_class = "ALL"
automatic_only = False
ignore_three_door = True #do not ignore 3 doors - some 3 door cars are usefull like the fiat 500



for car, details in cars_list.items():
    # print(f"Car: {car}")

    car_array = dict(details.items())


    car_search_model = car_array["car_model"]
    car_brand = car_array['car_brand']
    search_query = f"{car_brand}+{car_search_model}"
    print(search_query)

    url = get_synetic_url(f"{search_query}", car_class, search_any_day, days_in_advance) #CHANGE FOR DATE TO SEARCH
    html_search_car_results = get_html(url, headers, cookies, True)

    print(f"searching for: {car_brand} {car_search_model}")
    vehicle_lists = html_search_car_results.find_all('div', class_='row vehicle_list')

    if len(vehicle_lists) == 0 :
        continue

    loop_through_cars(vehicle_lists, car_search_model, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only)

mycarcheck_link = "https://www.mycarcheck.com"
message = f"PARAMETERS\nspent_on_repairs_parameter: {spent_on_repairs_parameter}\ncar_profit_parameter: {car_profit_parameter}\nmaximum_milleage_parameter: \n{maximum_milleage_parameter}\ncar_price_threshold: {car_price_threshold}\ndays_in_advance: {days_in_advance}\ncar_class: {car_class}\nDO NOT FORGET TO CHECK MOT HISTORY HERE:\n{mycarcheck_link}\nEND OF THE SCRIPT 🚗🚗🚗🚗🚗🚗🚗🚗🚗🚗🚗"


post_on_whatsapp("+447423162427", message)
post_on_whatsapp("+447465717175", message)
post_on_whatsapp("+447452881822", message)

# start script a 9 am
# open aunction cars for today (DONE)
# search each car - puma, corsa, etc; one by one
# loop through cars (DONE)
# loop through pages -- optional
# loop through years
# open car url and find (DONE)
# engine starts
# reserve is met
#
# message on whats app
# check if the reserve is met
# check if the bid happens today

# set an alarm to run the script 10 mins before the bid ends
# when the times up, the script should run for this specific link and check again
# if the amount is X compared to the price in the market, notify whats app


# delivery costs = £2.88 per mile