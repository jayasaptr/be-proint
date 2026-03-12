from app import db
from datetime import datetime

class PMEduMajor(db.Model):
    """
    Model untuk tabel PMEduMajor - Jurusan Pendidikan
    """
    __tablename__ = "PMEduMajor"
    __table_args__ = {'schema': 'dbo'}

    EduMjrId = db.Column(db.Integer, primary_key=True)
    EduMjrCode = db.Column(db.String(50))
    EduMjrName = db.Column(db.String(100))
    MajorGrpId = db.Column(db.String(50))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgActive = db.Column(db.String(10))
    InActDate = db.Column(db.DateTime)
    InActByUserId = db.Column(db.String(50))
    InActByEmpId = db.Column(db.String(50))

    def __repr__(self):
        return f"<PMEduMajor {self.EduMjrCode} - {self.EduMjrName}>"

    def to_dict(self):
        """Convert education major object to dictionary"""
        return {
            "EduMjrId": self.EduMjrId,
            "EduMjrCode": self.EduMjrCode,
            "EduMjrName": self.EduMjrName,
            "MajorGrpId": self.MajorGrpId,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgActive": self.FgActive,
            "InActDate": self.InActDate.isoformat() if self.InActDate else None,
            "InActByUserId": self.InActByUserId,
            "InActByEmpId": self.InActByEmpId,
        }
