from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime, timedelta

from .models import CarTooOldException

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


def _extract_listing_tags(car_row):
    car_title = car_row.find('div', class_='list_title')

    # synetic html tags
    car_a_tag = car_title.find('a', href=True)
    h2_tag = car_a_tag.find('h2') if car_a_tag else None
    car_title_text = h2_tag.text.strip().split()
    car_data_table_synetic = car_row.find_all('span', class_='list-group-text-item')
    car_price_synetic = car_row.find_all('span', class_='list_price_2')
    car_coundown_synetic = car_row.find_all('span', class_='countdown_time')

    return car_a_tag, car_title_text, car_data_table_synetic, car_price_synetic, car_coundown_synetic


def _set_car_title_fields(car, car_title_text):
    # data extracted from html tags
    car.year = car_title_text[0].lower()
    car.brand = car_title_text[1].lower()
    car.model = car_title_text[2].lower()

    if int(car.year) < 2014 :
        raise CarTooOldException("error: car too old")


def _set_car_odometer(car, car_data_table_synetic):
    try:
        car.odometer = int(car_data_table_synetic[3].text.replace(',', ''))
    except:
        # raise NotAvailableOrdometerException()
        car.odometer = 0


def _set_car_price(car, car_price_synetic):
    car.price = int(car_price_synetic[0].text.replace('£', '').replace(',', ''))


def _set_car_distance(car, car_data_table_synetic):
    car.distance = car_data_table_synetic[5].text


def _set_car_countdown(car, car_coundown_synetic):
    car.hours_left = car_coundown_synetic[1].text
    car.minutes_left = car_coundown_synetic[2].text


def _set_car_link(car, car_a_tag):
    car.car_link = "https://auctions.synetiq.co.uk" + car_a_tag['href']


def find_car_data(car_row, car):
    car_a_tag, car_title_text, car_data_table_synetic, car_price_synetic, car_coundown_synetic = _extract_listing_tags(car_row)

    _set_car_title_fields(car, car_title_text)
    _set_car_odometer(car, car_data_table_synetic)
    _set_car_price(car, car_price_synetic)
    _set_car_distance(car, car_data_table_synetic)
    _set_car_countdown(car, car_coundown_synetic)
    _set_car_link(car, car_a_tag)
    try:
        set_car_drives_from_car_page(car)
    except Exception as e:
        print("ERROR: there is an issue with the Car Page (not the search page)")


def _fetch_car_page_soup(car):
    car_session = HTMLSession()
    car_sitemap_response = car_session.get(car.car_link, headers=headers)
    if car_sitemap_response.status_code == 200:
        return BeautifulSoup(car_sitemap_response.html.html, 'html.parser')
    return None


def _set_car_detail_fields(car, car_data):
    car_engine_starts_key = car_data[17].find('span', class_='d-xl-inline-block').text
    car.engine_starts = car_data[17].find('span', class_='list-group-text-item').text
    car_engine_drives_key = car_data[18].find('span', class_='d-xl-inline-block').text
    car.engine_drives = car_data[18].find('span', class_='list-group-text-item').text
    car_gearbox_key = car_data[2].find('span', class_='d-md-inline-block').text
    car.gearbox = car_data[2].find('span', class_='list-group-text-item').text
    car_car_engine_key = car_data[1].find('span', class_='d-md-inline-block').text
    car.engine = car_data[1].find('span', class_='list-group-text-item').text

    return car_engine_starts_key, car_engine_drives_key


def _validate_engine_keys(car_engine_starts_key, car_engine_drives_key):
    if car_engine_starts_key.lower() != "Engine starts".lower() or car_engine_drives_key.lower() != "Drivetrain drives".lower():
        print("ENGINE STARTS html tag have changed")
        print(car_engine_starts_key)
        print(car_engine_drives_key)

    # ADD STATEMENT IN CASE PAGE BREAKS


def set_car_drives_from_car_page(car):
    # get data from Car Page

    car_soup = _fetch_car_page_soup(car)
    if car_soup is not None:
        car_data = car_soup.find_all('div', class_='info-on-two-lines d-flex justify-content-between align-items-center')

        car_engine_starts_key, car_engine_drives_key = _set_car_detail_fields(car, car_data)


        _validate_engine_keys(car_engine_starts_key, car_engine_drives_key)
