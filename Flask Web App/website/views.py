from flask import Blueprint, render_template, request, flash, get_flashed_messages, jsonify
from flask_login import login_required, current_user
views = Blueprint('views', __name__)
from .models import Ticket
from . import db
import json


#category='error': label for evaluation that simply changes the background color to red to indicate an error
#category='success': label for evaluation that simply changes the background color to green to indicate successful post
#flash is a method to literally flash a message at the top, takes two parameters ("string to return", category of evaluation)

#root directory for our website
@views.route('/', methods=['GET', 'POST'])
@login_required
#what happens when we arrive at our endpoint
def home():
    #check request type
    if request.method =='POST' and 'createTicket' in request.form:
        #if user clicks add ticket
        #return our passed variables through flask
        ticketType = request.form.get('ticketType')
        ticketComments = request.form.get('ticketComments')
        #check that our returned ticket variables are valid
        if len(ticketType) < 1:
            flash('Please Select a Type!', category='error')
        elif len(ticketComments) < 1:
            flash('Please add comments to the ticket!', category='error')
        else:
            #create a new_Ticket object with the parameters... Ticket() is an instantiation from our database where we assign our fields
            new_ticket = Ticket(ticketType = ticketType, ticketComments = ticketComments, creatorID = current_user.id, Status = "Active")
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket Created!', category = 'success')
        
    if request.method =='POST' and "changeStatus" in request.form:
        newStatus = request.form.get('status')
        print(newStatus)
        ticketID = request.form.get('ticketID')
        print(ticketID)
        Ticket.query.filter_by(ticketID = ticketID).update(dict(Status=newStatus))
        db.session.commit()
    #returns our html document for the current user authentication
    return render_template("home.html", user=current_user)

#route for deleting a ticket... only accepts a post request, as we don't have an endpoint
@views.route('/delete-ticket', methods=['POST'])
#what happens when we call this request
def delete_ticket():
    #get our ticketID to identify which ticket we are removing
    ticket = json.loads(request.data)
    ticketID = ticket['ticketID']
    #queries our database with the ticketID to remove
    ticket = Ticket.query.get(ticketID)
    #if the ticket does exist (logically this will always be true)
    if ticket:
        #validate that the user is deleting a ticket that belongs to them
        if ticket.creatorID == current_user.id:
            db.session.delete(ticket)
            db.session.commit()
    return jsonify({})

@views.route('/empTicketHub', methods=['GET','POST'])
def pickTicket():    
    tickets = Ticket.query.filter_by(employeeID = None)
    for ticket in tickets:
        print(ticket)

    if (request.method == 'POST'):
        pass
    return render_template("empTicketHub.html", tickets=tickets)