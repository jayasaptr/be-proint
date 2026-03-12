from app import db
from datetime import datetime

class PMKecamatan(db.Model):
    """
    Model untuk tabel PMKecamatan - Data Kecamatan
    """
    __tablename__ = "PMKecamatan"
    __table_args__ = {'schema': 'dbo'}

    KecamatanId = db.Column(db.Integer, primary_key=True)
    CityId = db.Column(db.Integer)
    KecamatanName = db.Column(db.String(100))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgStatus = db.Column(db.String(10))
    ExportDate = db.Column(db.DateTime)

    def __repr__(self):
        return f"<PMKecamatan {self.KecamatanName}>"

    def to_dict(self):
        """Convert kecamatan object to dictionary"""
        return {
            "KecamatanId": self.KecamatanId,
            "CityId": self.CityId,
            "KecamatanName": self.KecamatanName,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgStatus": self.FgStatus,
            "ExportDate": self.ExportDate.isoformat() if self.ExportDate else None,
        }
