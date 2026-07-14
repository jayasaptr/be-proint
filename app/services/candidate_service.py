from app import db
from app.models.candidate import RCECandidate, RCECanAddr, RCCanEdu, CanCardId, CanExpQuestId, RCECanExperience, RCECanJobExpected, RCECanPhoto, RCECanDocument
from app.models.maritalstatus import PMMaritalSt
from app.models.city import PMCity
from app.models.state import PMState
from app.models.race import PMRace
from app.models.cardtype import PMCardType
from app.models.edulevel import PMEduLevel
from app.models.eduinstitution import PMEduInstitution
from app.models.question import RCQuestion
from app.models.vacantpos import RCEVacantPos
from app.models.odposition import ODPosition
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
import json
import requests

class CandidateService:
    """Service layer untuk mengelola Candidate submission"""

    @staticmethod
    def safe_string(value, max_length):
        """
        Safely truncate string to max length

        Args:
            value: String value to truncate
            max_length (int): Maximum length

        Returns:
            str: Truncated string or None
        """
        if value is None:
            return None
        str_value = str(value).strip()
        if len(str_value) > max_length:
            print(f"Warning: Truncating string from {len(str_value)} to {max_length} chars: {str_value[:50]}...")
            return str_value[:max_length]
        return str_value if str_value else None

    @staticmethod
    def log_model_fields(model_instance, model_name):
        """
        Log all string fields and their lengths for debugging truncation errors

        Args:
            model_instance: SQLAlchemy model instance
            model_name (str): Name of the model for logging
        """
        print(f"\n=== Debugging {model_name} field lengths ===")
        for column in model_instance.__table__.columns:
            value = getattr(model_instance, column.name, None)
            if value is not None and isinstance(value, str):
                col_type = str(column.type)
                print(f"  {column.name}: '{value}' (len={len(value)}, type={col_type})")
        print(f"=== End {model_name} debug ===\n")

    @staticmethod
    def generate_candidate_code():
        """Generate unique candidate code: YYMM.NNNNN"""
        year_month = datetime.now().strftime("%y%m")

        # Get the latest candidate for this year-month
        latest = RCECandidate.query.filter(
            RCECandidate.CanCode.like(f'{year_month}.%')
        ).order_by(RCECandidate.CanId.desc()).first()

        if latest and latest.CanCode:
            # Extract sequence number and increment
            try:
                last_sequence = int(latest.CanCode.split('.')[-1])
                new_sequence = last_sequence + 1
            except:
                new_sequence = 1
        else:
            new_sequence = 1

        return f"{year_month}.{new_sequence:05d}"

    @staticmethod
    def captcha_enabled():
        """
        Feature flag to enable/disable captcha verification.

        Controlled by CAPTCHA_ENABLED in .env (default: true so behavior stays
        secure if the flag is missing). Set to false to temporarily hide the
        captcha function without removing any code.

        Returns:
            bool: True if captcha is enabled, False if disabled
        """
        return os.getenv('CAPTCHA_ENABLED', 'true').strip().lower() in ('true', '1', 'yes')

    @staticmethod
    def verify_captcha(token, secret_key=None):
        """
        Verify Cloudflare Turnstile captcha token

        Args:
            token (str): Captcha token from frontend
            secret_key (str): Cloudflare Turnstile secret key

        Returns:
            bool: True if valid, False otherwise
        """
        # Captcha disabled via feature flag — skip verification entirely
        if not CandidateService.captcha_enabled():
            return True

        if not secret_key:
            # Get from environment or config
            secret_key = os.getenv('TURNSTILE_SECRET_KEY', '')

        if not secret_key:
            # Skip verification if no secret key configured
            return True

        try:
            response = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': secret_key,
                    'response': token
                },
                timeout=5
            )
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            print(f"Captcha verification error: {str(e)}")
            # On error, allow submission (fail open) or fail closed based on preference
            return True  # Change to False for fail-closed behavior

    @staticmethod
    def resolve_city_name(city_id):
        """Resolve city ID to name"""
        if not city_id:
            return None
        city = PMCity.query.filter_by(CityId=city_id).first()
        return city.CityName if city else None

    @staticmethod
    def resolve_state_name(state_id):
        """Resolve state/province ID to name"""
        if not state_id:
            return None
        state = PMState.query.filter_by(StateId=state_id).first()
        return state.StateName if state else None

    @staticmethod
    def resolve_edu_institution_name(edu_ins_id):
        """Resolve education institution ID to name"""
        if not edu_ins_id:
            return None
        institution = PMEduInstitution.query.filter_by(EduInsId=edu_ins_id).first()
        return institution.EduInsName if institution else None

    @staticmethod
    def check_duplicate_email(email):
        """Check if email already exists (for any job application)"""
        return RCECandidate.query.filter_by(CanEmail=email).first() is not None

    @staticmethod
    def check_duplicate_identity(identity_number):
        """Check if identity number already exists (for any job application)"""
        return CanCardId.query.filter_by(CardNumber=identity_number).first() is not None

    @staticmethod
    def check_duplicate_application(email, job_id):
        """
        Check if candidate with this email already applied to this specific job

        Args:
            email (str): Candidate email
            job_id (int): Job/vacancy ID

        Returns:
            bool: True if already applied, False otherwise
        """
        return RCECandidate.query.filter_by(
            CanEmail=email,
            CanAdvId=job_id
        ).first() is not None

    @staticmethod
    def save_file(file, upload_folder='uploads'):
        """
        Save uploaded file to storage

        Args:
            file: FileStorage object
            upload_folder: Folder to save files

        Returns:
            str: Saved file path
        """
        if not file:
            return None

        # Create upload folder if not exists
        os.makedirs(upload_folder, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        unique_filename = f"{timestamp}_{filename}"

        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        return file_path

    @staticmethod
    def submit_candidate(form_data, files):
        """
        Submit candidate application

        Args:
            form_data (dict): Form data from request
            files (dict): Files from request

        Returns:
            tuple: (success: bool, message: str, data: dict, status_code: int)
        """
        try:
            # 1. Validate captcha
            captcha_token = form_data.get('captcha_token')
            if captcha_token:
                if not CandidateService.verify_captcha(captcha_token):
                    return False, "Captcha verification failed", None, 400

            # 2. Validate required fields (updated field names to match API spec)
            required_fields = ['full_name', 'email', 'gender', 'birth_city_id',
                             'date_of_birth', 'marital_status_id', 'mobile_phone',
                             'id_card_address', 'province_id', 'city_id', 'zip_code',
                             'job_id', 'is_declared_true']

            errors = {}
            for field in required_fields:
                value = form_data.get(field)
                if value is None or (isinstance(value, str) and not value.strip()):
                    errors[field] = [f"{field} wajib diisi"]

            if errors:
                return False, "Gagal mengirim lamaran", {"errors": errors}, 422

            # 3. Check duplicate application (same email + same job)
            email = form_data.get('email')
            job_id = form_data.get('job_id')

            if CandidateService.check_duplicate_application(email, job_id):
                return False, "Anda sudah pernah melamar posisi ini", {
                    "errors": {"email": ["Anda sudah pernah melamar posisi ini dengan email yang sama"]}
                }, 422

            # 4. Parse JSON fields
            try:
                identities = json.loads(form_data.get('identities', '[]'))
                educations = json.loads(form_data.get('educations', '[]'))
                experiences = json.loads(form_data.get('experiences', '[]'))
                answers = json.loads(form_data.get('answers', '[]'))
            except json.JSONDecodeError as e:
                return False, "Invalid JSON format in nested fields", {"errors": {"json": [str(e)]}}, 422

            # 5. Start transaction
            db.session.begin_nested()

            try:
                # 6. Get IDs from form (frontend now sends IDs directly)
                marital_status_id = int(form_data.get('marital_status_id')) if form_data.get('marital_status_id') else None
                birth_city_id = int(form_data.get('birth_city_id')) if form_data.get('birth_city_id') else None
                city_id = int(form_data.get('city_id')) if form_data.get('city_id') else None
                province_id = int(form_data.get('province_id')) if form_data.get('province_id') else None
                race_id = int(form_data.get('race_id')) if form_data.get('race_id') else None

                # 7. Resolve names from IDs for name columns
                city_name = CandidateService.resolve_city_name(city_id)
                state_name = CandidateService.resolve_state_name(province_id)

                # 8. Query VacantPos to get OrgRecId for CanOrgId
                vacant_pos = RCEVacantPos.query.filter_by(VacantPosId=int(job_id)).first()
                if not vacant_pos:
                    raise ValueError(f"Vacant position with ID {job_id} not found")

                org_rec_id = vacant_pos.OrgRecId

                # 9. Generate candidate code
                can_code = CandidateService.generate_candidate_code()

                # 10. Create RCECandidate with safe string truncation
                now = datetime.now()
                candidate = RCECandidate(
                    CanCode=CandidateService.safe_string(can_code, 15),  # YYMM.NNNNN format
                    CanName=CandidateService.safe_string(form_data.get('full_name'), 50),
                    CanStatus=None,  # Set to NULL as per requirement
                    CanDateBirth=datetime.strptime(form_data.get('date_of_birth'), '%Y-%m-%d').date(),
                    CanSex=CandidateService.safe_string(form_data.get('gender'), 1),  # 'M' or 'F'
                    CanIsFore=CandidateService.safe_string('N', 1),  # Default: Not foreigner
                    CanMaritalStId=marital_status_id,
                    CanCityBirthId=birth_city_id,
                    CanCityBirthName=None,  # Set to NULL as per requirement
                    CanBloodType=CandidateService.safe_string(form_data.get('blood_type'), 2) if form_data.get('blood_type') else None,
                    CanRaceId=race_id,
                    CanHandphone=CandidateService.safe_string(form_data.get('mobile_phone'), 15),
                    CanEmail=CandidateService.safe_string(form_data.get('email'), 50),
                    CanEntryDate=now,
                    CanApplyDate=now,
                    CanAdvId=int(job_id),
                    CanOrgId=org_rec_id,  # Set from RCEVacantPos.OrgRecId
                    CanSource=None,  # Set to NULL as per requirement
                    UpdDate=now,
                    UpdUser=CandidateService.safe_string(can_code, 15),  # Use candidate_code
                    UpdFlag=CandidateService.safe_string('I', 1)
                )

                # Debug: Log all field lengths before insert
                CandidateService.log_model_fields(candidate, "RCECandidate")

                db.session.add(candidate)
                db.session.flush()  # Get CanId

                # Handle photo upload - Save as BLOB in RCECanPhoto table
                if 'photo' in files and files['photo'] and files['photo'].filename:
                    photo_file = files['photo']
                    # Read photo as binary data
                    photo_binary = photo_file.read()

                    # Create RCECanPhoto record
                    can_photo = RCECanPhoto(
                        CanId=candidate.CanId,
                        CanPhoto=photo_binary,
                        FgDefault=CandidateService.safe_string('Y', 1),  # Set as default photo
                        UpdDate=now,
                        UpdUser=CandidateService.safe_string(can_code, 15),
                        Updflag=CandidateService.safe_string('I', 1)
                    )
                    db.session.add(can_photo)

                # 10. Create RCECanAddr with safe string truncation
                can_addr = RCECanAddr(
                    CanId=candidate.CanId,
                    CanResAddress=form_data.get('id_card_address'),  # Text field
                    CanResCityId=city_id,
                    CanResCityName=CandidateService.safe_string(city_name, 50),
                    CanResStateName=CandidateService.safe_string(state_name, 50),
                    CanResZipCode=CandidateService.safe_string(form_data.get('zip_code'), 10),
                    CanResPhone=CandidateService.safe_string(form_data.get('mobile_phone'), 15),
                    # Copy to origin address (alamat asal = alamat KTP)
                    CanOriAddress=form_data.get('id_card_address'),
                    CanOriCityId=city_id,
                    CanOriCityName=CandidateService.safe_string(city_name, 50),
                    CanOriStateName=CandidateService.safe_string(state_name, 50),
                    CanOriZipCode=CandidateService.safe_string(form_data.get('zip_code'), 10),
                    UpdDate=now,
                    UpdUser=CandidateService.safe_string(can_code, 15),  # Use candidate_code
                    UpdFlag=CandidateService.safe_string('I', 1)
                )
                db.session.add(can_addr)

                # 11. Create RCECanEdu (multiple) with safe string truncation
                for edu in educations:
                    # Frontend sends edu_level_id and edu_institution_id as integers
                    edu_level_id = int(edu.get('edu_level_id')) if edu.get('edu_level_id') else None
                    edu_ins_id = edu.get('edu_institution_id')

                    # edu_institution_id can be integer (from dropdown) or string (manual input)
                    if edu_ins_id:
                        try:
                            edu_ins_id = int(edu_ins_id)
                        except (ValueError, TypeError):
                            # Manual input (string) - store as ID = None
                            edu_ins_id = None

                    can_edu = RCCanEdu(
                        CanId=candidate.CanId,
                        EduStatus=CandidateService.safe_string('F', 10),  # Set to 'F'
                        EduLvlId=edu_level_id,
                        EduMjrName=CandidateService.safe_string(edu.get('major'), 100),
                        EduInsId=edu_ins_id,
                        EduInsName=None,  # Set to NULL as per requirement
                        EduGrade=float(edu.get('gpa')) if edu.get('gpa') else None,
                        FgLastEdu=CandidateService.safe_string('Y' if edu.get('is_last_education') else 'N', 1),
                        UpdDate=now,
                        UpdUser=CandidateService.safe_string(can_code, 15),  # Use candidate_code
                        UpdFlag=CandidateService.safe_string('I', 1)
                    )
                    db.session.add(can_edu)

                # 12. Create RCECanIDCard (multiple) with safe string truncation
                for idx, identity in enumerate(identities):
                    # Frontend sends card_type_id as integer
                    card_type_id = int(identity.get('card_type_id')) if identity.get('card_type_id') else None

                    if card_type_id:
                        can_card = CanCardId(
                            CanId=candidate.CanId,
                            CardTypeId=card_type_id,
                            CardNumber=CandidateService.safe_string(identity.get('number'), 30),
                            CardFgDefault=CandidateService.safe_string('Y' if idx == 0 else 'N', 1),
                            UpdDate=now,
                            UpdUser=CandidateService.safe_string(can_code, 15),  # Use candidate_code
                            UpdFlag=CandidateService.safe_string('I', 1)
                        )
                        db.session.add(can_card)

                # 12.1. Create RCECanJobExpected - Posisi yang dilamar
                # Use vacant_pos from earlier query (Step 8)
                # Query ODPosition to get PositionId using VacantPosCode
                position = ODPosition.query.filter_by(PosCode=vacant_pos.VacantPosCode).first()
                if not position:
                    raise ValueError(f"Position with PosCode {vacant_pos.VacantPosCode} not found")

                can_job_expected = RCECanJobExpected(
                    CanId=candidate.CanId,
                    Priority=1,  # Set priority to 1 (highest)
                    PositionId=position.PositionId,  # PositionId dari ODPosition
                    VacantId=None,  # VacantId di-set NULL
                    VacantPosId=int(job_id),  # VacantPosId dari job_id
                    UpdDate=now,
                    UpdUser=CandidateService.safe_string(can_code, 15),  # Use candidate_code
                    UpdFlag=CandidateService.safe_string('I', 1)  # Insert flag
                )
                db.session.add(can_job_expected)

                # 13. Create RCECanExperience (multiple) for work experiences - MOVED BEFORE QUESTIONS
                # This must be done first because RCECanExpQuest requires CanExpId from experiences
                experience_ids = []  # Store created experience IDs
                for idx, exp in enumerate(experiences):
                    company_name = exp.get('company_name')
                    position = exp.get('position')

                    # Skip if no company name or position
                    if not company_name or not position:
                        continue

                    # Parse job period
                    job_start = None
                    job_end = None
                    job_period_year = exp.get('job_period_year')  # Format: "2020 - 2022" or "2020"
                    job_period_month = exp.get('job_period_month')  # Optional: total months worked
                    job_prd_year = None
                    job_prd_month = None

                    if job_period_year:
                        try:
                            # Try to parse period like "2020 - 2022"
                            if ' - ' in str(job_period_year):
                                start_year, end_year = str(job_period_year).split(' - ')
                                job_start = datetime(int(start_year.strip()), 1, 1).date()
                                job_end = datetime(int(end_year.strip()), 12, 31).date()
                                # Calculate years
                                job_prd_year = int(end_year.strip()) - int(start_year.strip())
                            elif '-' in str(job_period_year):
                                start_year, end_year = str(job_period_year).split('-')
                                job_start = datetime(int(start_year.strip()), 1, 1).date()
                                job_end = datetime(int(end_year.strip()), 12, 31).date()
                                # Calculate years
                                job_prd_year = int(end_year.strip()) - int(start_year.strip())
                            else:
                                # Single year
                                year = int(str(job_period_year).strip())
                                job_start = datetime(year, 1, 1).date()
                        except (ValueError, TypeError, AttributeError):
                            pass

                    # Parse specific start/end dates if provided
                    if exp.get('job_start'):
                        try:
                            job_start = datetime.strptime(exp.get('job_start'), '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            pass

                    if exp.get('job_end'):
                        try:
                            job_end = datetime.strptime(exp.get('job_end'), '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            pass

                    # Parse job period if provided directly
                    if exp.get('job_prd_year'):
                        try:
                            job_prd_year = int(exp.get('job_prd_year'))
                        except (ValueError, TypeError):
                            pass

                    if exp.get('job_prd_month'):
                        try:
                            job_prd_month = int(exp.get('job_prd_month'))
                        except (ValueError, TypeError):
                            pass

                    # Determine if still working (present)
                    fg_present = 'N'
                    if exp.get('is_present') or exp.get('fg_present'):
                        fg_present = 'Y'
                        job_end = None  # Clear end date if still working

                    # Parse salary
                    salary_start = None
                    salary_end = None
                    if exp.get('salary'):
                        try:
                            salary_end = float(exp.get('salary'))
                        except (ValueError, TypeError):
                            pass

                    if exp.get('salary_start'):
                        try:
                            salary_start = float(exp.get('salary_start'))
                        except (ValueError, TypeError):
                            pass

                    if exp.get('salary_end'):
                        try:
                            salary_end = float(exp.get('salary_end'))
                        except (ValueError, TypeError):
                            pass

                    # Parse other fields
                    job_title_id = None
                    if exp.get('job_title_id'):
                        try:
                            job_title_id = int(exp.get('job_title_id'))
                        except (ValueError, TypeError):
                            pass

                    comp_type_id = None
                    if exp.get('comp_type_id'):
                        try:
                            comp_type_id = int(exp.get('comp_type_id'))
                        except (ValueError, TypeError):
                            pass

                    comp_city_id = None
                    if exp.get('comp_city_id'):
                        try:
                            comp_city_id = int(exp.get('comp_city_id'))
                        except (ValueError, TypeError):
                            pass

                    business_type_id = None
                    if exp.get('business_type_id'):
                        try:
                            business_type_id = int(exp.get('business_type_id'))
                        except (ValueError, TypeError):
                            pass

                    total_emp = None
                    if exp.get('total_emp'):
                        try:
                            total_emp = int(exp.get('total_emp'))
                        except (ValueError, TypeError):
                            pass

                    can_experience = RCECanExperience(
                        CanId=candidate.CanId,
                        CompName=CandidateService.safe_string(company_name, 100),
                        CompTypeId=comp_type_id,
                        CompTypeName=CandidateService.safe_string(exp.get('comp_type_name'), 50),
                        CompAddress=exp.get('comp_address'),  # Text field
                        CompCityId=comp_city_id,
                        CompZipCode=CandidateService.safe_string(exp.get('comp_zip_code'), 10),
                        CompPhone=CandidateService.safe_string(exp.get('comp_phone'), 15),
                        JobStart=job_start,
                        JobEnd=job_end,
                        JobTitleId=job_title_id,
                        JobTtlName=CandidateService.safe_string(position, 100),
                        SalaryStart=salary_start,
                        SalaryEnd=salary_end,
                        TermReason=exp.get('term_reason'),  # Text field
                        Description=exp.get('description'),  # Text field
                        UpdDate=now,
                        UpdUser=CandidateService.safe_string(can_code, 15),
                        UpdFlag=CandidateService.safe_string('I', 1),
                        CanSeq=idx + 1,  # Sequence number
                        JobPrdMonth=job_prd_month,
                        JobPrdYear=job_prd_year,
                        TotalEmp=total_emp,
                        CanReportTo=CandidateService.safe_string(exp.get('can_report_to'), 100),
                        BusinessTypeId=business_type_id,
                        BusinessType=CandidateService.safe_string(exp.get('business_type'), 100),
                        FgPresent=CandidateService.safe_string(fg_present, 1)
                    )
                    db.session.add(can_experience)

                # Flush all experiences and then query to get IDs
                # Note: RCECanExperience has triggers, so we can't use OUTPUT clause
                if experiences:
                    db.session.flush()  # Commit experiences to database
                    # Query back to get all experience IDs for this candidate
                    created_experiences = RCECanExperience.query.filter_by(
                        CanId=candidate.CanId
                    ).order_by(RCECanExperience.CanSeq).all()
                    experience_ids = [exp.CanExpId for exp in created_experiences]

                # 13.1. Create RCECanExpQuest (multiple) with CanExpId from experiences
                # Note: RCECanExpQuest requires CanExpId (FK to RCECanExperience)
                # If answers are experience-specific, they should include 'experience_id' or 'can_exp_id'
                # For general candidate questions (not experience-specific), save to different table or skip
                for answer in answers:
                    qtempid = int(answer.get('qtempid')) if answer.get('qtempid') else None
                    question_id = int(answer.get('question_id')) if answer.get('question_id') else None
                    answer_text = answer.get('answer')

                    # Check if answer has experience_id (for experience-specific questions)
                    answer_exp_id = answer.get('experience_id') or answer.get('can_exp_id')

                    if not question_id:
                        continue

                    # Get question details to determine FgAnsMode and QTopicId
                    question = RCQuestion.query.filter_by(QuestionId=question_id).first()

                    # Determine which experience ID to use
                    can_exp_id = None
                    if answer_exp_id:
                        # Use the specified experience ID
                        try:
                            can_exp_id = int(answer_exp_id)
                        except (ValueError, TypeError):
                            pass
                    elif experience_ids:
                        # If no specific experience_id, but candidate has experiences
                        # Link to the first experience (or skip if these are general questions)
                        # Option 1: Link to first experience
                        can_exp_id = experience_ids[0]
                        # Option 2: Skip general questions (uncomment next line to skip)
                        # continue
                    else:
                        # No experiences and no specific experience_id
                        # Skip this question as RCECanExpQuest requires CanExpId
                        print(f"Skipping question {question_id}: No experience to link to")
                        continue

                    can_answer = CanExpQuestId(
                        CanExpId=can_exp_id,  # REQUIRED: FK to RCECanExperience
                        QuestionId=question_id,
                        QuestCanId=candidate.CanId,
                        QTempId=qtempid,
                        QTopicId=question.QTopicId if question else None,
                        FgAnsMode=CandidateService.safe_string(question.FgAnsMode if question else None, 1),
                        UpdDate=now,
                        UpdUser=CandidateService.safe_string(can_code, 15),
                        UpdFlag=CandidateService.safe_string('I', 1)
                    )

                    # Set answer based on FgAnsMode
                    if question and question.FgAnsMode == 'O':
                        # Numeric answer (for salary expectations, etc.)
                        try:
                            can_answer.QAnsNumeric = float(answer_text)
                        except (ValueError, TypeError):
                            can_answer.QuestAnswer = answer_text  # Fallback to text
                    else:
                        # Text answer (for Yes/No, free text, etc.)
                        can_answer.QuestAnswer = answer_text

                    db.session.add(can_answer)

                # 14. Handle document uploads - Save as BLOB in RCECanDocument table
                if 'documents[]' in files:
                    documents = files.get('documents[]', [])
                    if not isinstance(documents, list):
                        documents = [documents]

                    # Get document descriptions if provided
                    doc_descriptions = form_data.get('document_descriptions[]', [])

                    # Handle different formats: list (from getlist), JSON string, or empty
                    if not isinstance(doc_descriptions, list):
                        if doc_descriptions:
                            try:
                                # If it's a JSON string, parse it
                                doc_descriptions = json.loads(doc_descriptions)
                            except (json.JSONDecodeError, ValueError):
                                doc_descriptions = []
                        else:
                            doc_descriptions = []

                    # Save each document as BLOB
                    for idx, doc in enumerate(documents):
                        if doc and doc.filename:
                            # Read document as binary data
                            doc_binary = doc.read()

                            # Get description for this document
                            doc_desc = doc_descriptions[idx] if idx < len(doc_descriptions) else None

                            # Create RCECanDocument record
                            can_doc = RCECanDocument(
                                CanId=candidate.CanId,
                                CanDocDesc=CandidateService.safe_string(doc_desc, 200) if doc_desc else None,
                                CanDocFile=CandidateService.safe_string(secure_filename(doc.filename), 200),
                                CanDoc=doc_binary,
                                CanDocTypeId=None,  # Set to None unless document type is provided
                                UpdDate=now,
                                UpdUser=CandidateService.safe_string(can_code, 15),
                                UpdFlag=CandidateService.safe_string('I', 1)
                            )
                            db.session.add(can_doc)

                # 15. Commit transaction
                db.session.commit()

                return True, "Lamaran berhasil dikirim", {
                    "candidate_id": candidate.CanId,
                    "candidate_code": candidate.CanCode
                }, 200

            except Exception as e:
                db.session.rollback()
                print(f"Transaction error: {str(e)}")
                import traceback
                traceback.print_exc()
                raise

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"Database error: {str(e)}", None, 500
        except Exception as e:
            db.session.rollback()
            print(f"Error submitting candidate: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"Error: {str(e)}", None, 500
