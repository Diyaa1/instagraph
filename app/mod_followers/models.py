from app import db

class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    full_name = db.Column(db.String(120))
    profile_pic_url = db.Column(db.Text())
    follower_for = db.Column(db.String(120))
    batch_id = db.Column(db.String(120))