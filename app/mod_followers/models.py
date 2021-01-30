from app import db

class Batch(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.String(120))
    created_at = db.Column(db.DateTime())

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user,
            "created_at": self.created_at,
        }

class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(120))
    username = db.Column(db.String(120))
    full_name = db.Column(db.String(120))
    profile_pic_url = db.Column(db.Text())
    follower_for = db.Column(db.String(120))
    batch_id = db.Column(db.Integer(), db.ForeignKey('batch.id'))

    def to_json(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "username": self.username,
            "full_name": self.full_name,
            "profile_pic_url": self.profile_pic_url,
            "follower_for": self.follower_for,
            "batch_id": int(self.batch_id),
        }