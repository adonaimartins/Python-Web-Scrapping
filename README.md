# Python-Web-Scrapping

Scrapes [Synetiq](https://auctions.synetiq.co.uk) salvage car auctions, compares current bid prices against estimated market values (`synetiq_scraper/data/cars_data.py`), and sends a WhatsApp alert via Twilio whenever a listing looks like a good buying opportunity.

## Project structure

```
synetiq_scraper/
├── __init__.py
├── main.py            # entry point: parameters, search loop, run()
├── models.py           # Car model + exceptions
├── scraper.py          # HTTP requests + HTML parsing
├── pricing.py           # fee/profit calculations and opportunity filtering
├── notifications.py     # WhatsApp alerts via Twilio
└── data/
    └── cars_data.py      # cars_list: brand/model -> estimated market value per year
legacy/                   # superseded snapshots of cars_data.py, kept for reference
config.py                 # Twilio credentials (git-ignored, create it yourself)
```

## Requirements

- Python 3.9+
- A Twilio account (Account SID, Auth Token, and WhatsApp-enabled sender number)

## Setup

1. **Clone the repo and create a virtual environment**

   ```bash
   git clone git@github.com:adonaimartins/Python-Web-Scrapping.git
   cd Python-Web-Scrapping
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Twilio credentials**

   Create a `config.py` file in the project root (this file is git-ignored and must never be committed):

   ```python
   TWILIO_ACCOUNT_SID = "your_account_sid"
   TWILIO_AUTH_TOKEN = "your_auth_token"
   ```

4. **Configure the car models to track**

   Edit `synetiq_scraper/data/cars_data.py` to add/adjust entries in `cars_list`. Each entry maps a model key to its brand and an estimated market value per year, e.g.:

   ```python
   "golf": {"car_brand": "volkswagen", "car_model": "golf", "2020": 12000, "2021": 13500, ...}
   ```

5. **Set recipient phone numbers**

   In `synetiq_scraper/pricing.py` and `synetiq_scraper/main.py`, update the WhatsApp numbers passed to `post_on_whatsapp(...)` to the numbers that should receive alerts.

## Running

From the project root:

```bash
python -m synetiq_scraper.main
```

The script will:

1. Loop through every car in `cars_list` and search Synetiq for matching listings.
2. Pull odometer, price, engine starts/drives, gearbox, and fuel type for each listing.
3. Calculate auction fees and potential profit against the estimated market value.
4. Send a WhatsApp message for each listing that clears the profit/mileage/price thresholds, followed by a summary message once the run finishes.

## Adjustable parameters

Near the top of `synetiq_scraper/main.py`:

| Parameter | Description |
|---|---|
| `spent_on_repairs_parameter` | Estimated repair cost to subtract from profit |
| `car_profit_parameter` | Minimum profit required to flag a car |
| `maximum_milleage_parameter` | Max odometer reading to consider |
| `car_price_threshold` | Max current bid price to consider |
| `days_in_advance` | How many days ahead to search (ignored when `search_any_day` is `True`) |
| `search_any_day` | If `True`, searches listings for any end date |
| `car_class` | Damage category filter: `ALL`, `X`, `N`, or `S` |
| `automatic_only` | If `True`, only flags automatic-gearbox cars |

## Notes

- `config.py` holds live credentials and is excluded from git via `.gitignore` — never commit it.
- Synetiq may change its page markup over time, which can break the HTML parsing in `find_car_data` / `set_car_drives_from_car_page` (`synetiq_scraper/scraper.py`).
- `legacy/` holds older, unused snapshots of the car pricing data kept only for reference.
