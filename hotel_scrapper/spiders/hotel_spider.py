import scrapy
import json
import os
import random
from scrapy.exceptions import CloseSpider

class HotelSpider(scrapy.Spider):
    name = "hotel_spider"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def start_requests(self):
        json_file_path = "combined_cities.json"

        if not os.path.exists(json_file_path):
            # Create JSON if it does not exist
            self.log("Creating combined_cities.json by fetching data from the website.")
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.create_json)
        else:
            # JSON exists, process hotel data
            self.log("Using existing combined_cities.json to fetch hotel data.")
            with open(json_file_path, "r", encoding="utf-8") as file:
                combined_cities = json.load(file)

            for city in combined_cities.get("cities", []):
                city_name = city.get("name")
                recommend_hotels = city.get("recommendHotels", [])

                # Select 3 random hotels from the list
                selected_hotels = random.sample(recommend_hotels, min(3, len(recommend_hotels)))

                for hotel in selected_hotels:
                    yield {
                        "city": city_name,
                        "title": hotel.get("hotelName"),
                        "rating": hotel.get("ratingTxt"),
                        "location": hotel.get("fullAddress"),
                        "latitude": hotel.get("lat"),
                        "longitude": hotel.get("lon"),
                        "room_type": hotel.get("brief"),
                        "price": self.get_price(hotel),
                        "images": hotel.get("imgUrl"),
                        "url": hotel.get("hotelJumpUrl"),
                    }

    def create_json(self, response):
        # Extract city data from JavaScript
        script_data = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        if script_data:
            import re
            match = re.search(r"window\.IBU_HOTEL\s*=\s*({.*?});", script_data, re.DOTALL)
            if match:
                try:
                    hotel_json = json.loads(match.group(1))
                    inbound_cities = hotel_json.get("initData", {}).get("htlsData", {}).get("inboundCities", [])
                    outbound_cities = hotel_json.get("initData", {}).get("htlsData", {}).get("outboundCities", [])
                    combined_cities = {"cities": inbound_cities + outbound_cities}

                    # Save combined city data to JSON
                    with open("combined_cities.json", "w", encoding="utf-8") as f:
                        json.dump(combined_cities, f, indent=4, ensure_ascii=False)
                    self.log("Saved city data to combined_cities.json")

                    # Stop the spider since the primary task is done
                    raise CloseSpider(reason="JSON file created. Restart the spider to process data.")
                except json.JSONDecodeError as e:
                    self.log(f"Error parsing city data JSON: {e}")
                    raise CloseSpider(reason="Failed to create JSON file.")

    def get_price(self, hotel):
        price_info = hotel.get("prices", {}).get("priceInfos", [])
        for price in price_info:
            if price.get("type") == "AverageWithoutTax":
                return price.get("price")
        return None
