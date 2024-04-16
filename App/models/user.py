from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    routines=db.Relationship('Routine', backref='user')
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def editRoutine(self,routineId,newRoutine):
        routine=Routine.query.get(routineID)
        if routine==self:
            routine.routineName=newRoutine
            db.session.add(routine)
            db.session.commit()
            return True
        return None

    def createRoutine(self,routineId):
        routine=Routine.query.get(routineID)
        if not routine:
            try:
                userRoutine=Routine(routineID,self.id)
                db.session.add(userRoutine)
                db.session.commit()
                return userRoutine
            except Exception as e:
                print(e)
                db.session.rollback()
                return None
        return None

    def removeRoutine(self,routineId):
        userRoutine=Routine.query.get(routineID)
        if userRoutine==self:
            db.session.delete(userRoutine)
            db.session.commit()
            return True
        else:
            return False

