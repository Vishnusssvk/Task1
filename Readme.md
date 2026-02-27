pip install -r requirements.txt 

run main.py

open postman and do

GET: http://127.0.0.1:5000//api/users

GET BY ID:http://127.0.0.1:5000//api/users/ID

POST:http://127.0.0.1:5000//api/users/
    add the json file on raw format
    
PUT: http://127.0.0.1:5000//api/users/{id}

PATCH:http://127.0.0.1:5000//api/users/{id}

DELETE:http://127.0.0.1:5000//api/users/{id}

PATCH: http://127.0.0.1:5000//api/users/{id}

SUMMARY:http://127.0.0.1:5000//api/users/summary

To handle limits and page
add ?page = (required number) / limit = (required number)

** use & if there exist multiple queies in the request

1.How long did it take you?

   it took me around 6 hours to complete this s it is new to me i have to lesrn each of them how it os working.

2.What was most challenging?

  the challenging part is the fetching the summary part i did more research n how to ftch all those data and aggregte them also the page limit and offset part.
  
 3.What was unclear?
 
  the connection made between sqlite flask and where the sqlite actually works
  
 4.Any unexpected challenges?
 
  when working with postman the bugs that araised made unexpected confusion on code , the initialization opart which I made where the db_initialized is set to fase and it shows nameerror (solved by adding globl keyword)
  
5.Is the difficulty appropriate?

  I feel yes as I was new to Flask and creating API and performing CRUD opertion made a basic understanding of flow that happens in a webpage
  
6.Why the chosen tools?

  flask is more beginner friendly as all the predefined classes and functions are easy 
  
7.Any assumptions or decisions made?

  pagination defaults (page = 1, limit = 5) were selected .
