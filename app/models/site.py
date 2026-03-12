from app import db
from datetime import datetime

class RCOrgRecMs(db.Model):
    """
    Model untuk tabel RCOrgRecMs - Data Site
    """
    __tablename__ = "RCOrgRecMs"
    __table_args__ = {'schema': 'dbo'}

    OrgRecId = db.Column(db.Integer, primary_key=True)
    OrgRecCode = db.Column(db.String(50))
    OrgRecName = db.Column(db.String(100))
    FgStatus = db.Column(db.String(10))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    FgDefault = db.Column(db.String(10))
    FgPosition = db.Column(db.String(10))
    FgJobTtl = db.Column(db.String(10))
    FgOrg = db.Column(db.String(10))
    FgJobLvl = db.Column(db.String(10))
    FgLoc = db.Column(db.String(10))
    FgComp = db.Column(db.String(10))

    def __repr__(self):
        return f"<RCOrgRecMs {self.OrgRecName}>"

    def to_dict(self):
        """Convert site object to dictionary"""
        return {
            "OrgRecId": self.OrgRecId,
            "OrgRecCode": self.OrgRecCode,
            "OrgRecName": self.OrgRecName,
            "FgStatus": self.FgStatus,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "FgDefault": self.FgDefault,
            "FgPosition": self.FgPosition,
            "FgJobTtl": self.FgJobTtl,
            "FgOrg": self.FgOrg,
            "FgJobLvl": self.FgJobLvl,
            "FgLoc": self.FgLoc,
            "FgComp": self.FgComp,
        }
