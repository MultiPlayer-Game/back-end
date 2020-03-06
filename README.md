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
  * `./`
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
### http://127.0.0.1:8000/api/adv/init
### http://127.0.0.1:8000/api/adv/move # GET: user inputs n, s, e, w
### http://127.0.0.1:8000/api/adv/say # POST: results of what room player is in
  
Configure Heroku Deployment

commit into the repo to link with heroku app:
```
  heroku git:remote -a <your-heroku-app-name>
```

git add, git commit, 
  
```
git push heroku master
heroku config:set DISABLE_COLLECTSTATIC=1
```
Heroku App page > Settings > Config Vars
More^ > Restart All Dynos 
To check if configs are there:
```
heroku config
```

Configure Postgres Database on Heroku:
```
heroku addons:create heroku-postgresql:hobby-dev
```
Heroku Run Database Migrations:
```
heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```
If your work is in master:
```
git push heroku master
```
If you are on a branch that is not master:
```
git push heroku your_local_branch_name:master
```

To create rooms, in sample_generator.py, comment out:
```
room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
```
And add:
```
# Note that in Django, you'll need to save the room after you create it
room = Room.objects.create(title = "A Generic Room", description = "This is a generic room.", n_to = 0, s_to = 0, e_to = 0, w_to = 0, x=x, y=y)
room.save()
```             

To test, locally, run the Django ORM:
```
python manage.py shell
```

Run the following 
```
>>>from adventure.models import Room
```
Check if anything is in the adventure_room table:
```
Room.objects.all()
```
If nothing is in there, it should look like:
```
<QuerySet []>
```
If something is in there, it might look like this:
```
<QuerySet [<Room: Room object (447)>, <Room: Room object (448)>, <Room: Room object (449)>, <Room: Room object (450)>, <Room: Room object (451)>, <Room: Room object (452)>, <Room: Room object (453)>, <Room: Room object (454)>, <Room: Room object (455)>, <Room: Room object (456)>, <Room: Room object (457)>, <Room: Room object (458)>, <Room: Room object (459)>, <Room: Room object (460)>, <Room: Room object (461)>, <Room: Room object (462)>, <Room: Room object (463)>, <Room: Room object (464)>, <Room: Room object (465)>, <Room: Room object (466)>, '...(remaining elements truncated)...']>
```


delete out lines in between 'World' class in sample_generator.py
paste something like the follow. Please remember you can't have blank lines. The Room function is not needed, just World:
```
class World():
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms): #10, #10, #100 passed in below in sample
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x
        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0
        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:
            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1: #keep on going right 
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0: 
                room_direction = "w" # once we have gone all the way to the right, we go to the left
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n" # can't go right anymore
                y += 1
                direction *= -1 #multiply by -1
            # Create a room in the given direction
            # room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it
            room = Room.objects.create(title = "A Generic Room", description = "This is a generic room.", n_to = 0, s_to = 0, e_to = 0, w_to = 0, x=x, y=y)
            room.save()
            # print(room.title)
            # Save the room in the World grid
            self.grid[y][x] = room
            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connectRooms(room, room_direction)
            # Update iteration variables
            previous_room = room
            room_count += 1
```
Then additionally add in:
```
Room.objects.all().delete()
w = World()
num_rooms = 144
width = 12
height = 12
w.generate_rooms(width, height, num_rooms)>
```
Check if rooms were added:
```
Room.objects.all()
```

Make a series of folders: adventure > management > commands > create_word.py

In create_world.py, first few lines should be:
```
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from adventure.models import Room


class Command(BaseCommand):
    def handle(self, *argv, **kwargs):
```
Then the function to generate rooms, which is letter by letter the World Class above, then end by calling the function that we had pasted separately in the ORM:
```
        try: 
            Room.objects.all().delete()
            w = World()
            num_rooms = 144
            width = 12
            height = 12
            w.generate_rooms(width, height, num_rooms)
        except:
            raise CommandError("command doesn't work")
```

After pushing to Heroku, run:
```
heroku run python manage.py create_world
```


### Run Front-end

If yarn is not installed:
###https://classic.yarnpkg.com/en/docs/install/#windows-stable
###https://chocolatey.org/install
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

choco install yarn

curl -o- -L https://yarnpkg.com/install.sh | bash

export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

```


Navigate to the mud folder in front-end repo
```
yarn install
yarn start
```
