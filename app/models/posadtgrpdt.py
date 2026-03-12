from app import db
from datetime import datetime

class RCEPosAdtGrpDt(db.Model):
    """
    Model untuk tabel RCEPosAdtGrpDt - Position Audit Group Detail
    """
    __tablename__ = "RCEPosAdtGrpDt"
    __table_args__ = {'schema': 'dbo'}

    PosAdtGrpId = db.Column(db.Integer, primary_key=True)
    PosAdtTypeId = db.Column(db.Integer, db.ForeignKey('dbo.RCEPosAdtGrpHd.PosAdtTypeId'))
    PosAdtGrpCode = db.Column(db.String(50))
    PosAdtGrpName = db.Column(db.String(200))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))

    # Relationship to RCEPosAdtGrpHd
    posadt_grp_hd = db.relationship('RCEPosAdtGrpHd', backref='posadt_grp_details', lazy=True)

    def __repr__(self):
        return f"<RCEPosAdtGrpDt {self.PosAdtGrpName}>"

    def to_dict(self, include_header=False):
        """Convert position audit group detail object to dictionary"""
        result = {
            "PosAdtGrpId": self.PosAdtGrpId,
            "PosAdtTypeId": self.PosAdtTypeId,
            "PosAdtGrpCode": self.PosAdtGrpCode,
            "PosAdtGrpName": self.PosAdtGrpName,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
        }

        # Include related header data if requested
        if include_header and self.posadt_grp_hd:
            result["PosAdtGrpHd"] = {
                "PosAdtTypeId": self.posadt_grp_hd.PosAdtTypeId,
                "PosAdtType": self.posadt_grp_hd.PosAdtType,
                "PosAdtName": self.posadt_grp_hd.PosAdtName,
                "FgShowOnSummary": self.posadt_grp_hd.FgShowOnSummary,
                "FgActive": self.posadt_grp_hd.FgActive,
                "FgStyle": self.posadt_grp_hd.FgStyle,
            }

        return result
