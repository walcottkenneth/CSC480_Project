from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


#defining our Ticket class... what fields it will have
class Ticket(db.Model):
    ticketID = db.Column(db.Integer, primary_key=True)
    creatorID = db.Column(db.Integer,db.ForeignKey('user.id'))
    employeeID = db.Column(db.Integer, db.ForeignKey('Employee.empID'))
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
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    tickets = db.relationship('Ticket')

class Employee(db.Model, UserMixin):
    __tablename__ = 'Employee'
    empID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    Department = db.Column(db.String(50))
    tickets = db.relationship('Ticket')
    


#class Solvers(db.Model, UserMixin):
    #empID = db.Column(db.Integer, primary_key=True)

    
    