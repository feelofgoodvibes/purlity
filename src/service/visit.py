from src.models import Visit


class VisitService():
    """This class provides methods for managing visit-related operations, including retrieving, creating, and listing visits."""

    def __init__(self, db):
        """
        Initialize the VisitService with a database connection.

        Args:
            db: The database connection to use.
        """

        self.db = db

    def get_visit(self, visit_id: int) -> Visit:
        """
        Retrieve a visit by its ID.

        Args:
            visit_id (int): ID of the visit to retrieve.

        Returns:
            Visit: The Visit object associated with the provided visit ID.

        Raises:
            ValueError: If the visit is not found.
        """

        visit = Visit.query.filter(Visit.id==visit_id).first()

        if visit is None:
            raise ValueError(f"Visit-{visit_id} not found!")
        
        return visit

    def get_all_visits(self, short_url: str = None) -> list[Visit]:
        """
        Retrieve a list of visits, optionally filtered by a short URL.

        Args:
            short_url (str, optional): Short URL to filter visits. Defaults to None.

        Returns:
            list[Visit]: A list of Visit objects.

        """

        visits = Visit.query

        if short_url:
            visits = visits.filter(Visit.short_url==short_url)

        return visits.all()

    def create_visit(self, short_url: str) -> Visit:
        """
        Create a new visit entry for the specified short URL.

        Args:
            short_url (str): The short URL for which to create a visit entry.

        Returns:
            Visit: The newly created Visit object.
        """

        visit = Visit(short_url=short_url)
        self.db.session.add(visit)

        return visit
