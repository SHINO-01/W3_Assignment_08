import scrapy
import re
import json

class HotelSpider(scrapy.Spider):
    name = "hotel_spider"
    start_urls = ["https://uk.trip.com/hotels/list?city=86491"]

    def parse(self, response):
        # Extract the JavaScript containing the `window.IBU_HOTEL` variable
        script_data = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()

        if script_data:
            # Use regex to extract the JSON part of `window.IBU_HOTEL`
            match = re.search(r"window\.IBU_HOTEL\s*=\s*({.*?});", script_data, re.DOTALL)
            if match:
                hotel_data = match.group(1)  # Extracted JSON string

                try:
                    # Parse the JSON data
                    hotel_json = json.loads(hotel_data)

                    # Save the data to a JSON file
                    with open("hotel_datav03.json", "w", encoding="utf-8") as f:
                        json.dump(hotel_json, f, indent=4, ensure_ascii=False)

                    self.log("Data successfully saved to hotel_data.json")
                except json.JSONDecodeError as e:
                    self.log(f"Failed to parse JSON: {e}")
            else:
                self.log("No matching data found for window.IBU_HOTEL")
        else:
            self.log("No <script> tag containing window.IBU_HOTEL found")
