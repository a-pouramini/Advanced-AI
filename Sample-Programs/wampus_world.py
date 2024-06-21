import random
import os

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

class World:
    def __init__(self, size, fill_random=False):
        self.grid =[['A', ' ', ' ', 'P', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', 'P', ' ', ' ', ' '],
                    [' ', ' ', 'P', ' ', ' '],
                    ['W', ' ', ' ', 'W', 'G']]
 
        if fill_random: # fill the gird by random pits and wampus
            self.grid = [[' ' for _ in range(size)] for _ in range(size)]
            # Place gold
            self.grid[size-1][size-1] = 'G'
            
            # Place pits
            num_pits =  size // 2 # random.randint(1, size)
            for _ in range(num_pits):
                pit_location = (random.randint(0, size-1), random.randint(0, size-1))
                self.grid[pit_location[0]][pit_location[1]] = 'P'
            
            # Place wampuss
            num_wampuss = size // 2 # random.randint(1, size)
            for _ in range(num_wampuss):
                wampus_location = (random.randint(0, size-1), random.randint(0, size-1))
                self.grid[wampus_location[0]][wampus_location[1]] = 'W'

        self.reset()
        self.size = len(self.grid)
        # find pits and wampus locations
        self.pit_locations = set()
        self.wampus_locations = set()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'A':
                    self.agent_location = (i,j)
                elif self.grid[i][j] == 'G':
                    self.gold_location = (i,j)
                elif self.grid[i][j] == 'P':
                    self.pit_locations.add((i, j))
                elif self.grid[i][j] == 'W':
                    self.wampus_locations.add((i, j))
        
    def reset(self):
        size = len(self.grid)
        self.gold_location = (size-1, size-1)
        self.agent_location = (0, 0)
       
        # KB
        self.safe_locations = set() # list of locations that are safe
        self.safe_locations.add(self.agent_location)

        self.possible_pits = set() # list of locations possibly containing pits
        self.possible_wampus = set() # list of locations possibly containing the Wampus
        self.confirmed_pits = set() # list of locations the agent is sure contain pits
        self.confirmed_wampus = set() # list of locations the agent is sure contain the Wampus

    def show_world(self):
        print('                    WORLD                 ')
        loc = self.agent_location
        if self.grid[loc[0]][loc[1]].strip() == '':
            self.grid[loc[0]][loc[1]] = 'A'
        elif not self.grid[loc[0]][loc[1]].strip() == 'A':
            self.grid[loc[0]][loc[1]] = 'A ' + self.grid[loc[0]][loc[1]]
        for row in self.grid:
            print(row)
        print()


    def show_kb(self):
        # Reset KB to empty state before updating
        KB = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        
        # Mark the agent's current location
        KB[self.agent_location[0]][self.agent_location[1]] = 'A'
        
        # Mark safe locations
        for loc in self.safe_locations:
            if KB[loc[0]][loc[1]].strip() == '':
                KB[loc[0]][loc[1]] = '-'
            else:
                KB[loc[0]][loc[1]] = '-' + KB[loc[0]][loc[1]]
        
        # Mark possible pits
        for loc in self.possible_pits:
            if KB[loc[0]][loc[1]].strip() == '':
                KB[loc[0]][loc[1]] = '?p'
            else:
                KB[loc[0]][loc[1]] += '?p'
        
        # Mark possible wampus locations
        for loc in self.possible_wampus:
            if KB[loc[0]][loc[1]].strip() == '':
                KB[loc[0]][loc[1]] = '?w'
            else:
                KB[loc[0]][loc[1]] += '?w'
        
        # Mark confirmed pits
        for loc in self.confirmed_pits:
            KB[loc[0]][loc[1]] = 'P'
        
        # Mark confirmed wampus
        for loc in self.confirmed_wampus:
            KB[loc[0]][loc[1]] = 'W'
        
        # Determine the maximum width of each column
        column_widths = [max(len(KB[row][col]) 
            for row in range(self.size)) for col in range(self.size)]
        
        # Print the knowledge base with equal cell lengths
        print("")
        for row in KB:
            formatted_row = " | ".join(cell.ljust(column_widths[i]) for i, cell in enumerate(row))
            print("        | " + formatted_row + " |")
        

    def get_action(self):
        action = None
        neighbors = self.get_neighbors(self.agent_location)
        for direction, cell in neighbors.items():
            if (not cell in self.confirmed_wampus  
                and not cell in self.confirmed_pits
                and not cell in self.possible_pits
                and not cell in self.possible_wampus
                and not cell in self.safe_locations):
                action = direction
        if action is None:
            for direction, cell in neighbors.items():
                if cell in self.safe_locations:
                    action = direction

        return action

    def do_action(self, action):
        y, x = self.agent_location
        self.grid[y][x] = ' '
        if action.startswith('u'):
            y -= 1
        elif action.startswith('d'):
            y += 1
        elif action.startswith('l'):
            x -= 1
        elif action.startswith('r'):
            x += 1
        
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print("Invalid move. Try again.")
        else:
            self.agent_location = (y, x)

    def is_game_finished(self):
        if self.agent_location == self.gold_location:
            print("--------------------------------------")
            print("!!!!!!!!!!!!!!! You Won !!!!!!!!!!!!")
            print("--------------------------------------")
            print("Agent found the gold! The game is over.")
            return True
        elif self.agent_location in self.pit_locations:
            print("--------------------------------------")
            print("!!!!!!!!!!!!!!! GAME OVER !!!!!!!!!!!!")
            print("--------------------------------------")
            print("Agent fell into a pit! Game over.")
            return True
        elif self.agent_location in self.wampus_locations:
            print("--------------------------------------")
            print("!!!!!!!!!!!!!!! GAME OVER !!!!!!!!!!!!")
            print("--------------------------------------")
            print("Agent encountered a wampus! Game over.")
            return True
        return False

    def update_kb(self):
        self.safe_locations.add(self.agent_location)
        for loc in self.safe_locations:
            if loc in self.possible_pits:
                self.possible_pits.remove(loc)
            if loc in self.possible_wampus:
                self.possible_wampus.remove(loc)

        # Complete the rest of this function so that it finds confirmed_pits and confirmed_wampus
        # and updates possible pits and possible wampus

    def get_neighbors(self, location):
        y, x = location 
        neighbors = {}
        if x > 0:
           neighbors["left"] = (y, x-1)
        if y > 0:
           neighbors["up"] = (y-1, x)
        if x < self.size -1:
           neighbors["right"] = (y, x+1)
        if y < self.size -1:
           neighbors["down"] = (y+1, x)
        return neighbors

    def percept(self):
        # get the list of neighbors of agent location
        neighbors = self.get_neighbors(self.agent_location).values()    
        
        # Check if any neighbor has a pit
        near_pit = any(neighbor in self.pit_locations for neighbor in neighbors)
        # Check if any neighbor has a confirmed pit
        near_confirmed_pit = any(neighbor in self.confirmed_pits for neighbor in neighbors)
        
        # Check if any neighbor has a Wampus
        near_wampus = any(neighbor in self.wampus_locations for neighbor in neighbors)
        # Check if any neighbor has a confirmed Wampus
        near_confirmed_wampus = any(neighbor in self.confirmed_wampus for neighbor in neighbors)
        
        # If there's a pit nearby and there is no confirmed pit nearby, 
        # add neighbors to possible pits 
        if near_pit and not near_confirmed_pit:
            for neighbor in neighbors:
                self.possible_pits.add(neighbor)
        
        # If there's a Wampus nearby and there is no confirmed wampus nearby, 
        # add neighbors to possible Wampus 
        if near_wampus and not near_confirmed_wampus:
            for neighbor in neighbors:
                self.possible_wampus.add(neighbor)

        # If there is no pit or wampus nearby, add all neighbors to the safe locations
        if not near_pit and not near_wampus:
            for neighbor in neighbors:
                self.safe_locations.add(neighbor)
        
def create_world(use_default=True):
    size = "5" 
    if not use_default:
        input("Enter the world size:")
        while not size.isnumeric():
            print("!!! Enter a number !!!")
            size = input("Enter the world size:")

    size = int(size)
    w = World(size, fill_random = not use_default)
    return w

quit_game = False
game_over = False
restart = False
take_action = False
w = create_world()
while not quit_game:
    w.percept()
    w.update_kb()
    
    clear_screen()
    w.show_kb()
   
    msg = """
        u)up d)down l)left  r)right 
        t)take action    
        w)show world 
        R)reset 
        q)quit

        :"""

    cmd = input(msg)
    quit_game = cmd.startswith("q")
    reset = cmd.startswith("R")
    take_action = cmd.startswith("t")
    show_world = cmd.startswith("w")
    if show_world:
       w.show_world()
       input("Enter any key to continue!")
       continue
    if quit_game:
        break
    if reset:
        w.reset()
        continue

    if take_action:
        action = w.get_action()
    else:
        action = cmd
    w.do_action(action)
    game_over = w.is_game_finished()
    if game_over:
        w.show_world()
        cmd = input("r) restart n) new world  q) quit game:")
        quit_game = cmd.startswith("q")
        if not quit_game:
            w = create_world(use_default = cmd != "n")

