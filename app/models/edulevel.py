from app import db
from datetime import datetime

class PMEduLevel(db.Model):
    """
    Model untuk tabel PMEduLevel - Jenjang Pendidikan
    """
    __tablename__ = "PMEduLevel"
    __table_args__ = {'schema': 'dbo'}

    EduLvlId = db.Column(db.Integer, primary_key=True)
    EduLvlCode = db.Column(db.String(50))
    EduLvlName = db.Column(db.String(100))
    EduLvlStatus = db.Column(db.String(20))
    EduLevel = db.Column(db.Integer)
    EduParent = db.Column(db.String(50))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgRpt = db.Column(db.String(10))
    FgSeq = db.Column(db.Integer)
    FgActive = db.Column(db.String(10))
    InActDate = db.Column(db.DateTime)
    InActByUserId = db.Column(db.String(50))
    InActByEmpId = db.Column(db.String(50))

    def __repr__(self):
        return f"<PMEduLevel {self.EduLvlCode} - {self.EduLvlName}>"

    def to_dict(self):
        """Convert education level object to dictionary"""
        return {
            "EduLvlId": self.EduLvlId,
            "EduLvlCode": self.EduLvlCode,
            "EduLvlName": self.EduLvlName,
            "EduLvlStatus": self.EduLvlStatus,
            "EduLevel": self.EduLevel,
            "EduParent": self.EduParent,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgRpt": self.FgRpt,
            "FgSeq": self.FgSeq,
            "FgActive": self.FgActive,
            "InActDate": self.InActDate.isoformat() if self.InActDate else None,
            "InActByUserId": self.InActByUserId,
            "InActByEmpId": self.InActByEmpId,
        }
