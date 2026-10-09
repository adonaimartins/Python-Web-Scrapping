from .data.cars_data import cars_list
from .notifications import post_on_whatsapp
from .pricing import loop_through_cars
from .scraper import cookies, get_html, get_synetic_url, headers

spent_on_repairs_parameter = 0
car_profit_parameter = 0
maximum_milleage_parameter = 70000
car_price_threshold = 1000
days_in_advance = 1
search_any_day = True #this ifnores cars in advance and will search for all cars at anytime
car_class = "ALL"
automatic_only = False
ignore_three_door = True #do not ignore 3 doors - some 3 door cars are usefull like the fiat 500


def _search_car(car_search_model, car_brand, car_class, search_any_day, days_in_advance):
    search_query = f"{car_brand}+{car_search_model}"
    print(search_query)

    url = get_synetic_url(f"{search_query}", car_class, search_any_day, days_in_advance) #CHANGE FOR DATE TO SEARCH
    html_search_car_results = get_html(url, headers, cookies, True)

    print(f"searching for: {car_brand} {car_search_model}")
    vehicle_lists = html_search_car_results.find_all('div', class_='row vehicle_list')

    return vehicle_lists


def _search_and_process_one_car(details, car_class, search_any_day, days_in_advance, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only):
    car_array = dict(details.items())

    car_search_model = car_array["car_model"]
    car_brand = car_array['car_brand']

    vehicle_lists = _search_car(car_search_model, car_brand, car_class, search_any_day, days_in_advance)

    if len(vehicle_lists) == 0 :
        return

    loop_through_cars(vehicle_lists, car_search_model, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only)


def search_all_cars(car_class, search_any_day, days_in_advance, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only):
    for car, details in cars_list.items():
        # print(f"Car: {car}")

        _search_and_process_one_car(details, car_class, search_any_day, days_in_advance, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only)


def _build_summary_message():
    mycarcheck_link = "https://www.mycarcheck.com"
    return f"PARAMETERS\nspent_on_repairs_parameter: {spent_on_repairs_parameter}\ncar_profit_parameter: {car_profit_parameter}\nmaximum_milleage_parameter: \n{maximum_milleage_parameter}\ncar_price_threshold: {car_price_threshold}\ndays_in_advance: {days_in_advance}\ncar_class: {car_class}\nDO NOT FORGET TO CHECK MOT HISTORY HERE:\n{mycarcheck_link}\nEND OF THE SCRIPT 🚗🚗🚗🚗🚗🚗🚗🚗🚗🚗🚗"


def _send_summary_message(message):
    post_on_whatsapp("+447423162427", message)
    post_on_whatsapp("+447465717175", message)
    post_on_whatsapp("+447452881822", message)


def run():
    search_all_cars(car_class, search_any_day, days_in_advance, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only)

    message = _build_summary_message()

    _send_summary_message(message)


if __name__ == "__main__":
    run()

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
