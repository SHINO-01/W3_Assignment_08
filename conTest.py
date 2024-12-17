from sqlalchemy import create_engine, text

# Database connection URL
DATABASE_URL = "postgresql://scrapy_user:scrapy_pass@postgres:5432/scrapyDB"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

try:
    # Establish a connection
    with engine.connect() as connection:
        # Execute a simple query to test the connection
        result = connection.execute(text("SELECT 1"))
        print(f"Database connection successful: {result.scalar()}")
except Exception as e:
    print(f"Database connection failed: {e}")
