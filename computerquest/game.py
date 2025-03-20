"""
Game controller for KodeKloud Computer Quest

Main game logic and controller
"""

import time
import random
from computerquest.world.architecture import ComputerArchitecture
from computerquest.mechanics.progress import ProgressSystem
from computerquest.commands import CommandProcessor
from computerquest.utils.helpers import prefix_match, format_box
from computerquest.config import DIRECTION_MAPPING, DIRECTION_NAMES, VIRUS_TYPES

# These will need to be properly implemented in the refactored version
class ComponentVisualizer:
    def render_cpu_text(self):
        return "CPU Visualization placeholder"
        
    def render_memory_hierarchy_text(self):
        return "Memory Hierarchy Visualization placeholder"
        
    def render_network_stack_text(self):
        return "Network Stack Visualization placeholder"
        
    def render_storage_hierarchy_text(self):
        return "Storage Hierarchy Visualization placeholder"

class CPUPipelineMinigame:
    def __init__(self, game):
        self.game = game
        
    def explain(self):
        return "CPU Pipeline Minigame placeholder"
        
    def get_status(self):
        return "CPU Pipeline status"
        
    def step(self):
        return "Advanced pipeline by one step"
        
    def toggle_pipeline(self):
        return "Toggled pipeline mode"
        
    def reset(self):
        return "Reset pipeline simulation"
        
class MemoryHierarchyMinigame:
    def __init__(self, game):
        self.game = game
        
    def explain(self):
        return "Memory Hierarchy Minigame placeholder"

# SaveLoadSystem placeholder (will need to be properly implemented)
class SaveLoadSystem:
    def __init__(self, game):
        self.game = game
        
    def save_game(self, name=None):
        return f"Game saved with name: {name or 'autosave'}"
        
    def load_game(self, name):
        return f"Game loaded: {name}"
        
    def list_saves(self):
        return "Available saved games: [none]"
        
    def delete_save(self, name):
        return f"Deleted save: {name}"

class Game:
    def __init__(self):
        """
        Constructor: Create a KodeKloud Computer Quest game
        Initialize the game world and components
        """
        # Initialize computer architecture
        self.game_map = ComputerArchitecture()
        self.game_map.setup()
        
        # Get player from the map
        self.player = self.game_map.player
        
        # Game state variables
        self.turns = 0
        self.game_over = False
        self.all_viruses_found = False
        self.victory = False
        
        # Initialize the progress tracking system
        self.progress = ProgressSystem(self)
        
        # Initialize visualizer
        self.visualizer = ComponentVisualizer()
        
        # Initialize minigame state
        self.current_minigame = None
        self.current_visualization = None
        
        # Initialize save/load system
        self.save_load = SaveLoadSystem(self)
        
        # Initialize command processor
        self.command_processor = CommandProcessor(self)
        
        # Initialize map grid for tracking visited rooms
        self._init_map_grid()
                
        # Mark the starting room as visited on the map
        for room_id, room in self.game_map.rooms.items():
            if room == self.player.location:
                if room_id in self.map_grid:
                    self.map_grid[room_id]['visited'] = True
                break
                
        # Print welcome message
        self.display_welcome()

    def _init_map_grid(self):
        """Initialize the map grid for tracking visited components"""
        self.map_grid = {}
        
        # CPU and cores
        cpu_components = ['cpu_package', 'core1', 'core1_cu', 'core1_alu', 'core1_registers', 
                         'core1_l1', 'core2', 'core2_cu', 'core2_alu', 'core2_registers', 'core2_l1']
        
        # Cache and memory
        memory_components = ['l2_cache1', 'l2_cache2', 'l3_cache', 'memory_controller',
                            'ram_dimm1', 'ram_dimm2', 'ram_dimm3', 'ram_dimm4']
        
        # Conceptual components
        conceptual_components = ['kernel', 'virtual_memory']
        
        # PCH components
        pch_components = ['pch', 'storage_controller', 'pcie_controller', 
                         'network_interface', 'bios']
        
        # Storage components
        storage_components = ['sata_ports', 'ssd', 'hdd']
        
        # PCIe components
        pcie_components = ['pcie_x16', 'pcie_x1_1', 'pcie_x1_2', 'gpu']
        
        # External ports
        port_components = ['usb_ports', 'ethernet']
        
        # Combine all components
        all_components = (cpu_components + memory_components + conceptual_components + 
                         pch_components + storage_components + pcie_components + port_components)
        
        # Initialize all as not visited
        for component in all_components:
            self.map_grid[component] = {'visited': False}
        
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
                
            # Process command through the command processor
            response = self.command_processor.process(user_input)
            
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
        direction: Direction to move (n, s, e, w, etc.)
        Returns: Description of new location or error message
        """
        # Normalize direction input
        dir_code = DIRECTION_MAPPING.get(direction, direction)
            
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
        Display an interactive map of visited rooms
        Returns: ASCII map showing explored components
        """
        from computerquest.utils.map_renderer import render_map
        
        # Make sure starting room is always marked as visited
        for room_id, room in self.game_map.rooms.items():
            if room == self.player.location:
                if room_id in self.map_grid:
                    self.map_grid[room_id]['visited'] = True
                break
                
        # Generate and return the map
        return render_map(self, self.map_grid)
            
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
        
    def _match_command_prefix(self, cmd):
        """Match command prefix with valid commands, return full command if unique match found"""
        if len(cmd) < 2:
            return cmd  # Don't try to match single-letter commands
            
        # Get all command keys from the command processor
        valid_commands = list(self.command_processor.commands.keys())
        
        # Use the helper function
        return prefix_match(cmd, valid_commands)
            
    def _match_item_prefix(self, item_prefix):
        """Match item prefix with items in current room, return full item name if unique match found"""
        if len(item_prefix) < 2:
            return item_prefix  # Don't try to match single-letter items
            
        # Get all items in current room
        room_items = list(self.player.location.items.keys())
        
        # Use the helper function
        return prefix_match(item_prefix, room_items)
            
    def _match_inventory_item_prefix(self, item_prefix):
        """Match item prefix with items in inventory, return full item name if unique match found"""
        if len(item_prefix) < 2:
            return item_prefix  # Don't try to match single-letter items
            
        # Get all items in inventory
        inventory_items = list(self.player.items.keys())
        
        # Use the helper function
        return prefix_match(item_prefix, inventory_items)