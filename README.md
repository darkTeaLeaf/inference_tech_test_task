## Message service
The idea of the project is a simple message service. One can create his own user and create the messages for others, 
also, created messages can be edited or deleted by its sender. Then there is a possibility to see the list of all messages which created or received by a particular user. 

## How to start
Download the source code and install all requirements as following:
``` 
pip install -r requirements.txt 
```
Migrate changes to the database:
```
python manage.py makemigrations
python manage.py migrate
```
Start the server using the command below:
``` 
python manage.py runserver 
```
Now you can see the application on your localhost.

## How to use
The full version of API is available at `/docs/`.

Being unauthorized user only can see the list of all users (`/users/`) and the particular ones (`/users/<user_id>/`).
One can create his own user by performing the POST request at `/users/` sending the JSON with `username` and `password`.
The user information can be edited or deleted as usual by sending PUT/PATCH/DELETE requests at `/users/<your_user_id>/`. 
Access to this operations has only the user itself (so the user needs to send his credentials with the request).

An authenticated user can send a message to any user in the system including himself. For this, he should go to the `/users/<user_id>/messages`
where `user_id` specifies the user to which he wants to send a message, and perform a POST request sending JSON with `text` field.
The messages sent to or received from a particular user can be seen at `/users/<user_id>/messages` where `user_id` specifies this particular user. (At this point pages with users messages can be considered to be similar to chats in a usual messenger.)

The user can send PUT/PATCH/DELETE requests at `/users/<user_id>/messages/<id>` where `user_id` is the receiver of the message and `id` 
is a unique key of  the message. Any user can perform such operations only on messages which sent by him 
(so the user needs to send his credentials with the request). 

## Testing
Run tests using the following command:
```
python manage.py test
```
