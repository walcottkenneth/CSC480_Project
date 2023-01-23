from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#defining our Ticket class... what fields it will have
class Ticket(db.Model):
    ticketID = db.Column(db.Integer, primary_key=True)
    creatorID = db.Column(db.Integer,db.ForeignKey('user.id'))
    #solver ID foreign key?
    ticketType = db.Column(db.String(30))
    ticketComments = db.Column(db.String(500))
    dateCreated = db.Column(db.DateTime(timezone=True), default=func.now())
    dateResolved = db.Column(db.DateTime(timezone=True))
    Status = db.Column(db.String(24))
    #priority level?
    #



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #all users should be combined?
    #standard user to create tickets
    #solver? people who answer ticket requests
    #super user?
    #separate ticket view/button access for solvers?
    #permissions level?
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    tickets = db.relationship('Ticket')

#class Solvers(db.Model, UserMixin):
    #empID = db.Column(db.Integer, primary_key=True)

    
    