import time
import random
from player import Player
from room import Room
from map import Map
from visualizer import ComponentVisualizer
from minigames import CPUPipelineMinigame, MemoryHierarchyMinigame

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
        Constructor: Create a ComputerQuest game
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
                print("\nThank you for playing ComputerQuest! Goodbye!")
        else:
            print("\nExiting ComputerQuest. Goodbye!")

# This method has been removed since we're now using Map class from map.py

# These methods have been removed since we're now using Map class from map.py

    def display_welcome(self):
        """Display welcome message and game introduction"""
        print("=" * 70)
        print("   █▀▀ █▀█ █▀▄▀█ █▀█ █░█ ▀█▀ █▀▀ █▀█   █▀█ █░█ █▀▀ █▀ ▀█▀   ")
        print("   █▄▄ █▄█ █░▀░█ █▀▀ █▄█ ░█░ ██▄ █▀▄   ▀▀█ █▄█ ██▄ ▄█ ░█░   ")
        print("=" * 70)
        print("\nWelcome to the Computer Architecture Quest!")
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
            
    def show_help(self):
        """Show available commands"""
        help_text = """
COMPUTERQUEST COMMANDS:

Movement:
  go [direction]   - Move between components (n, s, e, w, ne, sw, etc.)
  [direction]      - You can also just type the direction (north, s, east, w)

Exploration:
  look             - Examine your current location
  look [item]      - Examine a specific item
  read [item]      - Read text content of an item

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

Thank you for playing ComputerQuest!
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
                result = "Exiting ComputerQuest. Goodbye!"
            else:
                result = "Continuing mission..."
        
        # Handle 'about' command to show info about a computer component
        elif command == 'about':
            if len(cmd_list) > 1:
                topic = cmd_list[1].lower()
                result = self.get_component_info(topic)
            else:
                result = "What topic would you like information about? Try 'about cpu', 'about memory', etc."
        
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