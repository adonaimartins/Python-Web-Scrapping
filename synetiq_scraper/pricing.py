from .data.cars_data import cars_list
from .models import Car, CarTooOldException
from .notifications import post_on_whatsapp
from .scraper import find_car_data


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


def _build_car_from_row(vehicle_row):
    car = Car()
    try:
        find_car_data(vehicle_row, car)
    except CarTooOldException as e:
        return None
    # except NotAvailableOrdometerException as e:
    #     continue
    except Exception as e:
        print("ERROR: CAR ROW ISSUE  ")
    print("  ----  ")
    return car


def _compute_total_fees_and_profit(car, car_search_model, spent_on_repairs_parameter):
    total_fees = calculateTotalFees(car.price)
    car_profit = ((cars_list[car_search_model][car.year]  * 0.75) - car.price - total_fees) - spent_on_repairs_parameter
    dont_invest_more_than_this = (cars_list[car_search_model][car.year]  * 0.75)  - total_fees - spent_on_repairs_parameter - 2000
    return total_fees, car_profit, dont_invest_more_than_this


def _build_opportunity_message(car, total_fees, car_profit_parameter, dont_invest_more_than_this):
    return f"carName: {car.brand} - {car.model}\ncar price on the street: {car.avg_price}\ncar price depreciated: {car.avg_price_depreciated}\ncurrent bid price: {car.price}\nTotal bid price with fees: {car.price + total_fees}\navg bid price with delivery and repair:{car.price + total_fees + 1300}\npotential earning: {car.potential_earning}\nOdometer: {car.odometer}\nGearbox: {car.gearbox}\n\nDO NOT INVEST MORE THAN: {dont_invest_more_than_this} to earn {car_profit_parameter}\nthis car is a very good opportunity: \n{car.car_link}"


def _send_opportunity_alerts(message):
    post_on_whatsapp("+447423162427", message)
    post_on_whatsapp("+447465717175", message)
    post_on_whatsapp("+447452881822", message)


def _evaluate_and_notify(car, car_search_model, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only):
    try:
        total_fees, car_profit, dont_invest_more_than_this = _compute_total_fees_and_profit(car, car_search_model, spent_on_repairs_parameter)
        if is_the_car_an_opportunity(car, car_search_model, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, car_profit, automatic_only) :
            print(car)
            print("the car is a good portunity")

            message = _build_opportunity_message(car, total_fees, car_profit_parameter, dont_invest_more_than_this)

            try:

                _send_opportunity_alerts(message)
            except Exception as e:
                print("ERROR SENDING WHATS APP MESSAGE")
                raise e

    except Exception as e:
        print("ERROR: ERROR CALCULATING AN OPPORTUNITY  ")
        print(e)
        print("ERROR:END END")


def loop_through_cars(list_of_vehicles, car_search_model, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only):

    print(f"THIS IS THE SIZE{len(list_of_vehicles)}")
    for vehicle_row in list_of_vehicles:
        car = _build_car_from_row(vehicle_row)
        if car is None:
            continue

        _evaluate_and_notify(car, car_search_model, spent_on_repairs_parameter, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, automatic_only)
        # break

def _meets_opportunity_criteria(car, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, car_profit):
    return (car.engine_drives.lower() == "yes" and
        car.engine_starts.lower() == "yes" and
        car_profit > car_profit_parameter and
        car.odometer < maximum_milleage_parameter and
        car.price < car_price_threshold and
        (
            "petrol" in car.engine.lower() or
            "diesel" in car.engine.lower()
        )
    )


def _apply_opportunity_pricing(car, car_search_model, car_profit):
    car.avg_price = cars_list[car_search_model][car.year]
    car.avg_price_depreciated = cars_list[car_search_model][car.year] * 0.75
    car.potential_earning = car_profit


def is_the_car_an_opportunity(car:Car, car_search_model, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, car_profit, automatic_only):

    if _meets_opportunity_criteria(car, car_profit_parameter, maximum_milleage_parameter, car_price_threshold, car_profit) :
        if automatic_only == True and "automatic" not in car.gearbox.lower():
            return False
        _apply_opportunity_pricing(car, car_search_model, car_profit)
        return True

    # print(False)
    return False
