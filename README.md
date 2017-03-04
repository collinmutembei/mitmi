[![Build Status](https://travis-ci.com/collinmutembei/mitmi.svg?token=qfEB7xnx4GDmq32ixpnD&branch=develop)](https://travis-ci.com/collinmutembei/mitmi)

### mitmi
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f34d8625a16713f0d6d0#?env%5Bmitmi-local%5D=W3siZW5hYmxlZCI6dHJ1ZSwia2V5IjoibWl0bWkiLCJ2YWx1ZSI6Imh0dHA6Ly8xMjcuMC4wLjE6NTAwMCIsInR5cGUiOiJ0ZXh0In1d)

#### requirements
- [x] CRUD operations on user account
  - signup
    - [x] As a new user I should be able to CREATE an account using a username and password
    - [x] No READ
    - [x] No UPDATE
    - [x] No DELETE
  - signin
    - [x] As a user with an account I should authenticate with username and password to get token
    - [x] No READ
    - [x] No UPDATE
    - [x] No DELETE
- [ ] CRUD operations on events
  - [x] As a logged in user I should be able to CREATE an event using a name and location
  - [ ] As a logged in user I can see all events
  - [ ] As a logged in user and creator of event I should be able to UPDATE the event details
  - [ ] As a logged in user and creator of event I should be able to DELETE

#### License
This project is licensed under GNU GPL v3 &copy; Collin Mutembei <whenyourepissed@gmail.com>
