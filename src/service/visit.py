from src.models import Visit


class VisitService():
    def __init__(self, db):
        self.db = db

    def get_visit(self, visit_id: int) -> Visit:
        visit = Visit.query.filter(Visit.id==visit_id).first()

        if visit is None:
            raise ValueError(f"Visit-{visit_id} not found!")
        
        return visit

    def get_all_visits(self):
        return Visit.query.all()

    def create_visit(self, short_url: str):
        visit = Visit(short_url=short_url)
        self.db.session.add(visit)

        return visit
