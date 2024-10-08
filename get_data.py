import json
import requests
from database.connector import SessionLocal, init_db
from models.area import Area
from models.settlement import Settlement

def get_coordinates(location):
    try:
        base_url = "https://nominatim.openstreetmap.org/search"
        base_url = f"{base_url}?q={location}&format=json&addressdetails=1&limit=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "referer": "https://plex.klein.org.il",
        }
        response = requests.get(base_url, headers=headers)
        data = response.json()
        if data:
            latitude = float(data[0].get('lat'))
            longitude = float(data[0].get('lon'))
            return latitude, longitude
        return 0.0, 0.0
    except Exception as e:
        print(f"Error fetching coordinates for {location}: {str(e)}")
        return 0.0, 0.0

def populate_database(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    session = SessionLocal()
    try:
        for entry in data:
            # Check if the area exists
            area = session.query(Area).filter_by(areaid=entry['areaid']).first()
            if not area:
                area = Area(areaid=entry['areaid'], areaname=entry['areaname'])
                session.add(area)

            # Get coordinates
            latitude, longitude = get_coordinates(entry['label_he'])

            # Create the settlement entry
            settlement = Settlement(
                settlementid=int(entry['id']),
                settlementname=entry['label_he'],
                migun_time=entry['migun_time'],
                rashut=entry.get('rashut'),
                latitude=latitude,
                longitude=longitude,
                area=area
            )
            session.add(settlement)

        session.commit()
    except Exception as e:
        print(f"Error populating database: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    populate_database("areas.json")
