import time
import random
from player import Player
from room import Room

class Game:
    def __init__(self):
        """
        Constructor: Create a ComputerQuest game
        Initialize the game world and components
        """
        # Load rooms (computer components)
        self.rooms = []
        
        # Initialize computer architecture map
        self.init_map()
        
        # Create player and place at entry point (CPU Core)
        entry_room = self.cpu_core
        player_items = {
            'antivirus_tool': 'A basic scanner that can detect and quarantine viruses once found.',
            'system_manual': '# System Architecture Guide\n\nWelcome to ComputerQuest!\n\nYou are inside a computer system infected with viruses. Your mission is to locate and quarantine all viruses hidden throughout the system.\n\nBasic commands:\n-go (n/s/e/w): Move between components\n-look: Examine your surroundings\n-look [item]: Examine a specific item\n-take [item]: Add item to your inventory\n-drop [item]: Remove item from your inventory\n-inventory: List your items\n-scan: Search for viruses in current location\n-scan [item]: Check if a specific item is infected\n-quarantine [virus]: Contain a discovered virus\n-status: Check your progress\n-knowledge: View your computer architecture knowledge\n-help: Show available commands\n\nGood luck, Security Program!'
        }
        self.player = Player(entry_room, player_items, False, "Security Program")
        
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

    def init_map(self):
        """
        Initialize the computer architecture map
        Creating all components and connections
        """
        # Core CPU components
        self.cpu_core = Room(
            "CPU Core", 
            "You are inside the main processing core of the CPU. The environment pulses with energy as billions of instructions flow through. The air is electric with the sense of rapid calculations.", 
            True, 
            "001", 
            False
        )
        self.cpu_core.set_specs(3, ["Instructions", "Opcodes"], 10, 2, 8)
        
        self.control_unit = Room(
            "Control Unit",
            "You stand in the control unit. This area coordinates all CPU activities, decoding instructions and directing operations. Status lights blink in complex patterns as the system processes commands.",
            True,
            "002",
            False
        )
        self.control_unit.set_specs(3, ["Control Signals", "Instructions"], 9, 1, 8)
        
        self.alu = Room(
            "Arithmetic Logic Unit",
            "The ALU hums with computational activity. Here all calculations are performed - mathematical operations and logical comparisons. Numbers and logical values flow through circuits around you.",
            True,
            "003",
            False
        )
        self.alu.set_specs(3, ["Operands", "Results"], 10, 1, 8)
        
        self.registers = Room(
            "Registers",
            "You're in the registers - small, lightning-fast memory units that hold data being actively processed. Each register glows with stored values, changing rapidly as new calculations occur.",
            True,
            "004",
            False
        )
        self.registers.set_specs(3, ["Variables", "Addresses", "Flags"], 10, 3, 9)
        
        # Memory hierarchy
        self.l1_cache = Room(
            "L1 Cache",
            "You've entered the L1 cache - the CPU's closest and fastest memory. Data moves incredibly quickly here, with frequently used instructions and data readily accessible. The space is compact and incredibly efficient.",
            True,
            "010",
            False
        )
        self.l1_cache.set_specs(2, ["Program Code", "Data"], 9, 4, 9)
        
        self.l2_cache = Room(
            "L2 Cache",
            "The L2 cache stretches around you, larger but slightly slower than L1. It serves as the middle ground in the memory hierarchy. When the CPU can't find data in L1, it looks here next.",
            True,
            "011",
            False
        )
        self.l2_cache.set_specs(2, ["Program Code", "Data"], 8, 5, 9)
        
        self.l3_cache = Room(
            "L3 Cache",
            "You're standing in the expansive L3 cache, the last level of cache memory before main memory. It's much larger but slower than L1 and L2. This shared cache serves all CPU cores.",
            True,
            "012",
            False
        )
        self.l3_cache.set_specs(2, ["Program Code", "Data"], 7, 6, 9)
        
        self.memory_controller = Room(
            "Memory Controller",
            "The memory controller bustles with activity, managing the flow of data between the CPU and RAM. It orchestrates read and write operations with precise timing.",
            True,
            "013",
            False
        )
        self.memory_controller.set_specs(2, ["Memory Addresses", "Data"], 7, 3, 8)
        
        self.ram = Room(
            "RAM (Random Access Memory)",
            "You've entered the vast expanse of RAM. Compared to the cache levels, it feels enormous but less frantic. This is where active programs and data reside while the computer is running. Unlike the CPU areas, data here persists only while power flows.",
            True,
            "020",
            False
        )
        self.ram.set_specs(1, ["Program Code", "User Data", "System Data"], 6, 8, 7)
        
        # Connective architecture
        self.system_bus = Room(
            "System Bus",
            "You're traveling along the system bus - the main highway of data transfer between major system components. Information packets zoom past you in all directions.",
            True,
            "030",
            False
        )
        self.system_bus.set_specs(1, ["Data Packets", "Control Signals", "Addresses"], 8, 5, 7)
        
        self.pci_bus = Room(
            "PCI Express Bus",
            "You're on the PCI Express bus, a high-speed expansion bus that connects the system to peripheral components. The bandwidth here is impressive, with data flowing in parallel lanes.",
            True,
            "031",
            False
        )
        self.pci_bus.set_specs(1, ["Device Data", "Control Signals"], 8, 6, 7)
        
        self.io_controller = Room(
            "I/O Controller Hub",
            "You're in the I/O controller hub, managing connections to all external devices. This bustling area handles data flow to and from storage devices, network interfaces, and user input devices.",
            True,
            "032",
            False
        )
        self.io_controller.set_specs(1, ["Device Data", "Control Signals"], 6, 4, 7)
        
        # Storage and specialized components
        self.storage_controller = Room(
            "Storage Controller",
            "The storage controller manages data flow between the system and persistent storage devices. It translates system requests into the specific protocols needed by different storage media.",
            True,
            "040",
            False
        )
        self.storage_controller.set_specs(1, ["File Data", "Storage Commands"], 6, 4, 7)
        
        self.ssd = Room(
            "Solid State Drive",
            "You've entered the solid state drive. Unlike the constantly changing memory areas, data here is organized in flash memory cells that retain information even when power is off. The environment is silent but incredibly efficient.",
            True,
            "041",
            False
        )
        self.ssd.set_specs(1, ["Files", "Boot Data", "Application Data"], 6, 9, 8)
        
        self.hdd = Room(
            "Hard Disk Drive",
            "You stand among the mechanical structures of the hard disk drive. Here, data is stored magnetically on spinning platters, accessed by moving read/write heads. You can hear the mechanical movements as data is accessed.",
            True,
            "042",
            False
        )
        self.hdd.set_specs(1, ["Files", "Archives", "Backups"], 3, 10, 6)
        
        self.gpu = Room(
            "Graphics Processing Unit",
            "The GPU is a massive parallel processing environment. Thousands of small cores work simultaneously on graphics rendering tasks. Visual data streams all around you, being transformed from mathematical descriptions into rendered images.",
            True,
            "050",
            False
        )
        self.gpu.set_specs(2, ["Textures", "Shaders", "Vertex Data"], 9, 7, 7)
        
        self.vram = Room(
            "Video Memory (VRAM)",
            "You're inside the video memory, where frame buffers and texture data reside. This specialized memory is optimized for the parallel access patterns needed for graphics processing. The space is filled with image data in various stages of rendering.",
            True,
            "051",
            False
        )
        self.vram.set_specs(2, ["Frame Buffers", "Textures"], 8, 7, 7)
        
        self.network_interface = Room(
            "Network Interface",
            "You've reached the network interface, the gateway between this computer and the outside world. Data packets are assembled and disassembled here, following precise networking protocols.",
            True,
            "060",
            False
        )
        self.network_interface.set_specs(1, ["Network Packets", "Headers", "Payload Data"], 7, 5, 7)
        
        self.bios = Room(
            "BIOS/UEFI Firmware",
            "You're in the BIOS/UEFI firmware environment, the fundamental system that initializes hardware during boot. This ancient-seeming area contains the basic instructions that bring the computer to life. Odd symbols and fundamental commands are etched into the walls.",
            True,
            "070",
            False
        )
        self.bios.set_specs(3, ["Boot Instructions", "Hardware Configuration"], 5, 3, 9)
        
        # Virtual memory and OS components
        self.virtual_memory = Room(
            "Virtual Memory Manager",
            "You're in the virtual memory management system. Here, the illusion of unlimited memory is maintained by mapping virtual addresses to physical storage. Pages of memory move between RAM and storage as needed.",
            True,
            "080",
            False
        )
        self.virtual_memory.set_specs(2, ["Page Tables", "Memory Mappings"], 4, 8, 7)
        
        self.kernel = Room(
            "Operating System Kernel",
            "You stand in the kernel space - the core of the operating system. This protected environment controls all hardware resources and provides services to applications. The air of authority is palpable.",
            True,
            "090",
            False
        )
        self.kernel.set_specs(3, ["System Calls", "Drivers", "Resource Allocations"], 7, 6, 9)
        
        # Add all rooms to master list
        self.rooms = [
            self.cpu_core, self.control_unit, self.alu, self.registers,
            self.l1_cache, self.l2_cache, self.l3_cache, self.memory_controller, self.ram,
            self.system_bus, self.pci_bus, self.io_controller,
            self.storage_controller, self.ssd, self.hdd,
            self.gpu, self.vram,
            self.network_interface,
            self.bios,
            self.virtual_memory, self.kernel
        ]
        
        # Connect all the rooms (components)
        self.connect_components()
        
        # Add items and viruses to the rooms
        self.add_items_and_viruses()

    def connect_components(self):
        """Connect all computer architecture components"""
        # CPU Core connections
        self.cpu_core.connect_to(self.control_unit, 'n')
        self.cpu_core.connect_to(self.alu, 'e')
        self.cpu_core.connect_to(self.l1_cache, 's')
        self.cpu_core.connect_to(self.system_bus, 'w')
        
        # Control Unit connections
        self.control_unit.connect_to(self.cpu_core, 's')
        self.control_unit.connect_to(self.registers, 'e')
        self.control_unit.connect_to(self.alu, 'se')
        
        # ALU connections
        self.alu.connect_to(self.cpu_core, 'w')
        self.alu.connect_to(self.control_unit, 'nw')
        
        # Registers connections
        self.registers.connect_to(self.control_unit, 'w')
        self.registers.connect_to(self.l1_cache, 's')
        
        # Cache hierarchy connections
        self.l1_cache.connect_to(self.cpu_core, 'n')
        self.l1_cache.connect_to(self.registers, 'n')
        self.l1_cache.connect_to(self.l2_cache, 's')
        
        self.l2_cache.connect_to(self.l1_cache, 'n')
        self.l2_cache.connect_to(self.l3_cache, 's')
        
        self.l3_cache.connect_to(self.l2_cache, 'n')
        self.l3_cache.connect_to(self.memory_controller, 's')
        
        # Memory controller and RAM
        self.memory_controller.connect_to(self.l3_cache, 'n')
        self.memory_controller.connect_to(self.ram, 's')
        self.memory_controller.connect_to(self.system_bus, 'w')
        
        self.ram.connect_to(self.memory_controller, 'n')
        self.ram.connect_to(self.virtual_memory, 'e')
        self.ram.connect_to(self.system_bus, 'w')
        
        # System bus connections (central hub)
        self.system_bus.connect_to(self.cpu_core, 'e')
        self.system_bus.connect_to(self.memory_controller, 'e')
        self.system_bus.connect_to(self.ram, 'e')
        self.system_bus.connect_to(self.pci_bus, 's')
        self.system_bus.connect_to(self.io_controller, 'w')
        self.system_bus.connect_to(self.bios, 'n')
        self.system_bus.connect_to(self.kernel, 'ne')
        
        # PCI and I/O connections
        self.pci_bus.connect_to(self.system_bus, 'n')
        self.pci_bus.connect_to(self.gpu, 'e')
        
        self.io_controller.connect_to(self.system_bus, 'e')
        self.io_controller.connect_to(self.storage_controller, 's')
        self.io_controller.connect_to(self.network_interface, 'w')
        
        # Storage connections
        self.storage_controller.connect_to(self.io_controller, 'n')
        self.storage_controller.connect_to(self.ssd, 'e')
        self.storage_controller.connect_to(self.hdd, 'w')
        self.storage_controller.connect_to(self.virtual_memory, 'ne')
        
        self.ssd.connect_to(self.storage_controller, 'w')
        self.hdd.connect_to(self.storage_controller, 'e')
        
        # GPU and VRAM
        self.gpu.connect_to(self.pci_bus, 'w')
        self.gpu.connect_to(self.vram, 's')
        
        self.vram.connect_to(self.gpu, 'n')
        
        # Other connections
        self.network_interface.connect_to(self.io_controller, 'e')
        
        self.virtual_memory.connect_to(self.ram, 'w')
        self.virtual_memory.connect_to(self.storage_controller, 'sw')
        
        self.bios.connect_to(self.system_bus, 's')
        
        self.kernel.connect_to(self.system_bus, 'sw')

    def add_items_and_viruses(self):
        """
        Add items, tools, and viruses to the computer components
        """
        # Tools and useful items
        self.cpu_core.add_items({
            'processor_manual': 'A technical document describing CPU architecture and operation. It contains information about pipelines, instruction sets, and CPU optimization.'
        })
        
        self.control_unit.add_items({
            'decoder_tool': 'An instruction decoder that can help analyze code patterns and identify suspicious operations.'
        })
        
        self.registers.add_items({
            'register_log': 'A log showing recent register state changes. Some unusual patterns might indicate malicious activity.'
        })
        
        self.l1_cache.add_items({
            'cache_analyzer': 'A tool for examining cache contents to identify unusual access patterns or hidden code.'
        })
        
        self.io_controller.add_items({
            'port_scanner': 'A device that can scan I/O ports for unauthorized data transfers or suspicious activity.'
        })
        
        self.network_interface.add_items({
            'packet_analyzer': 'A tool that can inspect network packets for malicious content or suspicious communication patterns.'
        })
        
        self.hdd.add_items({
            'disk_scanner': 'A comprehensive scanning tool for detecting file system anomalies and hidden data.'
        })
        
        self.bios.add_items({
            'firmware_validator': 'A specialized tool for verifying firmware integrity and detecting unauthorized modifications.'
        })
        
        # Clues to viruses
        self.alu.add_items({
            'strange_calculation': 'A record of unusual calculation patterns that seem to be used for encryption. The patterns don\'t match any known legitimate applications.'
        })
        
        self.l3_cache.add_items({
            'memory_leak': 'Evidence of a program gradually consuming more memory than it should. Memory utilization graphs show irregular patterns.'
        })
        
        self.system_bus.add_items({
            'suspicious_packet': 'A data packet with an unusual destination that doesn\'t match any known system component. The header contains obscured routing information.'
        })
        
        self.virtual_memory.add_items({
            'page_fault_log': 'A log showing an unusually high number of page faults in specific memory regions. The affected areas don\'t correspond to any legitimate software.'
        })
        
        self.gpu.add_items({
            'shader_anomaly': 'A shader program with code that doesn\'t appear to be related to graphics rendering. Hidden within the complex calculations are what look like data exfiltration routines.'
        })
        
        # Educational items about computer architecture
        self.ram.add_items({
            'memory_architecture_guide': '# Memory Hierarchy Guide\n\nRAM (Random Access Memory) is the main memory of a computer system. Unlike storage devices, RAM is volatile, meaning it loses its contents when power is removed.\n\nMemory Hierarchy:\n1. Registers (fastest, smallest)\n2. L1 Cache\n3. L2 Cache\n4. L3 Cache\n5. RAM (slower than cache, larger)\n6. Virtual Memory (uses disk space)\n7. Storage Devices (slowest, largest)\n\nThis hierarchy balances speed, size, and cost to optimize system performance.'
        })
        
        self.system_bus.add_items({
            'bus_topology_map': '# System Bus Architecture\n\nThe system bus is the main pathway for data between major computer components. It consists of:\n\n- Address Bus: Carries memory addresses\n- Data Bus: Carries actual data being processed\n- Control Bus: Carries control signals\n\nSystem buses operate at specific clock speeds and widths (like 64-bit), which determine their bandwidth and performance.'
        })
        
        self.kernel.add_items({
            'os_architecture_primer': '# Operating System Architecture\n\nThe kernel is the core of the operating system, with direct access to hardware.\n\nKernel responsibilities:\n- Process management\n- Memory management\n- Device drivers\n- System calls\n- Security enforcement\n\nUser applications request services from the kernel through system calls rather than accessing hardware directly. This provides security and abstraction.'
        })
        
        # The viruses - hidden in specific locations
        self.ssd.add_items({
            'boot_sector_virus': 'A virus that has infected the boot sector of the drive, activating before the operating system loads. It can manipulate system startup and hide other malicious code.'
        })
        
        self.kernel.add_items({
            'rootkit_virus': 'A sophisticated rootkit that has embedded itself in the kernel, hiding its presence from standard detection methods. It has elevated privileges to manipulate system behavior.'
        })
        
        self.ram.add_items({
            'memory_resident_virus': 'A virus that stays entirely in RAM, modifying programs as they\'re loaded from storage. It leaves no traces on disk, making it difficult to detect through conventional scans.'
        })
        
        self.bios.add_items({
            'firmware_virus': 'A virus that has infected the system firmware, persisting even through operating system reinstalls. It can manipulate hardware initialization and compromise the system from the earliest boot stages.'
        })
        
        self.network_interface.add_items({
            'packet_sniffer_virus': 'A virus that captures and redirects sensitive network traffic. It can intercept data before encryption or after decryption, allowing it to steal credentials and sensitive information.'
        })

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
  quarantine [virus] - Contain a discovered virus

