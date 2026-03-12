from app import db
from datetime import datetime

class RCEPosAdtGrpMbr(db.Model):
    """
    Model untuk tabel RCEPosAdtGrpMbr - Position Audit Group Member (Many-to-Many relationship)
    """
    __tablename__ = "RCEPosAdtGrpMbr"
    __table_args__ = {'schema': 'dbo'}

    PosAdtMbrId = db.Column(db.Integer, primary_key=True)
    PosAdtGrpId = db.Column(db.Integer, db.ForeignKey('dbo.RCEPosAdtGrpDt.PosAdtGrpId'))
    PosAdtTypeId = db.Column(db.Integer, db.ForeignKey('dbo.RCEPosAdtGrpHd.PosAdtTypeId'))
    VacantPosId = db.Column(db.Integer, db.ForeignKey('dbo.RCEVacantPos.VacantPosId'))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))

    # Relationships
    vacant_pos = db.relationship('RCEVacantPos', backref='posadt_members', lazy=True)
    posadt_grp_dt = db.relationship('RCEPosAdtGrpDt', backref='members', lazy=True)
    posadt_grp_hd = db.relationship('RCEPosAdtGrpHd', backref='members', lazy=True)

    def __repr__(self):
        return f"<RCEPosAdtGrpMbr {self.PosAdtMbrId}>"

    def to_dict(self):
        """Convert position audit group member object to dictionary"""
        return {
            "PosAdtMbrId": self.PosAdtMbrId,
            "PosAdtGrpId": self.PosAdtGrpId,
            "PosAdtTypeId": self.PosAdtTypeId,
            "VacantPosId": self.VacantPosId,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
        }
