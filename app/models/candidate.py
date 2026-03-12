from app import db
from datetime import datetime

class RCECandidate(db.Model):
    """
    Model untuk tabel RCECandidate - Data Personal Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya
    """
    __tablename__ = "RCECandidate"
    __table_args__ = {'schema': 'dbo'}

    CanId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CanCode = db.Column(db.String(15))  # Actual: max 15 chars untuk CAN-2026-00001
    CanName = db.Column(db.String(50), nullable=False)  # Reduced: max 50 chars
    CanStatus = db.Column(db.String(3))  # Actual: max 3 chars untuk 'NEW'
    CanDateBirth = db.Column(db.Date, nullable=False)
    CanSex = db.Column(db.String(1), nullable=False)  # Actual: 1 char untuk 'M'/'F'
    CanIsFore = db.Column(db.String(1))  # Actual: 1 char untuk 'Y'/'N'
    CanMaritalStId = db.Column(db.Integer)
    CanCityBirthId = db.Column(db.Integer)
    CanCityBirthName = db.Column(db.String(50))  # Reduced: max 50 chars
    CanBloodType = db.Column(db.String(2))  # Actual: max 2 chars untuk 'A', 'B', 'AB', 'O'
    CanRaceId = db.Column(db.Integer)
    CanReligionId = db.Column(db.Integer)
    CanHeight = db.Column(db.Float)
    CanWeight = db.Column(db.Float)
    CanHandphone = db.Column(db.String(15))  # Reduced: max 15 chars
    CanEmail = db.Column(db.String(50))  # Reduced: max 50 chars
    CanCitizenId = db.Column(db.String(20))  # Reduced: max 20 chars
    CanSourceId = db.Column(db.Integer)
    CanSourceNote = db.Column(db.Text)
    CanFrontTitle = db.Column(db.String(10))  # Reduced
    CanEndTitle = db.Column(db.String(10))  # Reduced
    CanEntryDate = db.Column(db.DateTime)
    CanApplyDate = db.Column(db.DateTime)
    CanCurrId = db.Column(db.Integer)
    CanExpSal = db.Column(db.Float)
    CanExpType = db.Column(db.String(1))  # Reduced: likely 1 char flag
    CanAvailability = db.Column(db.String(10))  # Reduced
    CanAdvId = db.Column(db.Integer)
    CanOrgId = db.Column(db.Integer)
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))  # Reduced: max 15 chars untuk 'CAREER_PORTAL'
    UpdFlag = db.Column(db.String(1))  # Actual: 1 char untuk 'I'/'U'/'D'
    CanSource = db.Column(db.String(10))  # Reduced: max 10 chars untuk 'Website'
    CanNPWP = db.Column(db.String(20))  # Reduced
    CanMarriedDate = db.Column(db.Date)
    FgChanges = db.Column(db.String(1))  # Reduced: likely 1 char flag
    FgFreshGrad = db.Column(db.String(1))  # Reduced: likely 1 char flag
    CanNickName = db.Column(db.String(30))  # Reduced
    RefTypeId = db.Column(db.Integer)
    RefTypeName = db.Column(db.String(50))  # Reduced
    CanInstId = db.Column(db.Integer)
    CanInstName = db.Column(db.String(100))  # Reduced
    CanBPJSTKNo = db.Column(db.String(20))  # Reduced
    CanBPJSKesNo = db.Column(db.String(20))  # Reduced
    CanFaskesId = db.Column(db.Integer)
    CanBankAcc = db.Column(db.String(30))  # Reduced
    CanBankName = db.Column(db.String(50))  # Reduced
    CanBankId = db.Column(db.Integer)
    FgCanCategory = db.Column(db.String(1))  # Reduced: likely 1 char flag
    CanLocRecruitId = db.Column(db.Integer)
    CanBankAttach = db.Column(db.Text)
    PPhPTKP = db.Column(db.String(5))  # Reduced: max 5 chars untuk PTKP code
    CanBankAttachFile = db.Column(db.String(200))  # Reduced

    def __repr__(self):
        return f"<RCECandidate {self.CanName}>"

    def to_dict(self):
        """Convert candidate object to dictionary"""
        return {
            "CanId": self.CanId,
            "CanCode": self.CanCode,
            "CanName": self.CanName,
            "CanStatus": self.CanStatus,
            "CanDateBirth": self.CanDateBirth.isoformat() if self.CanDateBirth else None,
            "CanSex": self.CanSex,
            "CanEmail": self.CanEmail,
            "CanHandphone": self.CanHandphone,
        }


