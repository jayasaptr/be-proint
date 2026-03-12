from app import db
from datetime import datetime

class PMReligion(db.Model):
    """
    Model untuk tabel PMReligion - Data Agama
    """
    __tablename__ = "PMReligion"
    __table_args__ = {'schema': 'dbo'}

    ReligionId = db.Column(db.Integer, primary_key=True)
    Religion = db.Column(db.String(100))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    ExportDate = db.Column(db.DateTime)

    def __repr__(self):
        return f"<PMReligion {self.Religion}>"

    def to_dict(self):
        """Convert religion object to dictionary"""
        return {
            "ReligionId": self.ReligionId,
            "Religion": self.Religion,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "ExportDate": self.ExportDate.isoformat() if self.ExportDate else None,
        }
