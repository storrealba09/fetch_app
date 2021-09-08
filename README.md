# Fetch_App

This app is intended to satisfy the exercise for Fetch Rewards Backend Program.

Python is the language I consider myself most proficient, for the same reason, I'm choosing Flask as my framework

[here's some documentation for Flask](https://flask.palletsprojects.com/en/2.0.x/)

For this app I'm assuming the user already have an python enviroment to make the testing.

## Dependencies

The dependencies can be installed by running: pip install requirements.txt

Also we're having a dummy database in the memory as purpose of the exercise

## Calls

The calls used here are for the functions specified for the exercise. 

assuming we're running in localhost and each request is a JSON object,

we have three calls:

### /addtx
  Which add a new single transaction to the database, this is coing to be a **POST** request in the form:
       
       { "payer": string, "points": integer, "timestamp": date }
  
  reponse will be a message: *success!*

### /spend
  Where it'll calculate and update the database with the new available points and also adding this Tx to the database, it's also a **POST** request,
  The request should be:
  
          { "points": integer }
      
   the response:
                    
          [{ "payer": string, "points": integer } , { "payer": string, "points": integer }]
    
  Every entry on the list mean the amount of points discounted per payer.
  
 
 ### /balance
  This will show the current balance of each one of the payers, this is a **GET** request with no parameters to look for.
  
  The response will show payer and current points:
  
            { "payer1": integer, "payer2": integer }
            
            
            
            
            
            
            
            
I hope this documentation is clear enough to have a succesful test. This code was tested using POSTMAN.

## Thank you for your consideration
  
  
