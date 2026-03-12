from app import db
from datetime import datetime

class PMCardType(db.Model):
    """
    Model untuk tabel PMCardType - Data Tipe Kartu
    """
    __tablename__ = "PMCardType"
    __table_args__ = {'schema': 'dbo'}

    CardTypeId = db.Column(db.Integer, primary_key=True)
    CardType = db.Column(db.String(100))
    FgCardCan = db.Column(db.String(10))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgDefaultERec = db.Column(db.String(10))
    FgNoExpiry = db.Column(db.String(10))
    FgRpt = db.Column(db.String(10))

    def __repr__(self):
        return f"<PMCardType {self.CardType}>"

    def to_dict(self):
        """Convert card type object to dictionary"""
        return {
            "CardTypeId": self.CardTypeId,
            "CardType": self.CardType,
            "FgCardCan": self.FgCardCan,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgDefaultERec": self.FgDefaultERec,
            "FgNoExpiry": self.FgNoExpiry,
            "FgRpt": self.FgRpt,
        }
