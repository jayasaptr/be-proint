from app import db
from datetime import datetime

class ODJobTitle(db.Model):
    """
    Model untuk tabel ODJobTitle - Data Job Title
    """
    __tablename__ = "ODJobTitle"
    __table_args__ = {'schema': 'dbo'}

    JobTtlId = db.Column(db.Integer, primary_key=True, autoincrement=False)
    JobTtlCode = db.Column(db.String(50))
    JobTtlName = db.Column(db.String(200))
    JobTtlAlias = db.Column(db.String(200))
    JobTtlOrgId = db.Column(db.Integer)
    JobTtlLvlId = db.Column(db.Integer)
    JobTtlGrpId = db.Column(db.Integer)
    JobTtlParentId = db.Column(db.Integer)
    JobTtlValue = db.Column(db.String(50))
    JobLvlTopId = db.Column(db.Integer)
    StartLvlId = db.Column(db.Integer)
    JobTtlCompGrpId = db.Column(db.Integer)
    ActDate = db.Column(db.DateTime)
    InActDate = db.Column(db.DateTime)
    Initiator = db.Column(db.String(50))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    JobTtlReqId = db.Column(db.Integer)
    JobTtlDesc = db.Column(db.String(500))
    ExportDate = db.Column(db.DateTime)
    FgJobTtlFPK = db.Column(db.String(10))
    MaxEmpTypeLvl = db.Column(db.Integer)

    def __repr__(self):
        return f"<ODJobTitle {self.JobTtlId}: {self.JobTtlName}>"

    def to_dict(self):
        """Convert job title object to dictionary"""
        return {
            "JobTtlId": self.JobTtlId,
            "JobTtlCode": self.JobTtlCode,
            "JobTtlName": self.JobTtlName,
            "JobTtlAlias": self.JobTtlAlias,
            "JobTtlOrgId": self.JobTtlOrgId,
            "JobTtlLvlId": self.JobTtlLvlId,
            "JobTtlGrpId": self.JobTtlGrpId,
            "JobTtlParentId": self.JobTtlParentId,
            "JobTtlValue": self.JobTtlValue,
            "JobLvlTopId": self.JobLvlTopId,
            "StartLvlId": self.StartLvlId,
            "JobTtlCompGrpId": self.JobTtlCompGrpId,
            "ActDate": self.ActDate.isoformat() if self.ActDate else None,
            "InActDate": self.InActDate.isoformat() if self.InActDate else None,
            "Initiator": self.Initiator,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "JobTtlReqId": self.JobTtlReqId,
            "JobTtlDesc": self.JobTtlDesc,
            "ExportDate": self.ExportDate.isoformat() if self.ExportDate else None,
            "FgJobTtlFPK": self.FgJobTtlFPK,
            "MaxEmpTypeLvl": self.MaxEmpTypeLvl
        }
