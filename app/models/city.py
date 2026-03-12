from app import db
from datetime import datetime

class PMCity(db.Model):
    """
    Model untuk tabel PMCity - Data Kota
    """
    __tablename__ = "PMCity"
    __table_args__ = {'schema': 'dbo'}

    CityId = db.Column(db.Integer, primary_key=True)
    CityCode = db.Column(db.String(50))
    CityName = db.Column(db.String(100))
    CityStateId = db.Column(db.Integer)
    CityCountryId = db.Column(db.Integer)
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgStatus = db.Column(db.String(10))

    def __repr__(self):
        return f"<PMCity {self.CityName}>"

    def to_dict(self):
        """Convert city object to dictionary"""
        return {
            "CityId": self.CityId,
            "CityCode": self.CityCode,
            "CityName": self.CityName,
            "CityStateId": self.CityStateId,
            "CityCountryId": self.CityCountryId,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgStatus": self.FgStatus,
        }
