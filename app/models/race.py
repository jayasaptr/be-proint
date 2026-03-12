from app import db
from datetime import datetime

class PMRace(db.Model):
    """
    Model untuk tabel PMRace - Data Suku
    """
    __tablename__ = "PMRace"
    __table_args__ = {'schema': 'dbo'}

    RaceId = db.Column(db.Integer, primary_key=True)
    Race = db.Column(db.String(100))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))

    def __repr__(self):
        return f"<PMRace {self.Race}>"

    def to_dict(self):
        """Convert race object to dictionary"""
        return {
            "RaceId": self.RaceId,
            "Race": self.Race,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
        }
