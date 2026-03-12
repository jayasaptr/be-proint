from app import db
from datetime import datetime

class PMState(db.Model):
    """
    Model untuk tabel PMState - Data Provinsi
    """
    __tablename__ = "PMState"
    __table_args__ = {'schema': 'dbo'}

    StateId = db.Column(db.Integer, primary_key=True)
    CountryId = db.Column(db.Integer)
    StateCode = db.Column(db.String(50))
    StateName = db.Column(db.String(100))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgStatus = db.Column(db.String(10))

    def __repr__(self):
        return f"<PMState {self.StateName}>"

    def to_dict(self):
        """Convert state object to dictionary"""
        return {
            "StateId": self.StateId,
            "CountryId": self.CountryId,
            "StateCode": self.StateCode,
            "StateName": self.StateName,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgStatus": self.FgStatus,
        }
