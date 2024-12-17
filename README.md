<body>
    <h1>Hotel Scraper Project</h1> 
    <h2>1. Introduction</h2>
    <p>The Hotel Scraper project is a web scraping application built using the Scrapy framework. It fetches hotel data from Trip.com, including hotel details, images, and prices. The scraped data is saved into a database and hotel images are downloaded locally.</p>
    <h2>2. Table of Contents</h2>
    <ul>
        <li><a href="#introduction">1. Introduction</a></li>
        <li><a href="#structure">2. Project Folder Structure</a></li>
        <li><a href="#setup">3. Downloading and Setting Up the Project</a></li>
        <li><a href="#how-to-run">4. How to Run</a></li>
        <li><a href="#output">5. Sample Output</a></li>
        <li><a href="#documentation">6. Technical Documentation of All Functions</a></li>
        <li><a href="#issues">7. Known Issues</a></li>
        <li><a href="#summary">8. Summary</a></li>
    </ul>
    <h2 id="structure">3. Project Folder Structure</h2>
    <pre>
    project/
    |-- hotel_scraper/
    |   |-- spiders/
    |   |    |-- hotel_spider.py  # Main spider logic
    |   |-- pipelines.py         # Custom pipelines for image download and database storage
    |   |-- items.py             # Item definitions
    |   |-- settings.py          # Scrapy project settings
    |-- combined_cities.json     # JSON file to store city data
    |-- media/
        |-- images/              # Folder where downloaded images are stored
    </pre>
    <h2 id="setup">4. Downloading and Setting Up the Project</h2>
    <ol>
        <li>Clone the project repository:
            <pre>git clone https://github.com/SHINO-01/W3_Assignment_08.git</pre>
        </li>
        <li>Navigate to the project folder:</li>
        <pre>cd hotel-scraper</pre>
        <li>Create a Venv and Install the required dependencies:</li>
        <pre>python3 -m venv .venv</pre>
        <pre>source .venv/bin/activate</pre>
        <pre>pip install -r requirements.txt</pre>
    </ol>
    <h2 id="how-to-run">5. How to Run</h2>
    <ol>
        <li>Run the docker using <code>docker-compose up --build</code></li>
        <li>Navigate to localhost:5050</li>
        <li>Login with username: admin@admin.com and pass:admin1234</li>
        <li>Select Server and click the register option from the object dropdown.</li>
        <li>In general tab Name Field: HotelDB, then in Connedtion Tab, Host Field: postgres_scrapy, Username: scrapy_user, pass: scrapy_pass, then hit connect</li>
        <li>make sure all the containers are running.</li>
        <li>Run the spider for the first time to fetch city data and generate the JSON file:</li>
        <pre>docker exec -it scrapy_container scrapy crawl hotel_spider</pre>
        <li>Restart the spider to process the data and download hotel images.</li>
        <pre>sdocker exec -it scrapy_container scrapy crawl hotel_spider</pre>
    </ol>
    <h2 id="output">6. Sample Output</h2>
    <p>The database stores the following information:</p>
    <pre>
    | ID | City       | Title          | Rating | Location         | Latitude | Longitude | Images                   | Price |
    |----|------------|----------------|--------|------------------|----------|-----------|-------------------------|-------|
    | 1  | London     | Hotel ABC      | 4.5    | 123 Main St, UK  | 51.5074  | -0.1278   | image1.jpg, image2.jpg   | 150   |
    | 2  | New York   | Hotel XYZ      | 4.2    | 456 Park Ave, NY | 40.7128  | -74.0060  | image3.jpg, image4.jpg   | 200   |
    </pre>
    <p>Hotel images are stored in the <code>media/images</code> folder.</p>
    <h2 id="documentation">7. Technical Documentation of All Functions</h2>
    <ul>
        <li><strong>start_requests</strong>: Checks if the <code>combined_cities.json</code> file exists. If not, it fetches city data; otherwise, it processes the data.</li>
        <li><strong>create_json</strong>: Scrapes city data and stores it in <code>combined_cities.json</code>.</li>
        <li><strong>get_price</strong>: Extracts price information from hotel data.</li>
    </ul>
    <h2 id="issues">8. Known Issues</h2>
    <ul>
        <li>Some image URLs return 404 errors. These are logged, and the spider continues.</li>
        <li>Ensure a proper database connection string in the <code>pipelines.py</code> file.</li>
    </ul>
    <h2 id="summary">9. Summary</h2>
    <p>This project demonstrates the use of Scrapy for web scraping and managing downloaded media files. It includes functionalities for data persistence, image downloading, and robust error handling.</p>
</body>