class RCECanAddr(db.Model):
    """
    Model untuk tabel RCECanAddr - Alamat Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya
    """
    __tablename__ = "RCECanAddr"
    __table_args__ = {'schema': 'dbo'}

    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), primary_key=True)
    CanResAddress = db.Column(db.Text)
    CanResCityId = db.Column(db.Integer)
    CanResCityName = db.Column(db.String(50))  # Reduced
    CanResStateName = db.Column(db.String(50))  # Reduced
    CanResZipCode = db.Column(db.String(10))  # Reduced
    CanResStatusId = db.Column(db.Integer)
    CanResStatusName = db.Column(db.String(30))  # Reduced
    CanResStart = db.Column(db.Date)
    CanResPhone = db.Column(db.String(15))  # Reduced
    CanOriAddress = db.Column(db.Text)
    CanOriCityId = db.Column(db.Integer)
    CanOriCityName = db.Column(db.String(50))  # Reduced
    CanOriStateName = db.Column(db.String(50))  # Reduced
    CanOriZipCode = db.Column(db.String(10))  # Reduced
    CanOriStatusId = db.Column(db.Integer)
    CanOriStatusName = db.Column(db.String(30))  # Reduced
    CanOriStart = db.Column(db.Date)
    CanOriPhone = db.Column(db.String(15))  # Reduced
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))  # Reduced
    UpdFlag = db.Column(db.String(1))  # Reduced
    CanResRT = db.Column(db.String(5))  # Reduced
    CanOriRT = db.Column(db.String(5))  # Reduced
    CanResRW = db.Column(db.String(5))  # Reduced
    CanOriRW = db.Column(db.String(5))  # Reduced
    CanResKecId = db.Column(db.Integer)
    CanOriKecId = db.Column(db.Integer)
    CanResDesa = db.Column(db.String(50))  # Reduced
    CanOriDesa = db.Column(db.String(50))  # Reduced
    CanOriAreaId = db.Column(db.Integer)
    CanOriAreaCode = db.Column(db.String(20))  # Reduced
    CanOriPhoneNmbr = db.Column(db.String(15))  # Reduced

    def __repr__(self):
        return f"<RCECanAddr CanId={self.CanId}>"


class RCCanEdu(db.Model):
    """
    Model untuk tabel RCECanEdu - Riwayat Pendidikan Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya
    """
    __tablename__ = "RCECanEdu"
    __table_args__ = {'schema': 'dbo'}

    CanEduId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), nullable=False)
    EduStatus = db.Column(db.String(10))  # Reduced
    EduLvlId = db.Column(db.Integer)
    EduMjrId = db.Column(db.Integer)
    EduMjrName = db.Column(db.String(100))  # Reduced
    EduInsId = db.Column(db.Integer)
    EduInsName = db.Column(db.String(100))  # Reduced
    EduCityId = db.Column(db.Integer)
    EduCityName = db.Column(db.String(50))  # Reduced
    EduGrade = db.Column(db.Float)
    EduStart = db.Column(db.Date)
    EduGraduate = db.Column(db.Date)
    EduGraduateId = db.Column(db.Integer)
    EduFrontTitle = db.Column(db.String(10))  # Reduced
    EduEndTitle = db.Column(db.String(10))  # Reduced
    FgLastEdu = db.Column(db.String(1))  # Reduced
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))  # Reduced
    UpdFlag = db.Column(db.String(1))  # Reduced
    CanEdufunded = db.Column(db.String(1))  # Reduced
    CanEduName = db.Column(db.String(100))  # Reduced
    EduPeriodStart = db.Column(db.Date)
    EduPeriodEnd = db.Column(db.Date)
    FgCertificate = db.Column(db.String(1))  # Reduced
    EduEnd = db.Column(db.Date)

    def __repr__(self):
        return f"<RCCanEdu CanId={self.CanId} Institution={self.EduInsName}>"


