from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = 'expense'  # Matches existing database table

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)        # Date object type
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        """Helper to format JSON responses matching YYYY-MM-DD string format."""
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d") if self.date else None,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }