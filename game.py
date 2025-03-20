import time
import random
from player import Player
from room import Room
from map import Map
from visualizer import ComponentVisualizer
from minigames import CPUPipelineMinigame, MemoryHierarchyMinigame
from saveload import SaveLoadSystem

class Achievement:
    def __init__(self, id, name, description, condition_fn, reward=None):
        self.id = id
        self.name = name
        self.description = description
        self.condition_fn = condition_fn  # Function that returns True when achieved
        self.unlocked = False
        self.unlock_time = None
        self.reward = reward  # Optional reward (item, knowledge, etc.)

class ProgressSystem:
    def __init__(self, game):
        self.game = game
        self.achievements = []
        self.exploration_progress = 0  # Percentage of map explored
        self.knowledge_progress = 0    # Percentage of total knowledge gained
        self.virus_progress = 0        # Percentage of viruses found/quarantined
        self.total_score = 0
        
        # Setup achievements
        self.setup_achievements()
        
    def setup_achievements(self):
        """Define all achievements for the game"""
        self.achievements = [
            Achievement(
                "first_step",
                "First Steps",
                "Visit your first new component after the CPU Core",
                lambda: len([r for r in self.game.game_map.rooms.values() if r.visited]) > 1
            ),
            Achievement(
                "explorer",
                "System Explorer",
                "Visit at least 10 different components",
                lambda: len([r for r in self.game.game_map.rooms.values() if r.visited]) >= 10
            ),
            Achievement(
                "master_explorer",
                "System Cartographer",
                "Visit all system components",
                lambda: all(r.visited for r in self.game.game_map.rooms.values())
            ),
            Achievement(
                "first_virus",
                "Threat Detector",
                "Find your first virus",
                lambda: len(self.game.player.found_viruses) >= 1
            ),
            Achievement(
                "virus_hunter",
                "Virus Hunter",
                "Find all viruses in the system",
                lambda: len(self.game.player.found_viruses) >= len(self.game.viruses)
            ),
            Achievement(
                "first_quarantine",
                "Security Specialist",
                "Successfully quarantine your first virus",
                lambda: len(self.game.player.quarantined_viruses) >= 1
            ),
            Achievement(
                "system_savior",
                "System Savior",
                "Quarantine all viruses and save the system",
                lambda: len(self.game.player.quarantined_viruses) >= len(self.game.viruses)
            ),
            Achievement(
                "cpu_expert",
                "CPU Architecture Expert",
                "Reach maximum knowledge of CPU components",
                lambda: self.game.player.knowledge['cpu'] >= 5
            ),
            Achievement(
                "memory_expert",
                "Memory Systems Expert",
                "Reach maximum knowledge of memory systems",
                lambda: self.game.player.knowledge['memory'] >= 5
            ),
            Achievement(
                "storage_expert",
                "Storage Expert",
                "Reach maximum knowledge of storage systems",
                lambda: self.game.player.knowledge['storage'] >= 5
            ),
            Achievement(
                "network_expert",
                "Networking Expert",
                "Reach maximum knowledge of network components",
                lambda: self.game.player.knowledge['networking'] >= 5
            ),
            Achievement(
                "security_expert",
                "Security Expert",
                "Reach maximum knowledge of security concepts",
                lambda: self.game.player.knowledge['security'] >= 5
            ),
            Achievement(
                "computer_scientist",
                "Computer Scientist",
                "Reach maximum knowledge in all areas",
                lambda: all(level >= 5 for level in self.game.player.knowledge.values())
            ),
            Achievement(
                "efficient",
                "Efficient Operator",
                "Complete the game in under 50 turns",
                lambda: self.game.victory and self.game.turns < 50
            ),
        ]
    
    def update(self):
        """
        Update progress metrics and check for newly unlocked achievements
        Should be called after each player action
        """
        # Update exploration progress
        visited_rooms = len([r for r in self.game.game_map.rooms.values() if r.visited])
        total_rooms = len(self.game.game_map.rooms)
        self.exploration_progress = int((visited_rooms / total_rooms) * 100)
        
        # Update knowledge progress
        current_knowledge = sum(self.game.player.knowledge.values())
        max_knowledge = len(self.game.player.knowledge) * 5  # 5 is max level per area
        self.knowledge_progress = int((current_knowledge / max_knowledge) * 100)
        
        # Update virus progress - considered 50% for finding, 50% for quarantining
        viruses_found_pct = len(self.game.player.found_viruses) / len(self.game.viruses) * 50
        viruses_quarantined_pct = len(self.game.player.quarantined_viruses) / len(self.game.viruses) * 50
        self.virus_progress = int(viruses_found_pct + viruses_quarantined_pct)
        
        # Calculate total score
        self.total_score = self.calculate_score()
        
        # Check for newly unlocked achievements
        newly_unlocked = []
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.condition_fn():
                achievement.unlocked = True
                achievement.unlock_time = self.game.turns
                newly_unlocked.append(achievement)
                
                # Apply any rewards
                if achievement.reward:
                    self.apply_reward(achievement.reward)
                    
        return newly_unlocked
    
    def apply_reward(self, reward):
        """Apply a reward to the player"""
        if isinstance(reward, dict):
            if 'item' in reward:
                # Add an item to player inventory
                self.game.player.items[reward['item']] = reward.get('description', 'A special item')
            elif 'knowledge' in reward:
                # Increase knowledge in specific area
                area = reward['knowledge']
                amount = reward.get('amount', 1)
                if area in self.game.player.knowledge:
                    self.game.player.knowledge[area] = min(5, self.game.player.knowledge[area] + amount)
    
    def calculate_score(self):
        """Calculate player's score based on various factors"""
        score = 0
        
        # Points for exploration
        visited_rooms = len([r for r in self.game.game_map.rooms.values() if r.visited])
        score += visited_rooms * 10  # 10 points per room visited
        
        # Points for viruses found and quarantined
        score += len(self.game.player.found_viruses) * 50       # 50 points per virus found
        score += len(self.game.player.quarantined_viruses) * 100  # 100 points per virus quarantined
        
        # Points for knowledge gained
        knowledge_total = sum(self.game.player.knowledge.values())
        score += knowledge_total * 20  # 20 points per knowledge level
        
        # Bonus for efficiency (fewer turns)
        if self.game.victory:
            efficiency_bonus = max(0, 500 - (self.game.turns * 5))
            score += efficiency_bonus
        
        # Points for achievements
        score += sum(100 for a in self.achievements if a.unlocked)
        
        return score
    
    def get_progress_report(self):
        """Generate a detailed progress report for the player"""
        report = "PROGRESS REPORT\n"
        report += "===============\n\n"
        
        report += f"Exploration: {self.exploration_progress}% of system mapped\n"
        report += f"Knowledge: {self.knowledge_progress}% of total knowledge\n"
        report += f"Security: {self.virus_progress}% of virus threats handled\n\n"
        
        report += f"Current Score: {self.total_score} points\n\n"
        
        # List achievements
        if any(a.unlocked for a in self.achievements):
            report += "Achievements Unlocked:\n"
            for achievement in sorted([a for a in self.achievements if a.unlocked], key=lambda a: a.unlock_time):
                report += f"- {achievement.name}: {achievement.description}\n"
        
        # List locked achievements with hints
        locked = [a for a in self.achievements if not a.unlocked]
        if locked:
            report += "\nRemaining Challenges:\n"
            for achievement in locked:
                report += f"- ???: {achievement.description}\n"
        
        return report

