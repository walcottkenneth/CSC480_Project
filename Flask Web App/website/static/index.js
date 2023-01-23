function delete_ticket(ticketID) {
    fetch('/delete-ticket',{
        method: 'POST',
        body: JSON.stringify({ ticketID: ticketID}),
    }).then((_res) => {
        window.location.href="/";
    });
}

