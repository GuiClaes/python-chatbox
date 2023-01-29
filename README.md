# Chatbox
A web app developped in Python with the framework Django.
The goal is to be able to chat with another user on the app.

#Technically
There are 2 µservices : 
- Login-app
- Message-app

HTML/CSS has been mainly done with Bootstrap as I'm not a good designer.
Back-end has been done with the following pattern : Model - View - Template. I have voluntary add a 'Repository' layer to make the lisibility easier.
All sensitive data are crypted with Bcrypt.
