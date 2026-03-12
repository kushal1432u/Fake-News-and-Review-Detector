# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Database Handler
# ═══════════════════════════════════════════════════════════
# Provides save_result() and get_history() helpers that
# interact with the MySQL detection_history table.

import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def _get_connection():
    """Return a new PyMySQL connection to the Fake News and Review Detector database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def save_result(detection_type: str, result: str, confidence: float,
                input_text: str = None, image_filename: str = None):
    """
    Insert a detection result into detection_history.

    Args:
        detection_type: 'news', 'review', or 'image'
        result:         'REAL' or 'FAKE'
        confidence:     float percentage (0-100)
        input_text:     the text that was analysed (optional)
        image_filename: filename of the uploaded image (optional)
    """
    connection = None
    try:
        connection = _get_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO detection_history
                    (detection_type, input_text, image_filename, result, confidence)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                detection_type,
                input_text,
                image_filename,
                result,
                confidence,
            ))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"[DB] save_result error: {e}")
    finally:
        if connection:
            connection.close()


def get_history(limit: int = 50) -> list:
    """
    Fetch the most recent detection records.

    Returns:
        List of dicts from detection_history ordered by created_at DESC.
    """
    connection = None
    try:
        connection = _get_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT id, detection_type, input_text, image_filename,
                       result, confidence, created_at
                FROM detection_history
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            # Convert datetime objects to strings for JSON serialisation
            for row in rows:
                if row.get("created_at"):
                    row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            return rows
    except pymysql.MySQLError as e:
        print(f"[DB] get_history error: {e}")
        return []
    finally:
        if connection:
            connection.close()
