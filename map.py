import room
import player

class Map:
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.name = "ComputerQuest"

    def makeRooms(self):
        """
        Make the rooms representing computer architecture components
        """
        # Core CPU components
        self.cpu_core = room.Room(
            "CPU Core", 
            "You are inside the main processing core of the CPU. The environment pulses with energy as billions of instructions flow through. The air is electric with the sense of rapid calculations. From here, you can access the control unit, arithmetic logic unit, cache memory, and the system bus.", 
            True, 
            "CPU001"
        )
        self.rooms["cpu_core"] = self.cpu_core
        
        self.control_unit = room.Room(
            "Control Unit",
            "You stand in the control unit. This area coordinates all CPU activities, decoding instructions and directing operations. Status lights blink in complex patterns as the system processes commands. Paths lead to the CPU Core, the registers, and the ALU.",
            True,
            "CU001"
        )
        self.rooms["control_unit"] = self.control_unit
        
        self.alu = room.Room(
            "Arithmetic Logic Unit",
            "The ALU hums with computational activity. Here all calculations are performed - mathematical operations and logical comparisons. Numbers and logical values flow through circuits around you. Connections lead back to the control unit and CPU core.",
            True,
            "ALU001"
        )
        self.rooms["alu"] = self.alu
        
        self.registers = room.Room(
            "Registers",
            "You're in the registers - small, lightning-fast memory units that hold data being actively processed. Each register glows with stored values, changing rapidly as new calculations occur. There's a path back to the control unit and another leading to cache memory.",
            True,
            "REG001"
        )
        self.rooms["registers"] = self.registers
        
        # Memory hierarchy
        self.l1_cache = room.Room(
            "L1 Cache",
            "You've entered the L1 cache - the CPU's closest and fastest memory. Data moves incredibly quickly here, with frequently used instructions and data readily accessible. The space is compact and incredibly efficient. Paths lead to the registers, the L2 cache, and back to the CPU core.",
            True,
            "L1C001"
        )
        self.rooms["l1_cache"] = self.l1_cache
        
        self.l2_cache = room.Room(
            "L2 Cache",
            "The L2 cache stretches around you, larger but slightly slower than L1. It serves as the middle ground in the memory hierarchy. When the CPU can't find data in L1, it looks here next. Connections lead to L1 cache, L3 cache, and the memory controller.",
            True,
            "L2C001"
        )
        self.rooms["l2_cache"] = self.l2_cache
        
        self.l3_cache = room.Room(
            "L3 Cache",
            "You're standing in the expansive L3 cache, the last level of cache memory before main memory. It's much larger but slower than L1 and L2. This shared cache serves all CPU cores. Pathways connect to L2 cache and to the system memory controller.",
            True,
            "L3C001"
        )
        self.rooms["l3_cache"] = self.l3_cache
        
        self.memory_controller = room.Room(
            "Memory Controller",
            "The memory controller bustles with activity, managing the flow of data between the CPU and RAM. It orchestrates read and write operations with precise timing. Connections lead to the system bus, the L3 cache, and RAM.",
            True,
            "MC001"
        )
        self.rooms["memory_controller"] = self.memory_controller
        
        self.ram = room.Room(
            "RAM (Random Access Memory)",
            "You've entered the vast expanse of RAM. Compared to the cache levels, it feels enormous but less frantic. This is where active programs and data reside while the computer is running. Unlike the CPU areas, data here persists only while power flows. Paths lead to the memory controller, virtual memory, and the system bus.",
            True,
            "RAM001"
        )
        self.rooms["ram"] = self.ram
        
        # Connective architecture
        self.system_bus = room.Room(
            "System Bus",
            "You're traveling along the system bus - the main highway of data transfer between major system components. Information packets zoom past you in all directions. From here, you can access the CPU core, the RAM, the expansion buses, and the I/O controllers.",
            True,
            "BUS001"
        )
        self.rooms["system_bus"] = self.system_bus
        
        self.pci_bus = room.Room(
            "PCI Express Bus",
            "You're on the PCI Express bus, a high-speed expansion bus that connects the system to peripheral components. The bandwidth here is impressive, with data flowing in parallel lanes. Connections lead to the system bus, graphics processing unit, and external device controllers.",
            True,
            "PCI001"
        )
        self.rooms["pci_bus"] = self.pci_bus
        
        self.io_controller = room.Room(
            "I/O Controller Hub",
            "You're in the I/O controller hub, managing connections to all external devices. This bustling area handles data flow to and from storage devices, network interfaces, and user input devices. Paths lead to the system bus, storage controllers, and network interfaces.",
            True,
            "IOC001"
        )
        self.rooms["io_controller"] = self.io_controller
        
        # Storage and specialized components
        self.storage_controller = room.Room(
            "Storage Controller",
            "The storage controller manages data flow between the system and persistent storage devices. It translates system requests into the specific protocols needed by different storage media. Paths lead to the I/O controller, solid state drive, and hard disk drive.",
            True,
            "STC001"
        )
        self.rooms["storage_controller"] = self.storage_controller
        
        self.ssd = room.Room(
            "Solid State Drive",
            "You've entered the solid state drive. Unlike the constantly changing memory areas, data here is organized in flash memory cells that retain information even when power is off. The environment is silent but incredibly efficient. A connection leads back to the storage controller.",
            True,
            "SSD001"
        )
        self.rooms["ssd"] = self.ssd
        
        self.hdd = room.Room(
            "Hard Disk Drive",
            "You stand among the mechanical structures of the hard disk drive. Here, data is stored magnetically on spinning platters, accessed by moving read/write heads. You can hear the mechanical movements as data is accessed. A path leads back to the storage controller.",
            True,
            "HDD001"
        )
        self.rooms["hdd"] = self.hdd
        
        self.gpu = room.Room(
            "Graphics Processing Unit",
            "The GPU is a massive parallel processing environment. Thousands of small cores work simultaneously on graphics rendering tasks. Visual data streams all around you, being transformed from mathematical descriptions into rendered images. Connections lead to the PCI Express bus and video memory.",
            True,
            "GPU001"
        )
        self.rooms["gpu"] = self.gpu
        
        self.vram = room.Room(
            "Video Memory (VRAM)",
            "You're inside the video memory, where frame buffers and texture data reside. This specialized memory is optimized for the parallel access patterns needed for graphics processing. The space is filled with image data in various stages of rendering. A path leads back to the GPU.",
            True,
            "VRAM001"
        )
        self.rooms["vram"] = self.vram
        
        self.network_interface = room.Room(
            "Network Interface",
            "You've reached the network interface, the gateway between this computer and the outside world. Data packets are assembled and disassembled here, following precise networking protocols. A path leads back to the I/O controller, and there's what appears to be a portal leading to external networks.",
            True,
            "NET001"
        )
        self.rooms["network_interface"] = self.network_interface
        
        self.bios = room.Room(
            "BIOS/UEFI Firmware",
            "You're in the BIOS/UEFI firmware environment, the fundamental system that initializes hardware during boot. This ancient-seeming area contains the basic instructions that bring the computer to life. Odd symbols and fundamental commands are etched into the walls. A path leads to the system bus.",
            True,
            "BIOS001"
        )
        self.rooms["bios"] = self.bios
        
        # Virtual memory and other conceptual areas
        self.virtual_memory = room.Room(
            "Virtual Memory Manager",
            "You're in the virtual memory management system. Here, the illusion of unlimited memory is maintained by mapping virtual addresses to physical storage. Pages of memory move between RAM and storage as needed. Paths lead to RAM and the storage controllers.",
            True,
            "VM001"
        )
        self.rooms["virtual_memory"] = self.virtual_memory
        
        self.kernel = room.Room(
            "Operating System Kernel",
            "You stand in the kernel space - the core of the operating system. This protected environment controls all hardware resources and provides services to applications. The air of authority is palpable. Paths branch out to nearly all other system components.",
            True,
            "KRN001"
        )
        self.rooms["kernel"] = self.kernel

    def createItems(self):
        """
        Create the items related to computer components and the viruses
        """
        # Tools and useful items
        self.cpu_core.add_items({
            'instruction_manual': '# System Architecture Guide\n\nWelcome to ComputerQuest!\n\nYou are inside a computer system infected with multiple viruses. Your mission is to explore the system, learn about computer architecture, and locate all the viruses hiding in different components.\n\nBasic commands:\n-go : followed by a direction (n, s, e, w, up, down)\n-take : pick up an item\n-look : examine your surroundings or a specific item\n-read : read text content of items\n-scan : use on areas to detect virus presence\n-quarantine : use on viruses once found\n\nThe system has multiple levels, from the CPU to storage to networking. Each area represents a real computer architecture component with its own function. Learn about them as you explore!'
        })
        
        self.control_unit.add_items({
            'decoder_tool': 'An instruction decoder tool that can help analyze suspicious code patterns.'
        })
        
        self.registers.add_items({
            'register_log': 'A log showing recent register state changes. Some unusual patterns are highlighted.'
        })
        
        self.l1_cache.add_items({
            'cache_analyzer': 'A tool for examining cache contents to identify unusual access patterns.'
        })
        
        self.io_controller.add_items({
            'port_scanner': 'A device that can scan I/O ports for unauthorized data transfers.'
        })
        
        self.network_interface.add_items({
            'packet_analyzer': 'A tool that can inspect network packets for malicious content.'
        })
        
        self.hdd.add_items({
            'disk_scanner': 'A comprehensive scanning tool for detecting file system anomalies.'
        })
        
        self.bios.add_items({
            'firmware_validator': 'A specialized tool for verifying firmware integrity.'
        })
        
        # Clues to viruses
        self.alu.add_items({
            'strange_calculation': 'A record of unusual calculation patterns that seem to be used for encryption.'
        })
        
        self.l3_cache.add_items({
            'memory_leak': 'Evidence of a program gradually consuming more memory than it should.'
        })
        
        self.system_bus.add_items({
            'suspicious_packet': 'A data packet with an unusual destination that doesn\'t match any known system component.'
        })
        
        self.virtual_memory.add_items({
            'page_fault_log': 'A log showing an unusually high number of page faults in specific memory regions.'
        })
        
        self.gpu.add_items({
            'shader_anomaly': 'A shader program with code that doesn\'t appear to be related to graphics rendering.'
        })
        
        # The viruses - hidden in specific locations
        self.ssd.add_items({
            'boot_sector_virus': 'A virus that has infected the boot sector of the drive, activating before the operating system loads.'
        })
        
        self.kernel.add_items({
            'rootkit_virus': 'A sophisticated rootkit that has embedded itself in the kernel, hiding its presence from standard detection methods.'
        })
        
        self.ram.add_items({
            'memory_resident_virus': 'A virus that stays entirely in RAM, modifying programs as they're loaded from storage.'
        })
        
        self.bios.add_items({
            'firmware_virus': 'A virus that has infected the system firmware, persisting even through operating system reinstalls.'
        })
        
        self.network_interface.add_items({
            'packet_sniffer_virus': 'A virus that captures and redirects sensitive network traffic.'
        })

    def createNpc(self):
        """
        Create NPCs (could be defensive systems, other programs, etc.)
        """
        pass

    def createPlayer(self):
        """
        Create player object with starting position and inventory
        """
        playerItems = {
            'antivirus_tool': 'A basic antivirus scanner that can detect and quarantine viruses once they\'re found.',
            'system_mapper': 'A tool showing a map of the computer architecture you\'ve explored so far.'
        }
        
        # Start the player in the CPU Core
        self.player = player.Player(self.cpu_core, playerItems, False, "Security Program")

    def connectRooms(self):
        """
        Connect all the rooms according to computer architecture
        """
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

    def setup(self):
        """
        Setup the computer architecture world
        """
        self.makeRooms()
        self.connectRooms()
        self.createItems()
        self.createNpc()
        self.createPlayer()

if __name__ == "__main__":
    init = Map()
    init.setup()