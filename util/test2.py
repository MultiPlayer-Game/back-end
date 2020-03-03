import random
from adventure.models import Player, Room
Room.objects.all().delete()


class World:
    def __init__(self):
        self.grid = ''
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        # Initialize the grid
        grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(grid)):
            grid[i] = [None] * size_x
        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0
        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        horizontalDirection = 1  # 1: up, -1: down
        # Generated Room Names
        roomAdj = ["Dark", "Old", "Old, Intact", "Loathsome", "Horrid",
                   "Empty", "Moist, Murky", "Suspicous", "Damp", "Gloomy", "Secret", "Filthy", "Misty", "Moldy", "Pestilent", "Cozy Little", "Dim", "Smokey", "Vacant", "Ancient"]
        roomNames = ["Cellar", "Cave", "Cabin", "Hideout",
                     "Pathway", "Corridor", "Cave", "Hideout",
                     "Pathway", "Corridor", "Treasure Room"]
        # Generated Room Descriptions
        descriptionBeginnings = [
            "You approach a(n)", "You step forward and see a(n)", "You walk into a(n)", "This is a", "You creep into a(n)"]
        descriptionInfo = ["It seems to give off an errie mood", "Its a pretty dark room, better watch you step!", "You see a sparkling light deeper in the dungeon, is it your imagination?",
                    "A terrible smell creeps up your nose.", "Seems like a cozy place", "Its a very quiet room. Too quiet.", "Its very dark in here.", "Dont be fooled.", "You hear some rocks hit the ground, better watch your step."]
        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:
            # Calculate the direction of the room to be created
            nextDi = random.randint(0, 18)
            canDown = horizontalDirection <= 0
            canUp = horizontalDirection >= 0
            if nextDi > 11 and canDown and not grid[y-1][x] and y > 1 and x < size_x - 2 and x > 1:
                room_direction = "s"
                horizontalDirection = -1
                y -= 1
            elif x > 1 and nextDi > 16 and canUp:
                room_direction = "n"
                horizontalDirection = 1
                y += 1
            elif direction > 0 and x < size_x - 1 and not grid[y][x+1]:
                room_direction = "e"
                horizontalDirection = 0
                x += 1
            elif direction < 0 and x > 0 and not grid[y][x-1]:
                horizontalDirection = 0
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                # If theres a room above it, go to the room above that
                if grid[y+1][x]:
                    while grid[y+1][x]:
                        y += 1
                        previous_room = grid[y][x]
                y += 1
                room_direction = "n"
                horizontalDirection = 1
                direction *= -1
            currentName = random.choice(roomAdj) + " " + random.choice(roomNames)
            roomDescription = random.choice(
                descriptionBeginnings) + " " + currentName.lower() + ". " + random.choice(descriptionInfo)
            # Create a room in the given direction
            room = Room(title=currentName,
                        description=roomDescription, x=x, y=y)
            # Note that in Django, you'll need to save the room after you create it
            # Save the room in the World grid
            grid[y][x] = room
            room.save()
            # Connect the new room to the previous room
            if previous_room is not None:
                reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
                reverse_dir = reverse_dirs[room_direction]
                previous_room.connect_rooms(room, room_direction)
                room.connect_rooms(previous_room, reverse_dir)
            if nextDi < 10 and y > 0 and grid[y-1][x]:
                room.connect_rooms(grid[y-1][x], "s")
                grid[y-1][x].connect_rooms(room, "n")
            # Update iteration variables
            if previous_room:
                previous_room.save()
            room.save()
            previous_room = room
            room_count += 1
        self.grid = f"{grid}"
        return


w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
print(w.grid)
players = Player.objects.all()
for p in players:
    p.current_rooms = Room.objects.first()
    p.save()