from app.models.cardtype import PMCardType
from app import db
from sqlalchemy import asc, desc

class CardTypeService:
    """Service layer untuk mengelola Card Type"""

    @staticmethod
    def get_all_cardtypes(page=1, per_page=100, sort_by="CardType", sort_order="asc", search=""):
        """
        Get all card types with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "CardType")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by card type name (default: "")

        Returns:
            dict: Paginated card type data
        """
        try:
            # Build query
            query = PMCardType.query

            # Search filter
            if search:
                query = query.filter(PMCardType.CardType.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(PMCardType, sort_by, PMCardType.CardType)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [cardtype.to_dict() for cardtype in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_items": pagination.total,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving card types: {str(e)}"
            }

    @staticmethod
    def get_cardtype_by_id(cardtype_id):
        """
        Get a card type by ID

        Args:
            cardtype_id (int): Card Type ID

        Returns:
            dict: Card Type data
        """
        try:
            cardtype = PMCardType.query.get(cardtype_id)

            if not cardtype:
                return {
                    "success": False,
                    "message": "Card Type not found"
                }

            return {
                "success": True,
                "data": cardtype.to_dict()
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving card type: {str(e)}"
            }