class Game:
    def __init__(self):
        """
        Constructor: Create a KodeKloud Computer Quest game
        Initialize the game world and components
        """
        # Initialize computer architecture map from the Map class
        self.game_map = Map()
        self.game_map.setup()
        
        # Get player from the map
        self.player = self.game_map.player
        
        # Game state variables
        self.turns = 0
        self.game_over = False
        self.all_viruses_found = False
        self.victory = False
        
        # List of all viruses in the system
        self.viruses = [
            "boot_sector_virus", 
            "rootkit_virus", 
            "memory_resident_virus", 
            "firmware_virus", 
            "packet_sniffer_virus"
        ]
        
        # Initialize the progress tracking system
        self.progress = ProgressSystem(self)
        
        # Initialize visualizer
        self.visualizer = ComponentVisualizer()
        
        # Initialize minigame state
        self.current_minigame = None
        self.current_visualization = None
        
        # Initialize save/load system
        self.save_load = SaveLoadSystem(self)
        
        # Initialize map grid for tracking visited rooms
        self.map_grid = {
            # CPU Package
            'cpu_package': {'visited': False},
            
            # Cores and components
            'core1': {'visited': False},
            'core1_cu': {'visited': False},
            'core1_alu': {'visited': False},
            'core1_registers': {'visited': False},
            'core1_l1': {'visited': False},
            'core2': {'visited': False},
            'core2_cu': {'visited': False},
            'core2_alu': {'visited': False},
            'core2_registers': {'visited': False},
            'core2_l1': {'visited': False},
            
            # Cache hierarchy
            'l2_cache1': {'visited': False},
            'l2_cache2': {'visited': False},
            'l3_cache': {'visited': False},
            'memory_controller': {'visited': False},
            
            # RAM
            'ram_dimm1': {'visited': False},
            'ram_dimm2': {'visited': False},
            'ram_dimm3': {'visited': False},
            'ram_dimm4': {'visited': False},
            
            # Conceptual spaces
            'kernel': {'visited': False},
            'virtual_memory': {'visited': False},
            
            # PCH components
            'pch': {'visited': False},
            'storage_controller': {'visited': False},
            'pcie_controller': {'visited': False},
            'network_interface': {'visited': False},
            'bios': {'visited': False},
            
            # Storage 
            'sata_ports': {'visited': False},
            'ssd': {'visited': False},
            'hdd': {'visited': False},
            
            # PCIe and expansion
            'pcie_x16': {'visited': False},
            'pcie_x1_1': {'visited': False},
            'pcie_x1_2': {'visited': False},
            'gpu': {'visited': False},
            
            # External ports
            'usb_ports': {'visited': False},
            'ethernet': {'visited': False}
        }
        
        # Mark the starting room as visited on the map
        for room_id, room in self.game_map.rooms.items():
            if room == self.player.location:
                if room_id in self.map_grid:
                    self.map_grid[room_id]['visited'] = True
                break
                
        # Print welcome message
        self.display_welcome()
        
    def start(self):
        """
        Main game loop
        """
        # Loop until victory or quit
        while not self.game_over:
            # Get user input
            user_input = input("\n> ").strip()
            
            # Skip empty inputs
            if not user_input:
                continue
                
            # Split into command words
            cmd_words = user_input.split()
            
            # Process command
            response = self.process_cmd(cmd_words)
            
            # Display result
            print(f"\n{response}")
            
        # Game over - ask to play again or exit
        if self.victory:
            print("\nWould you like to play again? (y/n)")
            replay = input("> ").lower()
            if replay in ['y', 'yes']:
                # Reset and start new game
                self.__init__()
                self.start()
            else:
                print("\nThank you for playing KodeKloud Computer Quest! Goodbye!")
        else:
            print("\nExiting KodeKloud Computer Quest. Goodbye!")

# This method has been removed since we're now using Map class from map.py