class CanCardId(db.Model):
    """
    Model untuk tabel RCECanIDCard - Kartu Identitas Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya
    """
    __tablename__ = "RCECanIDCard"
    __table_args__ = {'schema': 'dbo'}

    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), primary_key=True)
    CardTypeId = db.Column(db.Integer, primary_key=True)
    CardNumber = db.Column(db.String(30), nullable=False)  # Reduced
    CardPublisher = db.Column(db.String(50))  # Reduced
    CardExpired = db.Column(db.Date)
    CardFgDefault = db.Column(db.String(1))  # Reduced
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))  # Reduced
    UpdFlag = db.Column(db.String(1))  # Reduced
    Attachment = db.Column(db.Text)
    AttachFile = db.Column(db.String(200))  # Reduced

    def __repr__(self):
        return f"<CanCardId CanId={self.CanId} CardTypeId={self.CardTypeId}>"


class CanExpQuestId(db.Model):
    """
    Model untuk tabel RCECanExpQuest - Jawaban Pertanyaan Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya

    Note: CanExpId adalah FK ke RCECanExperience.CanExpId (untuk pertanyaan terkait pengalaman kerja)
          Primary key adalah composite dari (CanExpId, QuestionId)
    """
    __tablename__ = "RCECanExpQuest"
    __table_args__ = {'schema': 'dbo'}

    CanExpId = db.Column(db.Integer, db.ForeignKey('dbo.RCECanExperience.CanExpId'), primary_key=True, nullable=False)
    QuestionId = db.Column(db.Integer, primary_key=True, nullable=False)
    QuestCanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'))
    QTempId = db.Column(db.Integer)
    QTopicId = db.Column(db.Integer)
    QuestAnswer = db.Column(db.Text)
    QuestPoint = db.Column(db.Float)
    QuestRemark = db.Column(db.Text)
    FgAnsMode = db.Column(db.String(1))  # Reduced
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))  # Reduced
    UpdFlag = db.Column(db.String(1))  # Reduced
    QAnsNumeric = db.Column(db.Float)

    def __repr__(self):
        return f"<CanExpQuestId CanExpId={self.CanExpId} QuestionId={self.QuestionId}>"


class RCECanExperience(db.Model):
    """
    Model untuk tabel RCECanExperience - Pengalaman Kerja Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya

    Note: Table has database triggers, so IDs are retrieved via SELECT after INSERT
    instead of using OUTPUT clause (which conflicts with triggers)
    """
    __tablename__ = "RCECanExperience"
    __table_args__ = {'schema': 'dbo', 'implicit_returning': False}
    __mapper_args__ = {
        'eager_defaults': True
    }

    CanExpId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), nullable=False)
    CompName = db.Column(db.String(100))  # Nama perusahaan
    CompTypeId = db.Column(db.Integer)  # ID tipe perusahaan
    CompTypeName = db.Column(db.String(50))  # Nama tipe perusahaan
    CompAddress = db.Column(db.Text)  # Alamat perusahaan
    CompCityId = db.Column(db.Integer)  # ID kota perusahaan
    CompZipCode = db.Column(db.String(10))  # Kode pos
    CompPhone = db.Column(db.String(15))  # Telepon perusahaan
    JobStart = db.Column(db.Date)  # Tanggal mulai kerja
    JobEnd = db.Column(db.Date)  # Tanggal selesai kerja
    JobTitleId = db.Column(db.Integer)  # ID jabatan
    JobTtlName = db.Column(db.String(100))  # Nama jabatan
    SalaryStart = db.Column(db.Float)  # Gaji awal
    SalaryEnd = db.Column(db.Float)  # Gaji akhir
    TermReason = db.Column(db.Text)  # Alasan berhenti
    Description = db.Column(db.Text)  # Deskripsi pekerjaan
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))
    UpdFlag = db.Column(db.String(1))
    CanSeq = db.Column(db.Integer)  # Urutan pengalaman
    JobPrdMonth = db.Column(db.Integer)  # Lama kerja (bulan)
    JobPrdYear = db.Column(db.Integer)  # Lama kerja (tahun)
    TotalEmp = db.Column(db.Integer)  # Jumlah karyawan di perusahaan
    CanReportTo = db.Column(db.String(100))  # Atasan/Lapor kepada
    BusinessTypeId = db.Column(db.Integer)  # ID jenis bisnis
    BusinessType = db.Column(db.String(100))  # Jenis bisnis
    FgPresent = db.Column(db.String(1))  # Flag masih bekerja (Y/N)

    def __repr__(self):
        return f"<RCECanExperience CanId={self.CanId} CompName={self.CompName}>"


