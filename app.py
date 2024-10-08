from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connector import SessionLocal, init_db
from models.settlement import Settlement

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/settlement/")
def get_settlement(settlement_name: str, db: Session = Depends(get_db)):
    settlement = db.query(Settlement).filter(Settlement.settlementname == settlement_name).first()
    if settlement is None:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return {
        "areaname": settlement.area.areaname,
        "settlementname": settlement.settlementname,
        "settlementid": settlement.settlementid,
        "migun_time": settlement.migun_time,
        "latitude": settlement.latitude,
        "longitude": settlement.longitude
    }

@app.delete("/settlement/{settlement_id}")
def delete_settlement(settlement_id: int, db: Session = Depends(get_db)):
    settlement = db.query(Settlement).filter(Settlement.settlementid == settlement_id).first()
    if settlement is None:
        raise HTTPException(status_code=404, detail="Settlement not found")
    db.delete(settlement)
    db.commit()
    return {"message": "Settlement deleted"}

@app.put("/settlement/{settlement_id}")
def update_settlement(settlement_id: int, settlement: Settlement, db: Session = Depends(get_db)):
    existing_settlement = db.query(Settlement).filter(Settlement.settlementid == settlement_id).first()
    if existing_settlement is None:
        raise HTTPException(status_code=404, detail="Settlement not found")

    # Update fields here
    existing_settlement.settlementname = settlement.settlementname
    existing_settlement.migun_time = settlement.migun_time
    existing_settlement.rashut = settlement.rashut
    existing_settlement.latitude = settlement.latitude
    existing_settlement.longitude = settlement.longitude

    db.commit()
    return {"message": "Settlement updated"}

@app.post("/settlement/")
def create_settlement(settlement: Settlement, db: Session = Depends(get_db)):
    db.add(settlement)
    db.commit()
    return {"message": "Settlement created"}
