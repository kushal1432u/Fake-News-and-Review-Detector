# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Database Setup Script
# ═══════════════════════════════════════════════════════════
# Run once:  python setup_db.py
# Creates the database and 'detection_history' table.

import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def setup_database():
    """Create the Fake News and Review Detector database and detection_history table."""
    connection = None
    try:
        # Connect without specifying a database first
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection.cursor() as cursor:
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;")
            cursor.execute(f"USE `{DB_NAME}`;")

            # Create detection_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detection_history (
                    id              INT AUTO_INCREMENT PRIMARY KEY,
                    detection_type  ENUM('news', 'review', 'image') NOT NULL,
                    input_text      TEXT,
                    image_filename  VARCHAR(255),
                    result          ENUM('REAL', 'FAKE') NOT NULL,
                    confidence      FLOAT NOT NULL,
                    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        connection.commit()
        print("Database ready.")

    except pymysql.MySQLError as e:
        print(f"MySQL error: {e}")
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    setup_database()
