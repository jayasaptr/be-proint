from app import db
from datetime import datetime

class PMEduInstitution(db.Model):
    """
    Model untuk tabel PMEduInstitution - Institusi Pendidikan
    """
    __tablename__ = "PMEduInstitution"
    __table_args__ = {'schema': 'dbo'}

    EduInsId = db.Column(db.Integer, primary_key=True)
    EduInsCode = db.Column(db.String(50))
    EduInsName = db.Column(db.String(200))
    CityId = db.Column(db.String(50))
    EduInsAddr = db.Column(db.String(500))
    EduInsPhone = db.Column(db.String(50))
    EduInsWebSite = db.Column(db.String(200))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgActive = db.Column(db.String(10))
    InActDate = db.Column(db.DateTime)
    InActByUserId = db.Column(db.String(50))
    InActByEmpId = db.Column(db.String(50))

    def __repr__(self):
        return f"<PMEduInstitution {self.EduInsCode} - {self.EduInsName}>"

    def to_dict(self):
        """Convert education institution object to dictionary"""
        return {
            "EduInsId": self.EduInsId,
            "EduInsCode": self.EduInsCode,
            "EduInsName": self.EduInsName,
            "CityId": self.CityId,
            "EduInsAddr": self.EduInsAddr,
            "EduInsPhone": self.EduInsPhone,
            "EduInsWebSite": self.EduInsWebSite,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgActive": self.FgActive,
            "InActDate": self.InActDate.isoformat() if self.InActDate else None,
            "InActByUserId": self.InActByUserId,
            "InActByEmpId": self.InActByEmpId,
        }
