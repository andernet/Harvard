  document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('', '', ''));


  // send the email
  document.querySelector('form').onsubmit = function() {
    const rec = document.querySelector('#compose-recipients').value;
    const sub = document.querySelector('#compose-subject').value;
    const bod = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: rec,
        subject: sub,
        body: bod
      })
    })
    .then(response => response.json())
    .then(result => {
      if (result.error !== undefined) {
        console.log(result);
        document.querySelector('#error').innerHTML = result.error; 
      }
      else {
        document.querySelector('#error').innerHTML = "";
        console.log('result.error === undefined');
        load_mailbox('sent');
      }
    })

    return false
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients='', subject='', body='') { 

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';

  //clean the div that show the emails
  document.querySelector('#emails-view').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch the email from the appropriate box
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      const divMail = document.createElement('div');
      divMail.id = `email${email.id}`
      divMail.setAttribute ('name', 'divMail');
      divMail.addEventListener('click', () => show_email(email.id, mailbox));
      if (email.read === true) 
        divMail.className = 'read container';
      else
        divMail.className = 'unread container';
      const divSender = document.createElement('div');
      divSender.innerHTML = `<b>From: </b>${email.sender}`;
      const divSubject = document.createElement('div');
      divSubject.innerHTML = `<b>Subject: </b>${email.subject}`;
      const divTimestamp = document.createElement('div');
      divTimestamp.className = 'time';
      divTimestamp.innerHTML = email.timestamp;
      divMail.append(divSender);
      divMail.append(divSubject);
      divMail.append(divTimestamp);
      document.querySelector('#emails-view').append(divMail);
    })
  })
}


// show a specific email
function show_email(id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'block';

  // clean the div that show the email
  document.querySelector('#email').innerHTML = '';

  // mark the email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  // get the email
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    const divHead = document.createElement('div');
    const divSender = document.createElement('div');
    const divRecipients = document.createElement('div');
    const divSubject = document.createElement('div');
    const divTimestamp = document.createElement('div');
    const divBody = document.createElement('div');

    divTimestamp.className = 'time';
    divHead.className = 'mailHead';

    divSender.innerHTML = `<b>From: </b>${email.sender}`;
    divRecipients.innerHTML = `<b>Recipients: </b>`;
    email.recipients.forEach(rec => {
      divRecipients.innerHTML += `${rec}, `;
    })
    divTimestamp.innerHTML = email.timestamp;
    divSubject.innerHTML = `<b>Subject: </b>${email.subject}`;
    divBody.innerHTML = email.body;

    // creates a button that archive/unarchive the email
    const butArchive = document.createElement('button');
    butArchive.className = 'btn btn-sm btn-outline-primary butt';
    if (email.archived === false) {
      butArchive.innerHTML = 'Archive';
    }
    else
      butArchive.innerHTML = 'unarchive';

    butArchive.addEventListener('click', async () => {
      await fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      load_mailbox('inbox');
    })

    // creates a reply button
    const butReply = document.createElement('button');
    butReply.className = 'btn btn-sm btn-outline-primary button';
    butReply.innerHTML = 'Reply';
    let newSubject = '';
    if (email.subject.startsWith('Re:'))
      newSubject = email.subject;
    else
      newSubject = `Re: ${email.subject}`;
    newBody = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
    butReply.addEventListener('click', () => { compose_email(email.sender, newSubject, newBody)});


    // add the divs to main email div
    divHead.append(divSender);
    divHead.append(divRecipients);
    divHead.append(divSubject);
    divHead.append(divTimestamp);
    document.querySelector('#email').append(divHead);
    document.querySelector('#email').append(divBody);
    if (mailbox !== 'sent')
      document.querySelector('#email').append(butArchive);
    document.querySelector('#email').append(butReply);
  })
}