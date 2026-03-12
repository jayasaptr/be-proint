from app import db
from datetime import datetime

class RCEVacantPos(db.Model):
    """
    Model untuk tabel RCEVacantPos - Data Vacant Position
    """
    __tablename__ = "RCEVacantPos"
    __table_args__ = {'schema': 'dbo'}

    VacantPosId = db.Column(db.Integer, primary_key=True)
    VacantPosCode = db.Column(db.String(50))
    VacantPostionId = db.Column(db.Integer)
    VacantPositionName = db.Column(db.String(200))
    VacantPosSpec = db.Column(db.Text)
    FgActive = db.Column(db.String(10))
    OrgRecId = db.Column(db.Integer)
    FgOtherPos = db.Column(db.String(10))
    VacantExpDate = db.Column(db.DateTime)
    VacantNote = db.Column(db.Text)
    FgShowVacant = db.Column(db.String(10))
    VacantCompGrpId = db.Column(db.Integer)
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    RequestNo = db.Column(db.String(50))

    def __repr__(self):
        return f"<RCEVacantPos {self.VacantPositionName}>"

    def to_dict(self, include_relations=False):
        """Convert vacant position object to dictionary"""
        result = {
            "VacantPosId": self.VacantPosId,
            "VacantPosCode": self.VacantPosCode,
            "VacantPostionId": self.VacantPostionId,
            "VacantPositionName": self.VacantPositionName,
            "VacantPosSpec": self.VacantPosSpec,
            "FgActive": self.FgActive,
            "OrgRecId": self.OrgRecId,
            "FgOtherPos": self.FgOtherPos,
            "VacantExpDate": self.VacantExpDate.isoformat() if self.VacantExpDate else None,
            "VacantNote": self.VacantNote,
            "FgShowVacant": self.FgShowVacant,
            "VacantCompGrpId": self.VacantCompGrpId,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "RequestNo": self.RequestNo,
        }

        # Include related position audit group data if requested
        if include_relations and hasattr(self, 'posadt_members') and self.posadt_members:
            result["PosAdtGroups"] = []
            for member in self.posadt_members:
                group_data = {
                    "PosAdtMbrId": member.PosAdtMbrId,
                    "PosAdtGrpId": member.PosAdtGrpId,
                    "PosAdtTypeId": member.PosAdtTypeId,
                }

                # Add PosAdtGrpDt data
                if member.posadt_grp_dt:
                    group_data["PosAdtGrpCode"] = member.posadt_grp_dt.PosAdtGrpCode
                    group_data["PosAdtGrpName"] = member.posadt_grp_dt.PosAdtGrpName

                # Add PosAdtGrpHd data
                if member.posadt_grp_hd:
                    group_data["PosAdtType"] = member.posadt_grp_hd.PosAdtType
                    group_data["PosAdtName"] = member.posadt_grp_hd.PosAdtName
                    group_data["FgShowOnSummary"] = member.posadt_grp_hd.FgShowOnSummary

                result["PosAdtGroups"].append(group_data)

        return result
