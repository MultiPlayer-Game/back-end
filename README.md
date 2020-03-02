### Instructions to run existing files from Lambda

Set up virtual environment:
```
pip3 install pipenv
pipenv install django
pipenv shell
```

Create an .env file
paste in:

```
DEBUG=on
SECRET_KEY = 'h5&d6r-8kxsbk(-y$uy)ao)norv(5-&y0%+3v=6h44qe^h8jo1'
```

Django-related commands to run the first time
```
python manage.py makemigrations
python manage.py migrate
winpty python manage.py createsuperuser
python manage.py runserver
```
Navigate to: http://127.0.0.1:8000/
Try logging into http://127.0.0.1:8000/admin to check out what's there

Download DB Browser and open the db.sqlite3 file in project folder. 

### How the django routes work

adventure > urls.py has the routes which trigger functions in adventure > api.py 

You can see the GET and POST requests that have been provided 

### Set up Pusher

Pusher.com > "navigate to the project" > Getting Started > "right hand side" .env, paste in credentials:
```
PUSHER_APP_ID=""
PUSHER_APP_KEY=""
PUSHER_APP_SECRET=""
PUSHER_CLUSTER="mt1" #for N.Virginia
```
Uncomment in the adventure > api.py file:
```
from pusher import Pusher
```
Edit and rename existing commented out config('PUSHER_KEY') to config('PUSHER_APP_KEY')
```
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_APP_KEY'), secret=config('PUSHER_APP_SECRET'), cluster=config('PUSHER_CLUSTER'))

```
and uncomment
```
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
```

Add rooms to your database
  * `./manage.py shell`
  * Copy/paste the contents of `util/create_world.py` into the Python interpreter
  * Exit the interpreter

Take a look at djangorestframework setup
```
python manage.py runserver
```
Navigate to 

### http://127.0.0.1:8000/api/registration/

Register a new user named "admin"

### checkout http://127.0.0.1:8000/api/user/?name=admin

PUT in first name, last name, take a look around

### Set up User Auth
### Follow tutorial at: https://medium.com/@dakota.lillie/django-react-jwt-authentication-5015ee00ef9a

Change "core" in tutorial to adventure

### To check login and obtain a token auth: http://127.0.0.1:8000/token-auth/

links that work related to the game: 
### http://127.0.0.1:8000/api/adventure/init
### http://127.0.0.1:8000/api/adventure/move # GET: user inputs n, s, e, w
### http://127.0.0.1:8000/api/adventure/say # POST: results of what room player is in
  
  
  


Think about the algorithm to draw your map. It will probably be something like this:

```
def draw_map():
    # Get all rooms
    # For each room in rooms...
        # Draw the room
        # Draw each exit
```

What data do you need to implement this? A list of rooms, their exits, maybe their positions? The server should return all the information you need from the `rooms` endpoint. Note that backend developers may need to define some fields in the `Room` model that do not exist yet.

### 3. How do I "create an interesting world"?

I'll leave that to you to determine.



### 5. What will the `rooms` API endpoint look like?

It's up to you what data the request will return but the API request should be something like this:

```
curl -X GET -H 'Authorization: Token cc504e88ef659843b858d61c101ca9d4f0edf979' http://lambda-mud-test.herokuapp.com/api/adv/rooms/
```

