class Room:
    def __init__(self, n="", d="", l=False, iden="000", save=False):
        """
        Constructor: create a new Room object representing a computer component
        n: name of component
        d: description
        l: if the component is "lit" (accessible without special tools)
        iden: unique identifier
        save: whether this component's state needs to be saved
        """
        self.name = n  # Component name
        self.desc1 = d  # Original description (unchangeable)
        self.desc = d   # Current description (changeable)
        self.door = {}  # Special connection points requiring actions to traverse
        self.doors = {} # Regular connections to other components
        self.openDoors = []  # List of all connections with other components
        self.items = {}  # Items/data in this component
        self.play = []  # List of entities in this component
        self.lit = l    # If component is accessible without special tools
        self.save = save  # If component state needs saving
        self.id = iden   # Component identifier
        self.security_level = 0  # Security restriction level (0=none, 1=user, 2=admin, 3=system)
        self.data_types = []  # Types of data typically found in this component
        self.performance = {  # Performance characteristics 
            "speed": 0,       # 1-10 scale
            "capacity": 0,    # 1-10 scale
            "reliability": 0  # 1-10 scale
        }
        self.visited = False  # Has player visited this component
        self.power_state = "on"  # Power state of the component (on/off/sleep)
        self.error_state = None  # Any error conditions present
        
    def name(self):
        """Returns component name"""
        return self.name
    
    def set_specs(self, security=0, data_types=None, speed=0, capacity=0, reliability=0):
        """Set technical specifications for this computer component"""
        self.security_level = security
        self.data_types = data_types or []
        self.performance["speed"] = speed
        self.performance["capacity"] = capacity
        self.performance["reliability"] = reliability

    def connect_to(self, other, direction):
        """
        Connect this component to another component via a data path
        other: the component to connect to
        direction: direction identifier (n, s, e, w, etc.)
        """
        # Check if connection already exists
        if other.id in [list(d.keys())[0].id for d in self.openDoors if d]:
            return
            
        # Add directional connection
        self.doors.update({direction: other})
        
        # Create connection record
        connect = {other: direction}
        self.openDoors.append(connect)
        
        # Update description to mention connection
        if direction == 'n':
            dir_name = "North"
        elif direction == 's':
            dir_name = "South"
        elif direction == 'e':
            dir_name = "East"
        elif direction == 'w':
            dir_name = "West"
        elif direction == 'ne':
            dir_name = "Northeast"
        elif direction == 'nw':
            dir_name = "Northwest"
        elif direction == 'se':
            dir_name = "Southeast"
        elif direction == 'sw':
            dir_name = "Southwest"
        elif direction == 'u':
            dir_name = "Up"
        elif direction == 'd':
            dir_name = "Down"
        else:
            dir_name = direction
            
        # No need to modify description - we'll handle this in print_details

    def add_items(self, item):
        """
        Add items/data to this component
        item: dictionary with name/description pairs
        """
        # Create item list string
        i = ' You discover: '
        for k, v in item.items():
            i += k + ', '
            
        # Add items to component
        self.items.update(item)
        
        # Don't automatically update description - we'll handle this in print_details

    def add_door(self, name, d, od, door):
        """
        Add a special connection requiring action to use
        name: name of the connection
        d: direction from this component
        od: direction from other component
        door: the component to connect to
        """
        self.door.update({name: [d, door, od]})
        
        # Update description
        if "connection" not in self.desc.lower():
            self.desc += f" There's a {name} connection that appears to require authentication."

    def print_details(self):
        """
        Generate detailed description of the component
        including connections and contents
        """
        # Component name
        s = f"{self.name}\n"
        
        # Main description
        s += f"{self.desc}\n"
        
        # Connections to other components
        if self.doors:
            s += "\nConnections:\n"
            for d, r in self.doors.items():
                # Convert direction code to readable text
                if d == 'n':
                    di = 'North'
                elif d == 's':
                    di = 'South'
                elif d == 'e':
                    di = 'East'
                elif d == 'w':
                    di = 'West'
                elif d == 'u':
                    di = 'Up'
                elif d == 'd':
                    di = 'Down'
                elif d == 'ne':
                    di = 'Northeast'
                elif d == 'nw':
                    di = 'Northwest'
                elif d == 'se':
                    di = 'Southeast'
                elif d == 'sw':
                    di = 'Southwest'
                else:
                    di = d
                    
                # Add connection information
                s += f"- {di}: {r.name}\n"
        
        # Items/data in this component
        if self.items:
            s += "\nPresent in this component:\n"
            for i in self.items:
                s += f"- {i}\n"
                
        # Technical details if player has advanced knowledge
        if self.visited:
            s += "\nComponent Specifications:\n"
            if self.security_level > 0:
                s += f"- Security Level: {self.security_level}\n"
            if self.data_types:
                s += f"- Data Types: {', '.join(self.data_types)}\n"
            if any(self.performance.values()):
                s += "- Performance Metrics:\n"
                for metric, value in self.performance.items():
                    if value > 0:
                        s += f"  * {metric.capitalize()}: {value}/10\n"
                        
        return s
        
    def mark_visited(self):
        """Mark this component as visited to reveal more details on subsequent visits"""
        self.visited = True
        
    def error(self, error_description):
        """Set component to error state"""
        self.error_state = error_description
        self.desc = f"ERROR: {error_description}\n\n" + self.desc
        
    def repair(self):
        """Clear error state"""
        self.error_state = None
        self.desc = self.desc1  # Reset to original description