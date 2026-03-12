# Import all models here
from app.models.edulevel import PMEduLevel
from app.models.maritalstatus import PMMaritalSt
from app.models.city import PMCity
from app.models.religion import PMReligion
from app.models.kecamatan import PMKecamatan
from app.models.vacantpos import RCEVacantPos
from app.models.odposition import ODPosition
from app.models.posadtgrphd import RCEPosAdtGrpHd
from app.models.posadtgrpdt import RCEPosAdtGrpDt
from app.models.posadtgrpmbr import RCEPosAdtGrpMbr
from app.models.race import PMRace
from app.models.candidate import RCECandidate, RCECanAddr, RCCanEdu, CanCardId, CanExpQuestId, RCECanExperience, RCECanJobExpected

__all__ = ['PMEduLevel', 'PMMaritalSt', 'PMCity', 'PMReligion', 'PMKecamatan', 'RCEVacantPos', 'ODPosition', 'RCEPosAdtGrpHd', 'RCEPosAdtGrpDt', 'RCEPosAdtGrpMbr', 'PMRace', 'RCECandidate', 'RCECanAddr', 'RCCanEdu', 'CanCardId', 'CanExpQuestId', 'RCECanExperience', 'RCECanJobExpected']
