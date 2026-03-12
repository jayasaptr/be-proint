from app import db
from datetime import datetime

class RCQuestTopic(db.Model):
    """
    Model untuk tabel RCQuestTopic - Topic Pertanyaan
    """
    __tablename__ = "RCQuestTopic"
    __table_args__ = {'schema': 'dbo'}

    QTopicId = db.Column(db.Integer, primary_key=True)
    QTopicCode = db.Column(db.String(50))
    QTopicName = db.Column(db.String(200))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))

    # Relationship
    questions = db.relationship('RCQuestion', back_populates='topic', lazy='select')

    def __repr__(self):
        return f"<RCQuestTopic {self.QTopicCode} - {self.QTopicName}>"

    def to_dict(self, include_questions=False):
        """Convert question topic object to dictionary"""
        data = {
            "QTopicId": self.QTopicId,
            "QTopicCode": self.QTopicCode,
            "QTopicName": self.QTopicName,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
        }

        if include_questions:
            data["questions"] = [q.to_dict(include_topic=False) for q in self.questions]

        return data
