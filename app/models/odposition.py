from app import db
from datetime import datetime

class ODPosition(db.Model):
    """
    Model untuk tabel ODPosition - Data Position
    """
    __tablename__ = "ODPosition"
    __table_args__ = {'schema': 'dbo'}

    PositionId = db.Column(db.Integer, primary_key=True)
    PosCode = db.Column(db.String(50))
    PosName = db.Column(db.String(200))
    PosLevel = db.Column(db.Integer)
    PosParent = db.Column(db.Integer)
    PosGrpId = db.Column(db.Integer)
    CompId = db.Column(db.Integer)
    OrgId = db.Column(db.Integer)
    LocationId = db.Column(db.Integer)
    JobLvlId = db.Column(db.Integer)
    JobTtlId = db.Column(db.Integer)
    FgActive = db.Column(db.String(1))
    FgStrategicPos = db.Column(db.String(1))
    CompGrpId = db.Column(db.Integer)
    InActiveBy = db.Column(db.String(50))
    ReActiveBy = db.Column(db.String(50))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(1))

    def __repr__(self):
        return f"<ODPosition {self.PosName}>"

    def to_dict(self):
        """Convert position object to dictionary"""
        return {
            "PositionId": self.PositionId,
            "PosCode": self.PosCode,
            "PosName": self.PosName,
            "PosLevel": self.PosLevel,
            "PosParent": self.PosParent,
            "PosGrpId": self.PosGrpId,
            "CompId": self.CompId,
            "OrgId": self.OrgId,
            "LocationId": self.LocationId,
            "JobLvlId": self.JobLvlId,
            "JobTtlId": self.JobTtlId,
            "FgActive": self.FgActive,
            "FgStrategicPos": self.FgStrategicPos,
            "CompGrpId": self.CompGrpId,
            "InActiveBy": self.InActiveBy,
            "ReActiveBy": self.ReActiveBy,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
        }
