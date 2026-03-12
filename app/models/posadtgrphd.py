from app import db
from datetime import datetime

class RCEPosAdtGrpHd(db.Model):
    """
    Model untuk tabel RCEPosAdtGrpHd - Position Audit Group Header
    """
    __tablename__ = "RCEPosAdtGrpHd"
    __table_args__ = {'schema': 'dbo'}

    PosAdtTypeId = db.Column(db.Integer, primary_key=True)
    PosAdtType = db.Column(db.String(50))
    PosAdtName = db.Column(db.String(200))
    FgShowOnSummary = db.Column(db.String(10))
    GrpIcoFileName = db.Column(db.String(200))
    GrpIcon = db.Column(db.LargeBinary)
    FgActive = db.Column(db.String(10))
    FgStyle = db.Column(db.String(50))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))

    def __repr__(self):
        return f"<RCEPosAdtGrpHd {self.PosAdtName}>"

    def to_dict(self):
        """Convert position audit group header object to dictionary"""
        return {
            "PosAdtTypeId": self.PosAdtTypeId,
            "PosAdtType": self.PosAdtType,
            "PosAdtName": self.PosAdtName,
            "FgShowOnSummary": self.FgShowOnSummary,
            "GrpIcoFileName": self.GrpIcoFileName,
            "GrpIcon": self.GrpIcon.hex() if self.GrpIcon else None,
            "FgActive": self.FgActive,
            "FgStyle": self.FgStyle,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
        }