# These methods have been removed since we're now using Map class from map.py

    def display_welcome(self):
        """Display welcome message and game introduction"""
        print("=" * 70)
        print("   █▄▀ █▀█ █▀▄ █▀▀ █▄▀ █   █▀█ █░█ █▀▄   █▀▀ █▀█ █▀▄▀█ █▀█ █░█ ▀█▀ █▀▀ █▀█   █▀█ █░█ █▀▀ █▀ ▀█▀")
        print("   █░█ █▄█ █▄▀ ██▄ █░█ █▄▄ █▄█ █▄█ █▄▀   █▄▄ █▄█ █░▀░█ █▀▀ █▄█ ░█░ ██▄ █▀▄   ▀▀█ █▄█ ██▄ ▄█ ░█░")
        print("=" * 70)
        print("\nWelcome to the KodeKloud Computer Architecture Quest!")
        print("\nYou are a security program deployed into a computer system infected with")
        print("multiple viruses. Your mission is to locate and quarantine all viruses")
        print("while learning about computer architecture.")
        print("\nAs you travel through the system, from CPU to memory to storage and beyond,")
        print("you'll discover how each component works and how they interconnect.")
        print("\nUse the 'help' command to see available actions.")
        print("\nGood luck, Security Program! The system's integrity depends on you.")
        print("\n" + "=" * 70)
        
        # Show initial location description
        print(f"\n{self.player.location.name}:\n{self.player.location.desc}")
        print("\nType 'help' for a list of commands.")

    def move(self, direction):
        """
        Move the player in the specified direction
        """
        # Normalize direction input
        if direction in ['north', 'n']:
            dir_code = 'n'
        elif direction in ['south', 's']:
            dir_code = 's'
        elif direction in ['east', 'e']:
            dir_code = 'e'
        elif direction in ['west', 'w']:
            dir_code = 'w'
        elif direction in ['northeast', 'ne']:
            dir_code = 'ne'
        elif direction in ['northwest', 'nw']:
            dir_code = 'nw'
        elif direction in ['southeast', 'se']:
            dir_code = 'se'
        elif direction in ['southwest', 'sw']:
            dir_code = 'sw'
        elif direction in ['up', 'u']:
            dir_code = 'u'
        elif direction in ['down', 'd']:
            dir_code = 'd'
        else:
            return f"Invalid direction: {direction}"
            
        # Track previous location to provide feedback
        prev_location = self.player.location
        
        # Attempt to move
        if self.player.go(dir_code):
            # If successfully moved
            curr_location = self.player.location
            
            # Mark newly visited components
            curr_location.mark_visited()
            
            # Update map - find which room this is
            for room_id, room in self.game_map.rooms.items():
                if room == curr_location:
                    # Found the room ID
                    if room_id in self.map_grid:
                        self.map_grid[room_id]['visited'] = True
                    break
            
            # Update turn counter
            self.turns += 1
            
            # Add system architecture educational note on first visit
            if prev_location.name != curr_location.name:
                result = f"Moved from {prev_location.name} to {curr_location.name}.\n\n"
                result += f"{curr_location.name}:\n{curr_location.desc}"
                
                # Handle any NPCs or hostile entities
                if curr_location.play:
                    # In future versions, handle encounters here
                    pass
                    
                return result
            else:
                # This shouldn't happen with the current implementation
                return f"You remain at {curr_location.name}."
        else:
            # Failed to move
            return f"There is no connection to the {direction} from {self.player.location.name}."
            
    def display_map(self):
        """
        Display an interactive map of visited rooms that reveals only explored areas
        """
        # Make sure starting room is always marked as visited
        for room_id, room in self.game_map.rooms.items():
            if room == self.game_map.player.location:
                if room_id in self.map_grid:
                    self.map_grid[room_id]['visited'] = True
                break
                
        # Template for creating fog of war (unexplored areas)
        empty_frame = [
            "+------------------------------------------------------------------+",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "|                                                                  |",
            "+------------------------------------------------------------------+"
        ]
        
        # Component parts of the motherboard - will be revealed when visited
        component_parts = {
            'kernel': [
                "|   +----------+                                                 |",
                "|   |          |                                                 |",
                "|   | OS Kernel|                                                 |",
                "|   | (In RAM) |                                                 |",
                "|   +----------+                                                 |"
            ],
            'virtual_memory': [
                "|   +----------+                                                 |",
                "|   | Virtual  |                                                 |",
                "|   | Memory   |                                                 |",
                "|   |          |                                                 |",
                "|   +----------+                                                 |"
            ],
            'cpu_package': [
                "|                    +----------------------------------+         |",
                "|                    |                                  |         |",
                "|                    |           CPU Package            |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    +----------------------------------+         |"
            ],
            'core1': [
                "|                    |  +--------+                      |         |",
                "|                    |  | Core 1 |                      |         |",
                "|                    |  +--------+                      |         |"
            ],
            'core2': [
                "|                    |                    +--------+    |         |",
                "|                    |                    | Core 2 |    |         |",
                "|                    |                    +--------+    |         |"
            ],
            'core_components': [
                "|                    |  | CU|ALU |        | CU|ALU |    |         |",
                "|                    |  | Reg|L1 |        | Reg|L1 |    |         |"
            ],
            'l2_cache': [
                "|                    |  +--------+        +--------+    |         |",
                "|                    |  |L2 Cache|        |L2 Cache|    |         |",
                "|                    |  +--------+        +--------+    |         |"
            ],
            'l3_cache': [
                "|                    |  +----------------------------+   |         |",
                "|                    |  |      L3 Cache (Shared)     |   |         |",
                "|                    |  +----------------------------+   |         |"
            ],
            'ram_dimm1': [
                "|   +----------+                                                 |",
                "|   |RAM DIMM 1|--                                              |",
                "|   +----------+                                                 |"
            ],
            'ram_dimm2': [
                "|   +----------+                                                 |",
                "|   |RAM DIMM 2|                                                 |",
                "|   +----------+                                                 |"
            ],
            'ram_dimm3': [
                "|   +----------+                                                 |",
                "|   |RAM DIMM 3|                                                 |",
                "|   +----------+                                                 |"
            ],
            'ram_dimm4': [
                "|   +----------+                                                 |",
                "|   |RAM DIMM 4|                                                 |",
                "|   +----------+                                                 |"
            ],
            'dmi_link': [
                "|                                    |                           |",
                "|                               DMI Link                         |",
                "|                                    |                           |"
            ],
            'pch': [
                "|                    +----------------------------------+         |",
                "|                    |               PCH                |         |",
                "|                    |     (Platform Controller Hub)    |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    |                                  |         |",
                "|                    +----------------------------------+         |"
            ],
            'pch_controllers': [
                "|                    |  +----------+      +----------+   |         |",
                "|                    |  | Storage  |      |   PCIe   |   |         |",
                "|                    |  |Controller|      |Controller|   |         |",
                "|                    |  +----------+      +----------+   |         |"
            ],
            'pch_components': [
                "|                    |  +----------+      +----------+   |         |",
                "|                    |  | Network  |      |BIOS/UEFI |   |         |",
                "|                    |  |Interface |      |  Flash   |   |         |",
                "|                    |  +----------+      +----------+   |         |"
            ],
            'storage': [
                "|   +------+                                                    |",
                "|   | SSD  |-------                                             |",
                "|   +------+                                                    |",
                "|                                                               |",
                "|   +------+                                                    |",
                "|   | HDD  |---+                                                |",
                "|   +------+   |                                                |"
            ],
            'io_ports': [
                "|                    +-----------------+---------+--------+      |",
                "|                    |  SATA Ports     |    USB Ports    Ethernet |",
                "|                    +-----------------+---------+--------+      |"
            ],
            'pcie_slots': [
                "|                    +----------------+                          |",
                "|                    |  PCIe x16 Slot |                          |",
                "|                    +----------------+                          |",
                "|                                                                |",
                "|                    +----------------+                          |",
                "|                    |  PCIe x1 Slot  |                          |",
                "|                    +----------------+                          |",
                "|                                                                |",
                "|                    +----------------+                          |",
                "|                    |  PCIe x1 Slot  |                          |",
                "|                    +----------------+                          |"
            ],
            'gpu': [
                "|   +------+                                                    |",
                "|   | GPU  |-------                                             |",
                "|   +------+                                                    |"
            ]
        }
        
        # Create the fog of war map (start with empty frame)
        fog_map = empty_frame.copy()
        
        # Add title
        fog_map[1] = "|             KodeKloud Computer Quest Exploration Map          |"
        
        # Dictionary of positions for each component in the map
        # The position is (row, column) where the marker will be placed
        positions = {
            'kernel': (7, 8),                # OS Kernel
            'virtual_memory': (12, 8),       # Virtual Memory
            'cpu_package': (7, 36),          # CPU Package
            'core1': (9, 15),                # Core 1
            'core1_cu': (10, 13),            # Core 1 CU
            'core1_alu': (10, 17),           # Core 1 ALU
            'core1_registers': (11, 13),     # Core 1 Registers
            'core1_l1': (11, 17),            # Core 1 L1
            'core2': (9, 38),                # Core 2
            'core2_cu': (10, 36),            # Core 2 CU
            'core2_alu': (10, 40),           # Core 2 ALU
            'core2_registers': (11, 36),     # Core 2 Registers
            'core2_l1': (11, 40),            # Core 2 L1
            'l2_cache1': (15, 15),           # L2 Cache 1
            'l2_cache2': (15, 38),           # L2 Cache 2
            'l3_cache': (19, 30),            # L3 Cache
            'ram_dimm1': (19, 8),            # RAM DIMM 1
            'ram_dimm2': (23, 8),            # RAM DIMM 2
            'ram_dimm3': (27, 8),            # RAM DIMM 3
            'ram_dimm4': (31, 8),            # RAM DIMM 4
            'pch': (29, 36),                 # PCH
            'storage_controller': (32, 15),  # Storage Controller
            'pcie_controller': (32, 38),     # PCIe Controller
            'network_interface': (37, 15),   # Network Interface
            'bios': (37, 38),                # BIOS/UEFI
            'ssd': (36, 8),                  # SSD
            'hdd': (40, 8),                  # HDD
            'sata_ports': (45, 16),          # SATA Ports
            'usb_ports': (45, 36),           # USB Ports
            'ethernet': (45, 51),            # Ethernet
            'pcie_x16': (49, 28),            # PCIe x16 Slot
            'gpu': (49, 8),                  # GPU
            'pcie_x1_1': (53, 28),           # PCIe x1 Slot 1
            'pcie_x1_2': (57, 28)            # PCIe x1 Slot 2
        }
        
        # Component groups for revealing sections on the map
        component_groups = {
            'cpu_package': ['cpu_package'],
            'kernel': ['kernel'],
            'virtual_memory': ['virtual_memory'],
            'core1': ['core1'],
            'core_components': ['core1_cu', 'core1_alu', 'core1_registers', 'core1_l1', 
                               'core2_cu', 'core2_alu', 'core2_registers', 'core2_l1'],
            'core2': ['core2'],
            'l2_cache': ['l2_cache1', 'l2_cache2'],
            'l3_cache': ['l3_cache'],
            'ram_dimm1': ['ram_dimm1'],
            'ram_dimm2': ['ram_dimm2'],
            'ram_dimm3': ['ram_dimm3'],
            'ram_dimm4': ['ram_dimm4'],
            'pch': ['pch'],
            'pch_controllers': ['storage_controller', 'pcie_controller'],
            'pch_components': ['network_interface', 'bios'],
            'storage': ['ssd', 'hdd'],
            'io_ports': ['sata_ports', 'usb_ports', 'ethernet'],
            'pcie_slots': ['pcie_x16', 'pcie_x1_1', 'pcie_x1_2'],
            'gpu': ['gpu']
        }
        
        # Track which component parts to reveal based on visited rooms
        revealed_parts = set()
        
        # Check which rooms have been visited and mark parts to reveal
        for room_id, room_data in self.map_grid.items():
            if room_data['visited']:
                # Add revealed component parts based on visited rooms
                for group_name, group_rooms in component_groups.items():
                    if room_id in group_rooms:
                        revealed_parts.add(group_name)
                
                # Special case for connections between components
                if room_id == 'cpu_package' or room_id == 'pch':
                    revealed_parts.add('dmi_link')
                
                if room_id in ['core1', 'core2', 'core1_cu', 'core1_alu', 'core1_registers', 'core1_l1']:
                    revealed_parts.add('core_components')
        
        # Reveal map sections based on exploration
        for part_name in revealed_parts:
            if part_name in component_parts:
                part_lines = component_parts[part_name]
                
                # Determine where to place these component lines
                if part_name == 'kernel':
                    start_row = 5
                elif part_name == 'virtual_memory':
                    start_row = 10
                elif part_name == 'cpu_package':
                    start_row = 5
                elif part_name == 'core1':
                    start_row = 8
                elif part_name == 'core2':
                    start_row = 8
                elif part_name == 'core_components':
                    start_row = 10
                elif part_name == 'l2_cache':
                    start_row = 14
                elif part_name == 'l3_cache':
                    start_row = 18
                elif part_name == 'ram_dimm1':
                    start_row = 18
                elif part_name == 'ram_dimm2':
                    start_row = 22
                elif part_name == 'ram_dimm3':
                    start_row = 26
                elif part_name == 'ram_dimm4':
                    start_row = 30
                elif part_name == 'dmi_link':
                    start_row = 23
                elif part_name == 'pch':
                    start_row = 27
                elif part_name == 'pch_controllers':
                    start_row = 31
                elif part_name == 'pch_components':
                    start_row = 36
                elif part_name == 'storage':
                    start_row = 35
                elif part_name == 'io_ports':
                    start_row = 44
                elif part_name == 'pcie_slots':
                    start_row = 48
                elif part_name == 'gpu':
                    start_row = 48
                else:
                    start_row = 1
                
                # Merge the component part into the fog map
                for i, line in enumerate(part_lines):
                    if start_row + i < len(fog_map):
                        # Preserve the map border
                        base_line = fog_map[start_row + i]
                        for j in range(min(len(line), len(base_line))):
                            if line[j] != ' ' and j > 0 and j < len(base_line) - 1:
                                chars = list(base_line)
                                chars[j] = line[j]
                                base_line = ''.join(chars)
                        fog_map[start_row + i] = base_line
        
        # Add markers for visited rooms and current location
        for room_id, room in self.game_map.rooms.items():
            if room_id in positions and room_id in self.map_grid and self.map_grid[room_id]['visited']:
                row, col = positions[room_id]
                
                if row < len(fog_map) and col < len(fog_map[row]):
                    # Mark current location with ★, visited locations with •
                    if room == self.player.location:
                        marker = '★'
                    else:
                        marker = '•'
                        
                    # Apply the marker
                    line = fog_map[row]
                    if col < len(line):
                        fog_map[row] = line[:col] + marker + line[col+1:]
        
        # Combine the fog map into a string
        map_str = "YOUR EXPLORATION MAP\n"
        map_str += "===================\n\n"
        
        for line in fog_map:
            map_str += line + '\n'
            
        map_str += "\nLEGEND:\n"
        map_str += "------\n"
        map_str += "• = Visited Location\n"
        map_str += "★ = Current Location\n\n"
        
        # Add current location and available connections
        map_str += f"You are currently in: {self.player.location.name}\n"
        
        # Add connections from current location
        if self.player.location.doors:
            map_str += "Available connections:\n"
            for direction, connected_room in self.player.location.doors.items():
                # Convert direction code to readable text
                if direction == 'n':
                    dir_text = 'North'
                elif direction == 's':
                    dir_text = 'South'
                elif direction == 'e':
                    dir_text = 'East'
                elif direction == 'w':
                    dir_text = 'West'
                elif direction == 'ne':
                    dir_text = 'Northeast'
                elif direction == 'nw':
                    dir_text = 'Northwest'
                elif direction == 'se':
                    dir_text = 'Southeast'
                elif direction == 'sw':
                    dir_text = 'Southwest'
                elif direction == 'u':
                    dir_text = 'Up'
                elif direction == 'd':
                    dir_text = 'Down (DMI Link)'
                else:
                    dir_text = direction
                    
                map_str += f"- {dir_text}: {connected_room.name}\n"
                
        # Add note about the motherboard command
        map_str += "\nTip: Use the 'motherboard' command to see the full diagram."
        
        return map_str
            
    def show_help(self):
        """Show available commands"""
        help_text = """
KODEKLOUD COMPUTER QUEST COMMANDS:

Movement:
  go [direction]   - Move between components (n, s, e, w, ne, sw, etc.)
  [direction]      - You can also just type the direction (north, s, east, w)

Exploration:
  look             - Examine your current location
  look [item]      - Examine a specific item
  read [item]      - Read text content of an item
  map, m           - Display a map of visited computer components
  motherboard      - Show the motherboard layout of the computer system

Inventory:
  inventory        - List items in your storage
  take [item]      - Add an item to your inventory
  drop [item]      - Remove an item from your inventory

Security Functions:
  scan             - Search for viruses in current location
  scan [item]      - Check if a specific item contains a virus
  advscan          - Perform advanced scan (requires decoder_tool)
  advscan [item]   - Perform advanced scan on specific item
  analyze [item]   - Deeply analyze an item for hidden properties
  quarantine [virus] - Contain a discovered virus

Information:
  status           - Check your virus discovery progress
  knowledge        - View your computer architecture knowledge
  about [topic]    - Get information about a computer component
  
Progress Tracking:
  achievements     - View your achievements and progress report
  stats            - Alternative command for achievements
  
Educational Features:
  visualize [comp] - Show visualization of a component (cpu, memory, network, storage)
  viz [comp]       - Shorthand for visualize
  simulate cpu     - Start CPU pipeline simulation minigame
  simulate memory  - Start memory hierarchy simulation
  simulate step    - Advance simulation by one step
  simulate toggle  - Toggle between simulation modes
  simulate reset   - Reset the simulation
  
Save/Load:
  save [name]      - Save your game progress (optional name)
  load [name]      - Load a saved game
  saves            - List all available save files
  deletesave [name] - Delete a saved game
  
System:
  help             - Show this help message
  quit             - Exit the game
"""
        return help_text
        
    def start_cpu_minigame(self):
        """Start the CPU pipeline simulation minigame"""
        if self.player.knowledge['cpu'] < 3:
            return "You need more knowledge about CPU architecture to understand this simulation. Explore CPU components and learn more first."
        
        self.current_minigame = CPUPipelineMinigame(self)
        
        return self.current_minigame.explain() + "\n\n" + self.current_minigame.get_status() + "\n\nUse 'simulate step' to advance the simulation, 'simulate toggle' to switch modes, and 'simulate reset' to restart."
        
    def start_memory_minigame(self):
        """Start the memory hierarchy simulation minigame"""
        if self.player.knowledge['memory'] < 3:
            return "You need more knowledge about memory systems to understand this simulation. Explore memory components and learn more first."
        
        self.current_minigame = MemoryHierarchyMinigame(self)
        
        return self.current_minigame.explain()
        
    def handle_visualization(self, viz_type=None):
        """Handle visualization commands"""
        if not viz_type:
            return "Please specify what to visualize: 'viz cpu', 'viz memory', 'viz network', or 'viz storage'."
            
        viz_type = viz_type.lower()
        
        if viz_type in ['cpu', 'processor']:
            self.current_visualization = 'cpu'
            return "Displaying CPU visualization in text mode:\n\n" + self.visualizer.render_cpu_text()
            
        elif viz_type in ['memory', 'ram', 'cache']:
            self.current_visualization = 'memory'
            return "Displaying memory hierarchy visualization in text mode:\n\n" + self.visualizer.render_memory_hierarchy_text()
            
        elif viz_type in ['network', 'protocol']:
            self.current_visualization = 'network'
            return "Displaying network protocol stack visualization in text mode:\n\n" + self.visualizer.render_network_stack_text()
            
        elif viz_type in ['storage', 'disk', 'drive']:
            self.current_visualization = 'storage'
            return "Displaying storage systems visualization in text mode:\n\n" + self.visualizer.render_storage_hierarchy_text()
            
        elif viz_type == 'stop':
            prev_viz = self.current_visualization
            self.current_visualization = None
            return f"Stopped {prev_viz} visualization. Returning to text mode."
            
        else:
            return f"Unknown visualization type: {viz_type}. Try 'cpu', 'memory', 'network', or 'storage'."
            
    def handle_simulation(self, action=None):
        """Handle simulation commands"""
        if not self.current_minigame:
            return "No active simulation. Start one with 'simulate cpu' or 'simulate memory'."
            
        if not action:
            return "Please specify a simulation action: 'step', 'toggle', 'reset', or 'stop'."
            
        action = action.lower()
        
        if action == 'step':
            return self.current_minigame.step()
            
        elif action == 'toggle':
            if hasattr(self.current_minigame, 'toggle_pipeline'):
                return self.current_minigame.toggle_pipeline()
            else:
                return "This simulation doesn't support toggling modes."
                
        elif action == 'reset':
            return self.current_minigame.reset()
            
        elif action == 'stop':
            self.current_minigame = None
            return "Simulation stopped."
            
        else:
            return f"Unknown simulation action: {action}. Try 'step', 'toggle', 'reset', or 'stop'."
            
    def get_component_info(self, topic):
        """Provide educational information about computer components"""
        topics = {
            "cpu": """CPU (Central Processing Unit):
The CPU is the primary component that executes instructions and processes data. It consists of:
- Control Unit: Coordinates CPU operations and decodes instructions
- ALU (Arithmetic Logic Unit): Performs mathematical calculations
- Registers: Ultra-fast storage locations for immediate data
- Cache: Fast memory that stores frequently used data
The CPU operates using a cycle of fetch, decode, execute, and writeback phases.""",

            "memory": """Computer Memory Hierarchy:
Computer systems use multiple types of memory arranged in a hierarchy:
1. Registers: Tiny, ultra-fast storage inside the CPU
2. Cache Memory: Small, very fast memory close to the CPU (L1, L2, L3)
3. RAM: Main system memory, volatile (erased when powered off)
4. Virtual Memory: Uses hard drive space as an extension of RAM
5. Storage: HDD/SSD for permanent data storage
As you move down the hierarchy, capacity increases but speed decreases.""",

            "cache": """Cache Memory:
Cache memory serves as a high-speed buffer between the CPU and main memory.
- L1 Cache: Smallest, fastest cache, located in the CPU
- L2 Cache: Larger but slightly slower than L1
- L3 Cache: Largest but slowest cache, often shared between CPU cores
Caches use principles of temporal locality (recently used data will be used again soon) and spatial locality (data near recently used data will be used soon).""",

            "storage": """Storage Systems:
Storage provides permanent data retention, unlike volatile RAM:
- SSD (Solid State Drive): Uses flash memory, no moving parts, fast
- HDD (Hard Disk Drive): Uses magnetic storage on spinning platters
- Storage Controller: Manages data flow between system and storage
- File Systems: Organize data into files and directories
Storage operations are much slower than memory but retain data without power.""",

            "bus": """System Bus Architecture:
Buses are communication pathways that transfer data between components:
- System Bus: Main pathway connecting CPU, memory, and I/O
- Address Bus: Carries memory addresses
- Data Bus: Carries the actual data being transferred
- Control Bus: Carries command signals
- PCI/PCIe: High-speed buses for connecting expansion cards
Bus width (16, 32, 64-bit) determines how much data can be transferred at once.""",

            "network": """Network Interface:
The network component connects the computer to other systems:
- Network Interface Card: Hardware that enables network connectivity
- Protocol Stack: Software layers that format and process network data
- Packets: Units of data transferred over networks
- Protocols: Rules that govern how data is transmitted (e.g., TCP/IP)
Network interfaces handle encoding/decoding data and managing connections.""",

            "firmware": """Firmware/BIOS:
Firmware is software permanently programmed into hardware:
- BIOS/UEFI: Initialize hardware components during boot
- ROM (Read-Only Memory): Stores permanent firmware
- Boot Sequence: Process of starting up computer hardware
- Hardware Configuration: Settings for system components
Firmware operates at a lower level than the operating system.""",

            "gpu": """Graphics Processing Unit (GPU):
The GPU specializes in parallel processing for graphics and computation:
- Shader Cores: Small processors that handle graphical calculations
- VRAM: Specialized memory for storing graphical data
- Render Pipeline: Stages for transforming 3D data to 2D images
- GPGPU: General-purpose computing on GPUs for non-graphics tasks
GPUs excel at tasks that can be broken into many parallel operations.""",

            "kernel": """Operating System Kernel:
The kernel is the core of the operating system:
- Process Management: Creates and schedules processes
- Memory Management: Allocates and tracks system memory
- Device Drivers: Interfaces with hardware components
- File Systems: Manages data storage and retrieval
- System Calls: Provides services to applications
The kernel operates in a privileged mode with direct hardware access.""",

            "virus": """Computer Viruses:
Viruses are malicious programs that can damage systems:
- Boot Sector Virus: Infects system startup areas
- Rootkit: Hides in the operating system kernel
- Memory-Resident Virus: Operates entirely in RAM
- Firmware Virus: Infects system firmware/BIOS
- Network Virus: Spreads via network connections
Viruses typically attempt to hide their presence and propagate to other systems."""
        }
        
        if topic in topics:
            return topics[topic]
        else:
            related_topics = []
            for key in topics:
                if key in topic or topic in key:
                    related_topics.append(key)
                    
            if related_topics:
                return f"Topic '{topic}' not found. Did you mean: {', '.join(related_topics)}?"
            else:
                return f"No information available about '{topic}'. Try topics like: cpu, memory, cache, storage, bus, network, firmware, gpu, kernel, or virus."
                
    def display_motherboard(self):
        """Display the full motherboard layout of the computer system"""
        motherboard = [
            "+------------------------------------------------------------------+",
            "|               KodeKloud Computer Quest Motherboard Layout       |",
            "+------------------------------------------------------------------+",
            "|                                                                  |",
            "|   +----------+     +----------------------------------+          |",
            "|   |          |     |                                  |          |",
            "|   | OS Kernel|     |           CPU Package            |          |",
            "|   | (In RAM) |     |  +--------+        +--------+   |          |",
            "|   +----------+     |  | Core 1 |        | Core 2 |   |          |",
            "|                    |  | CU|ALU |        | CU|ALU |   |          |",
            "|   +----------+     |  | Reg|L1 |        | Reg|L1 |   |          |",
            "|   | Virtual  |     |  +--------+        +--------+   |          |",
            "|   | Memory   |     |                                  |          |",
            "|   |          |     |  +--------+        +--------+   |          |",
            "|   +----------+     |  |L2 Cache|        |L2 Cache|   |          |",
            "|                    |  +--------+        +--------+   |          |",
            "|                    |                                  |          |",
            "|   +----------+     |  +----------------------------+  |          |",
            "|   |RAM DIMM 1|-----|  |      L3 Cache (Shared)     |  |          |",
            "|   +----------+     |  +----------------------------+  |          |",
            "|                    +----------------------------------+          |",
            "|   +----------+                      |                            |",
            "|   |RAM DIMM 2|                      |                            |",
            "|   +----------+                DMI Link                           |",
            "|                                     |                            |",
            "|   +----------+                      |                            |",
            "|   |RAM DIMM 3|     +----------------------------------+          |",
            "|   +----------+     |                                  |          |",
            "|                    |               PCH                |          |",
            "|   +----------+     |     (Platform Controller Hub)    |          |",
            "|   |RAM DIMM 4|     |  +----------+      +----------+  |          |",
            "|   +----------+     |  | Storage  |      |   PCIe   |  |          |",
            "|                    |  |Controller|      |Controller|  |          |",
            "|                    |  +----------+      +----------+  |          |",
            "|   +------+         |                                  |          |",
            "|   | SSD  |---------|  +----------+      +----------+  |          |",
            "|   +------+         |  | Network  |      |BIOS/UEFI |  |          |",
            "|                    |  |Interface |      |  Flash   |  |          |",
            "|   +------+         |  +----------+      +----------+  |          |",
            "|   | HDD  |---+     +----------------------------------+          |",
            "|   +------+   |                 |               |                 |",
            "|              |                 |               |                 |",
            "|              |     +-----------+     +---------+                 |",
            "|              |     |                 |                           |",
            "|              +-----|  SATA Ports     |    USB Ports    Ethernet |",
            "|                    +-----------------+---------+--------+        |",
            "|                                                                  |",
            "|   +------+         +----------------+                            |",
            "|   | GPU  |---------|  PCIe x16 Slot |                            |",
            "|   +------+         +----------------+                            |",
            "|                                                                  |",
            "|                    +----------------+                            |",
            "|                    |  PCIe x1 Slot  |                            |",
            "|                    +----------------+                            |",
            "|                                                                  |",
            "|                    +----------------+                            |",
            "|                    |  PCIe x1 Slot  |                            |",
            "|                    +----------------+                            |",
            "|                                                                  |",
            "+------------------------------------------------------------------+",
            "| Virus Locations:                                                 |",
            "| * Rootkit Virus: OS Kernel         * Firmware Virus: BIOS/UEFI   |",
            "| * Memory Resident Virus: RAM DIMM1 * Packet Sniffer: Network Int |",
            "| * Boot Sector Virus: SSD                                         |",
            "+------------------------------------------------------------------+"
        ]
        
        # Return the motherboard layout as a string
        return "\n".join(motherboard)

    def victory_message(self):
        """Generate victory message when all viruses are quarantined"""
        return """
CONGRATULATIONS! MISSION SUCCESSFUL!

You have successfully located and quarantined all viruses in the system.
The computer architecture is now secure and operating at optimal efficiency.

During your mission, you've explored the inner workings of computer components
and how they interconnect to form a complete system.

Your final statistics:
- Turns taken: {turns}
- Computer components visited: {components}/{total_components}
- Knowledge gained: {knowledge_level}

Thank you for playing KodeKloud Computer Quest!
""".format(
    turns=self.turns,
    components=sum(1 for room in self.game_map.rooms.values() if room.visited),
    total_components=len(self.game_map.rooms),
    knowledge_level=sum(self.player.knowledge.values())
)
    
    def process_cmd(self, cmd_list):
        """
        Process given command
        cmd_list is a list of arguments from user input
        """
        if not cmd_list:
            return "Please enter a command. Type 'help' for available commands."
            
        # Convert all to lowercase for easier parsing
        cmd_list = [word.lower() for word in cmd_list]
        command = cmd_list[0]
        
        # Movement directions
        directions = ['north', 'n', 'south', 's', 'east', 'e', 'west', 'w', 
                     'northeast', 'ne', 'northwest', 'nw', 'southeast', 'se', 
                     'southwest', 'sw', 'up', 'u', 'down', 'd']
        
        # Handle map command
        if command in ['map', 'm']:
            return self.display_map()
            
        # Handle motherboard command
        if command in ['motherboard', 'mb']:
            return self.display_motherboard()
            
        # Handle movement commands (including just typing the direction)
        if command in directions:
            result = self.move(command)
            
        # Handle 'go' command
        elif command == 'go':
            if len(cmd_list) > 1 and cmd_list[1] in directions:
                result = self.move(cmd_list[1])
            else:
                result = "Please specify a valid direction (n, s, e, w, etc.)"
                
        # Handle 'look' command
        elif command == 'look':
            if len(cmd_list) > 1:
                # Look at specific item
                item_name = cmd_list[1]
                result = self.player.look(item_name)
            else:
                # Look around current location
                # Mark component as visited to reveal more technical details
                self.player.location.mark_visited()
                result = self.player.look()
                
        # Handle 'take' command
        elif command == 'take' or command == 'get':
            if len(cmd_list) > 1:
                item_name = cmd_list[1]
                result = self.player.take(item_name)
                self.turns += 1
            else:
                result = "What do you want to take?"
                
        # Handle 'drop' command
        elif command == 'drop':
            if len(cmd_list) > 1:
                item_name = cmd_list[1]
                result = self.player.drop(item_name)
                self.turns += 1
            else:
                result = "What do you want to drop?"
                
        # Handle 'inventory' command
        elif command == 'inventory' or command == 'i':
            if not self.player.items:
                result = "Your system storage is empty."
            else:
                result = "System Storage Contains:\n"
                for item, desc in self.player.items.items():
                    # Show abbreviated description for inventory listing
                    short_desc = desc.split('.')[0] if '.' in desc else desc
                    if len(short_desc) > 50:
                        short_desc = short_desc[:47] + "..."
                    result += f"- {item}: {short_desc}\n"
            
        # Handle 'scan' command
        elif command == 'scan':
            if len(cmd_list) > 1:
                target = cmd_list[1]
                result = self.player.scan(target)
            else:
                result = self.player.scan()
                # Check for game winning conditions
                if len(self.player.found_viruses) == len(self.viruses):
                    self.all_viruses_found = True
            self.turns += 1
            
        # Handle 'advanced-scan' or 'advscan' command
        elif command in ['advanced-scan', 'advscan', 'advanced_scan']:
            if len(cmd_list) > 1:
                target = cmd_list[1]
                result = self.player.advanced_scan(target)
            else:
                result = self.player.advanced_scan()
                # Check for game winning conditions
                if len(self.player.found_viruses) == len(self.viruses):
                    self.all_viruses_found = True
            self.turns += 1
            
        # Handle 'analyze' command
        elif command == 'analyze':
            if len(cmd_list) > 1:
                target = cmd_list[1]
                result = self.player.analyze(target)
                self.turns += 1
            else:
                result = "What do you want to analyze? Usage: analyze [item]"
                
        # Handle 'quarantine' command
        elif command == 'quarantine':
            if len(cmd_list) > 1:
                virus_name = cmd_list[1]
                result = self.player.quarantine(virus_name)
                self.turns += 1
                
                # Check for victory condition
                if len(self.player.quarantined_viruses) == len(self.viruses):
                    self.victory = True
                    result += "\n\n" + self.victory_message()
                    self.game_over = True
                    # In a full implementation, we'd save high scores here
            else:
                result = "Which virus do you want to quarantine?"
                
        # Handle 'status' or 'progress' command
        elif command in ['status', 'progress']:
            result = self.player.check_progress()
        
        # Handle 'achievements' command
        elif command in ['achievements', 'achieve', 'stats']:
            result = self.progress.get_progress_report()
            
        # Handle 'knowledge' command
        elif command == 'knowledge':
            result = self.player.knowledge_report()
            
        # Handle 'read' command
        elif command == 'read':
            if len(cmd_list) > 1:
                item_name = cmd_list[1]
                
                # Check if item is in inventory
                if item_name in self.player.items:
                    content = self.player.items[item_name]
                    if content.startswith('#'):
                        # Format as proper document if it starts with #
                        result = content.replace('# ', '').replace('#', '')
                    else:
                        result = content
                    
                # Check if item is in the room
                elif item_name in self.player.location.items:
                    content = self.player.location.items[item_name]
                    if content.startswith('#'):
                        # Format as proper document if it starts with #
                        result = content.replace('# ', '').replace('#', '')
                    else:
                        result = content
                    
                else:
                    result = f"There is no {item_name} to read here."
            else:
                result = "What do you want to read?"
                
        # Handle 'help' command
        elif command == 'help':
            result = self.show_help()
            
        # Handle 'quit' or 'exit' command
        elif command in ['quit', 'exit', 'q']:
            confirm = input("Are you sure you want to exit? Progress will be lost. (y/n): ").lower()
            if confirm in ['y', 'yes']:
                self.game_over = True
                result = "Exiting KodeKloud Computer Quest. Goodbye!"
            else:
                result = "Continuing mission..."
        
        # Handle 'about' command to show info about a computer component
        elif command == 'about':
            if len(cmd_list) > 1:
                topic = cmd_list[1].lower()
                result = self.get_component_info(topic)
            else:
                result = "What topic would you like information about? Try 'about cpu', 'about memory', etc."
                
        # Handle save/load commands
        elif command == 'save':
            if len(cmd_list) > 1:
                result = self.save_load.save_game(cmd_list[1])
            else:
                result = self.save_load.save_game()
        elif command == 'load':
            if len(cmd_list) > 1:
                result = self.save_load.load_game(cmd_list[1])
            else:
                result = "Please specify a save file to load. Use 'saves' to list available saves."
        elif command in ['saves', 'listsaves']:
            result = self.save_load.list_saves()
        elif command == 'deletesave':
            if len(cmd_list) > 1:
                result = self.save_load.delete_save(cmd_list[1])
            else:
                result = "Please specify a save file to delete."
        
        # Handle visualization commands
        elif command == 'visualize' or command == 'viz':
            if len(cmd_list) > 1:
                viz_type = cmd_list[1].lower()
                result = self.handle_visualization(viz_type)
            else:
                result = self.handle_visualization()
        
        # Handle simulation commands
        elif command == 'simulate' or command == 'sim':
            if len(cmd_list) > 1:
                sim_action = cmd_list[1].lower()
                
                if sim_action == 'cpu':
                    result = self.start_cpu_minigame()
                elif sim_action == 'memory':
                    result = self.start_memory_minigame()
                else:
                    # This is an action for an already running simulation
                    result = self.handle_simulation(sim_action)
            else:
                result = "Please specify a simulation type (cpu, memory) or action (step, toggle, reset, stop)."
                
        else:
            result = f"Command '{command}' not recognized. Type 'help' for available commands."
            
        # Check for new achievements and notify the player
        newly_unlocked = self.progress.update()
        if newly_unlocked:
            result += "\n\nACHIEVEMENT UNLOCKED!\n"
            for achievement in newly_unlocked:
                result += f"- {achievement.name}: {achievement.description}\n"
                
        return result