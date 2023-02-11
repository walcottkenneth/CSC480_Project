from flask import Blueprint, render_template, request, flash, get_flashed_messages, jsonify, redirect, url_for
from flask_login import login_required, current_user
views = Blueprint('views', __name__)
from . import db
import json
from functools import wraps
from .models import User, Ticket, Employee



"""
@roles_required(roles)
Use: check if current_user contains one or multiple roles as part of the requirement
Parameters: (roles) is passed as a dict of strings... roles_required(['Base','Employee']), and checks the parameter against the current_user's roles as a subset.
Useful link for *args,**kwargs: https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
Useful link for @wraps https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
returns either a validated user or redirects them back to the login page
"""
def roles_required(roles):
    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if set(roles).issubset({r.name for r in current_user.roles}):
                return f(*args, **kwargs)
            else:
                print("Not Authorized!!!!")
                return redirect(url_for('auth.login'))
        return wrapper
    return decorated_function

"""
Route Directory for all Users... accessing 
"""
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #user form for creating a ticket
    if request.method =='POST' and 'createTicket' in request.form:
        ticketType = request.form.get('ticketType')
        ticketComments = request.form.get('ticketComments')
        if len(ticketType) < 1:     #input validation
            flash('Please Select a Type!', category='error')
        elif len(ticketComments) < 1:
            flash('Please add comments to the ticket!', category='error')
        else:
            new_ticket = Ticket(ticketType = ticketType, uidCreator = current_user.id, ticketComments = ticketComments, Status = "Active")
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket Created!', category = 'success') 
    if request.method =='POST' and "changeStatus" in request.form:
        newStatus = request.form.get('status')
        ticketID = request.form.get('ticketID')
        Ticket.query.filter_by(ticketID = ticketID).update(dict(Status=newStatus))
        db.session.commit()
    if (current_user.roles[0].name == 'Employee'):
        return render_template("empHome.html", user=current_user)
    print(current_user.roles[0].name)

    return render_template("home.html", user=current_user)


#employee view for all tickets that have not been claimed by another employee yet
@views.route('/empTicketHub', methods=['GET','POST'])
@roles_required(['Employee'])
def empTicketHub():   
    tickets = Ticket.query.filter_by(uidEmployee = None)
    emp = Employee.query.filter_by(user_id=current_user.id).first()
    print(emp.department)
    if (request.method == 'POST'):
        ticketID = request.form.get('ticketID')
        uidEmployee = current_user.id
        Ticket.query.filter_by(ticketID=ticketID).update(dict(uidEmployee=uidEmployee))
        db.session.commit()
    
    return render_template("empTicketHub.html", tickets=tickets, user=current_user)



#route for deleting a ticket...
#will validate a ticket ID, that it exists, and that it belongs to the user to delete the ticket.
@views.route('/delete-ticket', methods=['POST'])
def delete_ticket():
    ticket = json.loads(request.data)
    ticketID = ticket['ticketID']
    ticket = Ticket.query.get(ticketID)
    if ticket:
        if ticket.uidCreator == current_user.id:
            db.session.delete(ticket)
            db.session.commit()
    return jsonify({})

