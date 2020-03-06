from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from adventure.models import Room


class Command(BaseCommand):
    def handle(self, *argv, **kwargs):

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

        try: 
            Room.objects.all().delete()
            w = World()
            num_rooms = 144
            width = 12
            height = 12
            w.generate_rooms(width, height, num_rooms)
        except:
            raise CommandError("command doesn't work")