class RCECanJobExpected(db.Model):
    """
    Model untuk tabel RCECanJobExpected - Posisi yang Dilamar Kandidat
    IMPORTANT: Ukuran kolom disesuaikan dengan database SQL Server yang sebenarnya
    """
    __tablename__ = "RCECanJobExpected"
    __table_args__ = {'schema': 'dbo'}

    CanJobExpectedId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), nullable=False)
    Priority = db.Column(db.Integer)  # Prioritas posisi (1 = highest)
    JobTtlId = db.Column(db.Integer)  # ID job title
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))
    UpdFlag = db.Column(db.String(1))
    VacantId = db.Column(db.Integer)  # ID vacant position yang dilamar
    OtherJobTtlName = db.Column(db.String(100))  # Nama job title lainnya
    PositionId = db.Column(db.Integer)  # ID posisi yang dilamar
    OtherPosName = db.Column(db.String(100))  # Nama posisi lainnya
    VacantPosId = db.Column(db.Integer)  # ID vacant position yang dilamar

    def __repr__(self):
        return f"<RCECanJobExpected CanId={self.CanId} PositionId={self.PositionId}>"


class RCECanPhoto(db.Model):
    """
    Model untuk tabel RCECanPhoto - Foto Kandidat
    IMPORTANT: Foto disimpan sebagai BLOB dalam database
    """
    __tablename__ = "RCECanPhoto"
    __table_args__ = {'schema': 'dbo'}

    CanPhotoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), nullable=False)
    CanPhoto = db.Column(db.LargeBinary, nullable=False)  # BLOB untuk menyimpan foto
    FgDefault = db.Column(db.String(1))  # Flag default ('Y' untuk foto utama, 'N' untuk foto lainnya)
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))
    Updflag = db.Column(db.String(1))  # 'I' = Insert, 'U' = Update, 'D' = Delete

    def __repr__(self):
        return f"<RCECanPhoto CanPhotoId={self.CanPhotoId} CanId={self.CanId}>"


class RCECanDocument(db.Model):
    """
    Model untuk tabel RCECanDocument - Dokumen Kandidat
    IMPORTANT: Dokumen disimpan sebagai BLOB dalam database
    """
    __tablename__ = "RCECanDocument"
    __table_args__ = {'schema': 'dbo'}

    CanDocId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CanId = db.Column(db.Integer, db.ForeignKey('dbo.RCECandidate.CanId'), nullable=False)
    CanDocDesc = db.Column(db.String(200))  # Deskripsi dokumen
    CanDocFile = db.Column(db.String(200))  # Nama file asli
    CanDoc = db.Column(db.LargeBinary, nullable=False)  # BLOB untuk menyimpan dokumen
    CanDocTypeId = db.Column(db.Integer)  # ID tipe dokumen (jika ada)
    UpdDate = db.Column(db.DateTime)
    UpdUser = db.Column(db.String(15))
    UpdFlag = db.Column(db.String(1))  # 'I' = Insert, 'U' = Update, 'D' = Delete

    def __repr__(self):
        return f"<RCECanDocument CanDocId={self.CanDocId} CanId={self.CanId}>"
