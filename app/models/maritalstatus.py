from app import db
from datetime import datetime

class PMMaritalSt(db.Model):
    """
    Model untuk tabel PMMaritalStatus - Status Pernikahan
    """
    __tablename__ = "PMMaritalStatus"
    __table_args__ = {'schema': 'dbo'}

    MaritalStId = db.Column(db.Integer, primary_key=True)
    MaritalSt = db.Column(db.String(50))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgType = db.Column(db.String(10))

    def __repr__(self):
        return f"<PMMaritalSt {self.MaritalSt}>"

    def to_dict(self):
        """Convert marital status object to dictionary"""
        return {
            "MaritalStId": self.MaritalStId,
            "MaritalSt": self.MaritalSt,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgType": self.FgType,
        }
