- Working on the treatment model and endpoint
 1. created the treatment.py model
 2. created the treatment_route.py to have the treatment routes for CRUD
 3. added the new treatment blueprint in app.py for the treatment and also imported treatment route
 4. Ran the migrations - add treatment model

 to ensure that the details as patient and therapist id's are the same...
 1. updated user.py to create the rlthnsp - 
,



 Consider using a library like marshmallow to validate user input and ensure data integrity before saving it to the database.

 - please ensure to save your login token to use in the treatment endpoint


 errors sumbua

 app.py added 
 #added just to register working routes
for rule in app.url_map.iter_rules():
    print(rule)
