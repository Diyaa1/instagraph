from app import db

class Setting(db.Model):
    key = db.Column(db.String(60), primary_key=True, autoincrement=False)
    value = db.Column(db.String(120))

    def to_json(self):
        """Convert the model to dictionary for ease json conversion"""
        return {
            "key": self.key,
            "value": self.value,
        }