Information:
  status           - Check your virus discovery progress
  knowledge        - View your computer architecture knowledge
  about [topic]    - Get information about a computer component
  
System:
  help             - Show this help message
  quit             - Exit the game
"""
        return help_text
        
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
    components=sum(1 for room in self.rooms if room.visited),
    total_components=len(self.rooms),
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
            return self.move(command)
            
        # Handle 'go' command
        elif command == 'go':
            if len(cmd_list) > 1 and cmd_list[1] in directions:
                return self.move(cmd_list[1])
            else:
                return "Please specify a valid direction (n, s, e, w, etc.)"
                
        # Handle 'look' command
        elif command == 'look':
            if len(cmd_list) > 1:
                # Look at specific item
                item_name = cmd_list[1]
                return self.player.look(item_name)
            else:
                # Look around current location
                # Mark component as visited to reveal more technical details
                self.player.location.mark_visited()
                return self.player.look()
                
        # Handle 'take' command
        elif command == 'take' or command == 'get':
            if len(cmd_list) > 1:
                item_name = cmd_list[1]
                return self.player.take(item_name)
            else:
                return "What do you want to take?"
                
        # Handle 'drop' command
        elif command == 'drop':
            if len(cmd_list) > 1:
                item_name = cmd_list[1]
                return self.player.drop(item_name)
            else:
                return "What do you want to drop?"
                
        # Handle 'inventory' command
        elif command == 'inventory' or command == 'i':
            if not self.player.items:
                return "Your system storage is empty."
            
            result = "System Storage Contains:\n"
            for item, desc in self.player.items.items():
                # Show abbreviated description for inventory listing
                short_desc = desc.split('.')[0] if '.' in desc else desc
                if len(short_desc) > 50:
                    short_desc = short_desc[:47] + "..."
                result += f"- {item}: {short_desc}\n"
            return result
            
        # Handle 'scan' command
        elif command == 'scan':
            if len(cmd_list) > 1:
                target = cmd_list[1]
                return self.player.scan(target)
            else:
                result = self.player.scan()
                # Check for game winning conditions
                if len(self.player.found_viruses) == len(self.viruses):
                    self.all_viruses_found = True
                return result
                
        # Handle 'quarantine' command
        elif command == 'quarantine':
            if len(cmd_list) > 1:
                virus_name = cmd_list[1]
                result = self.player.quarantine(virus_name)
                
                # Check for victory condition
                if len(self.player.quarantined_viruses) == len(self.viruses):
                    self.victory = True
                    result += "\n\n" + self.victory_message()
                    self.game_over = True
                    # In a full implementation, we'd save high scores here
                    
                return result
            else:
                return "Which virus do you want to quarantine?"
                
        # Handle 'status' or 'progress' command
        elif command in ['status', 'progress']:
            return self.player.check_progress()
            
        # Handle 'knowledge' command
        elif command == 'knowledge':
            return self.player.knowledge_report()
            
        # Handle 'read' command
        elif command == 'read':
            if len(cmd_list) > 1:
                item_name = cmd_list[1]
                
                # Check if item is in inventory
                if item_name in self.player.items:
                    content = self.player.items[item_name]
                    if content.startswith('#'):
                        # Format as proper document if it starts with #
                        return content.replace('# ', '').replace('#', '')
                    else:
                        return content
                    
                # Check if item is in the room
                elif item_name in self.player.location.items:
                    content = self.player.location.items[item_name]
                    if content.startswith('#'):
                        # Format as proper document if it starts with #
                        return content.replace('# ', '').replace('#', '')
                    else:
                        return content
                    
                else:
                    return f"There is no {item_name} to read here."
            else:
                return "What do you want to read?"
                
        # Handle 'help' command
        elif command == 'help':
            return self.show_help()
            
        # Handle 'quit' or 'exit' command
        elif command in ['quit', 'exit', 'q']:
            confirm = input("Are you sure you want to exit? Progress will be lost. (y/n): ").lower()
            if confirm in ['y', 'yes']:
                self.game_over = True
                return "Exiting ComputerQuest. Goodbye!"
            else:
                return "Continuing mission..."
        
        # Handle 'about' command to show info about a computer component
        elif command == 'about':
            if len(cmd_list) > 1:
                topic = cmd_list[1].lower()
                return self.get_component_info(topic)
            else:
                return "What topic would you like information about? Try 'about cpu', 'about memory', etc."
                
        else:
            return f"Command '{command}' not recognized. Type 'help' for available commands."