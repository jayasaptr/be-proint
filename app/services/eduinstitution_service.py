from app.models.eduinstitution import PMEduInstitution
from app import db
from sqlalchemy import asc, desc

class EduInstitutionService:
    """Service layer untuk mengelola Education Institution"""

    @staticmethod
    def get_all_eduinstitutions(page=1, per_page=100, sort_by="EduInsName", sort_order="asc", active_only=True, search=""):
        """
        Get all education institutions with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "EduInsName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            active_only (bool): Filter only active records (default: True)
            search (str): Search by name (default: "")

        Returns:
            dict: Paginated education institutions data
        """
        try:
            # Build query
            query = PMEduInstitution.query

            # Filter active only if requested
            if active_only:
                query = query.filter(PMEduInstitution.FgActive == "Y")

            # Search filter
            if search:
                query = query.filter(PMEduInstitution.EduInsName.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(PMEduInstitution, sort_by, PMEduInstitution.EduInsName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [edu.to_dict() for edu in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving education institutions: {str(e)}"
            }

    @staticmethod
    def get_eduinstitution_by_id(edu_ins_id):
        """
        Get education institution by ID

        Args:
            edu_ins_id (int): Education institution ID

        Returns:
            dict: Education institution data or error message
        """
        try:
            edu_institution = PMEduInstitution.query.get(edu_ins_id)

            if not edu_institution:
                return {
                    "success": False,
                    "message": "Education institution not found"
                }

            return {
                "success": True,
                "data": edu_institution.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving education institution: {str(e)}"
            }
