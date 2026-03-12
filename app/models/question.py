from app import db
from datetime import datetime

class RCQuestion(db.Model):
    """
    Model untuk tabel RCQuestion - Pertanyaan
    """
    __tablename__ = "RCQuestion"
    __table_args__ = {'schema': 'dbo'}

    QuestionId = db.Column(db.Integer, primary_key=True)
    QTopicId = db.Column(db.Integer, db.ForeignKey('dbo.RCQuestTopic.QTopicId'))
    QuestCode = db.Column(db.String(50))
    QuestName = db.Column(db.String(500))
    FgAnsMode = db.Column(db.String(10))
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(50))
    UpdFlag = db.Column(db.String(10))
    QuestRow = db.Column(db.Integer)

    # Relationship
    topic = db.relationship('RCQuestTopic', back_populates='questions', lazy='joined')

    def __repr__(self):
        return f"<RCQuestion {self.QuestCode} - {self.QuestName}>"

    def to_dict(self, include_topic=True):
        """Convert question object to dictionary"""
        data = {
            "QuestionId": self.QuestionId,
            "QTopicId": self.QTopicId,
            "QuestCode": self.QuestCode,
            "QuestName": self.QuestName,
            "FgAnsMode": self.FgAnsMode,
            "UpdDate": self.UpdDate.isoformat() if self.UpdDate else None,
            "UpdUser": self.UpdUser,
            "UpdFlag": self.UpdFlag,
            "QuestRow": self.QuestRow,
        }

        if include_topic and self.topic:
            data["topic"] = self.topic.to_dict(include_questions=False)

        return data
