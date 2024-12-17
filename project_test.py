import pytest
import json
import os
from scrapy.http import HtmlResponse, Request
from hotel_scrapper.spiders.hotel_spider import HotelSpider
from hotel_scrapper.pipelines import HotelScrapperPipeline
from hotel_scrapper.middlewares import HotelScrapperSpiderMiddleware, HotelScrapperDownloaderMiddleware
from hotel_scrapper.items import HotelScrapperItem

TEST_JSON_FILE = "test_combined_cities.json"
TEST_JSON_CONTENT = {
    "cities": [
        {
            "name": "London",
            "recommendHotels": [
                {
                    "hotelName": "Test Hotel 1",
                    "ratingTxt": "4.5",
                    "fullAddress": "123 Test St, London",
                    "lat": 51.5074,
                    "lon": -0.1278,
                    "brief": "Luxury Room",
                    "prices": {"priceInfos": [{"type": "AverageWithoutTax", "price": 200}]},
                    "imgUrl": "/images/test1.jpg",
                    "hotelJumpUrl": "https://testurl.com/hotel1"
                }
            ]
        }
    ]
}

@pytest.fixture
def json_file():
    with open(TEST_JSON_FILE, "w") as file:
        json.dump(TEST_JSON_CONTENT, file)
    yield TEST_JSON_FILE
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)

@pytest.fixture
def spider():
    return HotelSpider()

def test_pipeline_process_item():
    pipeline = HotelScrapperPipeline()
    item = HotelScrapperItem(
        city="London",
        title="Test Hotel",
        rating="4.5",
        location="123 Test St, London",
        latitude=51.5074,
        longitude=-0.1278,
        room_type="Luxury Room",
        price=200,
        images="test_image.jpg",
        url="https://testurl.com/hotel1"
    )
    processed_item = pipeline.process_item(item)
    assert processed_item["title"] == "Test Hotel"

def test_spider_start_requests(spider, tmpdir):
    combined_cities = tmpdir.join("Test_combined_cities.json")
    combined_cities.write(json.dumps(TEST_JSON_CONTENT))

    spider.log = lambda msg: None
    with open("Test_combined_cities.json", "w") as f:
        json.dump(TEST_JSON_CONTENT, f)

    requests = list(spider.start_requests())
    assert len(requests) == 1

def test_spider_create_json(spider):
    response = HtmlResponse(
        url="https://test-url.com",
        body="""
        <script>
        window.IBU_HOTEL = {"initData": {"htlsData": {"inboundCities": [{"name": "Paris"}]}}}
        </script>
        """,
        encoding="utf-8"
    )
    spider.create_json(response)
    assert os.path.exists("Test_combined_cities.json")
    with open("Test_combined_cities.json") as f:
        data = json.load(f)
        assert data["cities"][0]["name"] == "Paris"
    os.remove("Test_combined_cities.json")

def test_get_price(spider):
    hotel = {"prices": {"priceInfos": [{"type": "AverageWithoutTax", "price": 150}]}}
    assert spider.get_price(hotel) == 150

def test_middlewares_spider_middleware():
    middleware = HotelScrapperSpiderMiddleware()
    response = HtmlResponse(url="https://testurl.com", body=b"", encoding="utf-8")
    result = list(middleware.process_spider_output(response, [], None))
    assert result == []

def test_middlewares_downloader_middleware():
    middleware = HotelScrapperDownloaderMiddleware()
    request = Request(url="https://testurl.com")
    response = HtmlResponse(url="https://testurl.com", body=b"test body", encoding="utf-8")
    result = middleware.process_response(request, response, None)
    assert result.status == 200
