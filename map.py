import room
import player

class Map:
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.name = "ComputerQuest"

    def makeRooms(self):
        """
        Make the rooms representing modern computer architecture components
        """
        # CPU Package components
        self.cpu_package = room.Room(
            "CPU Package", 
            "You are inside the main CPU package, the brain of the computer. This sophisticated silicon die houses multiple cores, cache memory levels, and the integrated memory controller. The environment hums with activity as billions of calculations occur every second.", 
            True, 
            "CPU000"
        )
        self.rooms["cpu_package"] = self.cpu_package
        
        # Core 1 components
        self.core1 = room.Room(
            "Core 1", 
            "You're inside the first CPU core. This processing unit contains its own control unit, ALU, registers, and L1 cache. The air crackles with electrical impulses as instructions are decoded and executed.", 
            True, 
            "CORE1"
        )
        self.rooms["core1"] = self.core1
        
        self.core1_cu = room.Room(
            "Core 1 Control Unit",
            "The control unit of Core 1 coordinates operations, fetching and decoding instructions. Status indicators flash in complex patterns as it orchestrates the execution pipeline.",
            True,
            "CU001"
        )
        self.rooms["core1_cu"] = self.core1_cu
        
        self.core1_alu = room.Room(
            "Core 1 ALU",
            "The Arithmetic Logic Unit of Core 1 performs all mathematical and logical operations. Numbers and boolean values flow through circuits as computations occur at incredible speed.",
            True,
            "ALU001"
        )
        self.rooms["core1_alu"] = self.core1_alu
        
        self.core1_registers = room.Room(
            "Core 1 Registers",
            "These small, ultra-fast storage locations hold data being actively processed by Core 1. Each register glows with changing values as operations proceed.",
            True,
            "REG001"
        )
        self.rooms["core1_registers"] = self.core1_registers
        
        self.core1_l1 = room.Room(
            "Core 1 L1 Cache",
            "The Level 1 cache for Core 1 - the fastest and smallest memory in the hierarchy. Split into instruction and data sections, it provides near-instant access to frequently used information.",
            True,
            "L1C001"
        )
        self.rooms["core1_l1"] = self.core1_l1
        
        # Core 2 components (similar structure)
        self.core2 = room.Room(
            "Core 2", 
            "You're inside the second CPU core. Like Core 1, this processing unit contains its own control unit, ALU, registers, and L1 cache, allowing parallel execution of instructions.", 
            True, 
            "CORE2"
        )
        self.rooms["core2"] = self.core2
        
        self.core2_cu = room.Room(
            "Core 2 Control Unit",
            "The control unit of Core 2 coordinates operations, fetching and decoding instructions. Status indicators flash in complex patterns as it orchestrates the execution pipeline.",
            True,
            "CU002"
        )
        self.rooms["core2_cu"] = self.core2_cu
        
        self.core2_alu = room.Room(
            "Core 2 ALU",
            "The Arithmetic Logic Unit of Core 2 performs all mathematical and logical operations. Numbers and boolean values flow through circuits as computations occur at incredible speed.",
            True,
            "ALU002"
        )
        self.rooms["core2_alu"] = self.core2_alu
        
        self.core2_registers = room.Room(
            "Core 2 Registers",
            "These small, ultra-fast storage locations hold data being actively processed by Core 2. Each register glows with changing values as operations proceed.",
            True,
            "REG002"
        )
        self.rooms["core2_registers"] = self.core2_registers
        
        self.core2_l1 = room.Room(
            "Core 2 L1 Cache",
            "The Level 1 cache for Core 2 - the fastest and smallest memory in the hierarchy. Split into instruction and data sections, it provides near-instant access to frequently used information.",
            True,
            "L1C002"
        )
        self.rooms["core2_l1"] = self.core2_l1
        
        # Level 2 Cache
        self.l2_cache1 = room.Room(
            "Core 1 L2 Cache",
            "The L2 cache for Core 1 - larger but slightly slower than L1. This dedicated cache serves only this core, providing a middle tier in the memory hierarchy.",
            True,
            "L2C001"
        )
        self.rooms["l2_cache1"] = self.l2_cache1
        
        self.l2_cache2 = room.Room(
            "Core 2 L2 Cache",
            "The L2 cache for Core 2 - similar to Core 1's L2 cache, it provides dedicated secondary caching for this core only.",
            True,
            "L2C002"
        )
        self.rooms["l2_cache2"] = self.l2_cache2
        
        # L3 Cache (shared)
        self.l3_cache = room.Room(
            "L3 Cache",
            "The Level 3 cache, shared between all CPU cores. Much larger than L1 or L2, but slower. This serves as the last line of cache before memory requests must go to RAM.",
            True,
            "L3C000"
        )
        self.rooms["l3_cache"] = self.l3_cache
        
        # Memory Controller
        self.memory_controller = room.Room(
            "Memory Controller",
            "The integrated memory controller manages all communication between the CPU and RAM. Once a separate component, it's now built into the CPU package for improved performance.",
            True,
            "MC000"
        )
        self.rooms["memory_controller"] = self.memory_controller
        
        # RAM DIMMs
        self.ram_dimm1 = room.Room(
            "RAM DIMM 1",
            "You're inside the first RAM module. This volatile memory stores active programs and data. The space is vast compared to caches, with electrical charges representing binary data.",
            True,
            "RAM001"
        )
        self.rooms["ram_dimm1"] = self.ram_dimm1
        
        self.ram_dimm2 = room.Room(
            "RAM DIMM 2",
            "The second RAM module, identical to DIMM 1 but addressing a different memory range. Together with the other modules, they form the system's main memory.",
            True,
            "RAM002"
        )
        self.rooms["ram_dimm2"] = self.ram_dimm2
        
        self.ram_dimm3 = room.Room(
            "RAM DIMM 3",
            "The third RAM module in the system, expanding the total memory capacity available to programs.",
            True,
            "RAM003"
        )
        self.rooms["ram_dimm3"] = self.ram_dimm3
        
        self.ram_dimm4 = room.Room(
            "RAM DIMM 4",
            "The fourth RAM module, completing the system's memory configuration. Data moves constantly between here and the CPU as programs execute.",
            True,
            "RAM004"
        )
        self.rooms["ram_dimm4"] = self.ram_dimm4
        
        # OS Kernel (conceptual)
        self.kernel = room.Room(
            "OS Kernel",
            "The core of the operating system, loaded into RAM at boot. This protected environment controls hardware resources and provides services to applications. Though residing in RAM physically, it appears as a distinct environment.",
            True,
            "KRN001"
        )
        self.rooms["kernel"] = self.kernel
        
        # Virtual Memory (conceptual)
        self.virtual_memory = room.Room(
            "Virtual Memory",
            "A conceptual space where the operating system creates the illusion of more memory than physically available. Pages of data move between RAM and storage as needed.",
            True,
            "VM001"
        )
        self.rooms["virtual_memory"] = self.virtual_memory
        
        # PCH components
        self.pch = room.Room(
            "Platform Controller Hub",
            "You've entered the PCH - the modern replacement for the traditional Northbridge and Southbridge chipsets. This hub manages most of the computer's I/O functions.",
            True,
            "PCH001"
        )
        self.rooms["pch"] = self.pch
        
        self.storage_controller = room.Room(
            "Storage Controller",
            "This component within the PCH manages all storage devices. It translates system requests into the specific protocols needed by different storage media.",
            True,
            "STC001"
        )
        self.rooms["storage_controller"] = self.storage_controller
        
        self.pcie_controller = room.Room(
            "PCIe Controller",
            "The PCIe Controller manages the high-speed expansion slots used for graphics cards and other peripherals. Information flows through multiple lanes at different speeds based on the connected device's capabilities.",
            True,
            "PCIE001"
        )
        self.rooms["pcie_controller"] = self.pcie_controller
        
        self.network_interface = room.Room(
            "Network Interface",
            "The network controller enables communication with other computers. Data packets are assembled and disassembled here, following precise networking protocols.",
            True,
            "NET001"
        )
        self.rooms["network_interface"] = self.network_interface
        
        self.bios = room.Room(
            "BIOS/UEFI Flash",
            "The firmware that initializes hardware during boot. This ancient-seeming area contains the basic instructions that bring the computer to life.",
            True,
            "BIOS001"
        )
        self.rooms["bios"] = self.bios
        
        # Storage components
        self.sata_ports = room.Room(
            "SATA Ports",
            "The connection points for storage devices. These standardized interfaces allow the system to communicate with SSDs and HDDs.",
            True,
            "SATA001"
        )
        self.rooms["sata_ports"] = self.sata_ports
        
        self.ssd = room.Room(
            "Solid State Drive",
            "The system's primary storage device. Unlike the constantly changing memory areas, data here is organized in flash memory cells that retain information when powered off.",
            True,
            "SSD001"
        )
        self.rooms["ssd"] = self.ssd
        
        self.hdd = room.Room(
            "Hard Disk Drive",
            "The mechanical storage device with spinning platters and moving read/write heads. While slower than the SSD, it offers larger capacity for data storage.",
            True,
            "HDD001"
        )
        self.rooms["hdd"] = self.hdd
        
        # PCIe slots and GPU
        self.pcie_x16 = room.Room(
            "PCIe x16 Slot",
            "The high-bandwidth expansion slot primarily used for graphics cards. 16 lanes of data can transfer simultaneously, enabling the fastest possible communication.",
            True,
            "PCIEX16"
        )
        self.rooms["pcie_x16"] = self.pcie_x16
        
        self.pcie_x1_1 = room.Room(
            "PCIe x1 Slot 1",
            "A smaller expansion slot with a single data lane, used for less bandwidth-intensive devices like sound cards or additional USB controllers.",
            True,
            "PCIEX11"
        )
        self.rooms["pcie_x1_1"] = self.pcie_x1_1
        
        self.pcie_x1_2 = room.Room(
            "PCIe x1 Slot 2",
            "Another single-lane expansion slot, identical to the first PCIe x1 slot but at a different physical location on the motherboard.",
            True,
            "PCIEX12"
        )
        self.rooms["pcie_x1_2"] = self.pcie_x1_2
        
        self.gpu = room.Room(
            "Graphics Processing Unit",
            "The GPU is a massive parallel processing environment. Thousands of small cores work simultaneously on graphics rendering tasks. Visual data streams all around you.",
            True,
            "GPU001"
        )
        self.rooms["gpu"] = self.gpu
        
        # External ports
        self.usb_ports = room.Room(
            "USB Ports",
            "The connection points for external USB devices. These versatile interfaces support a wide variety of peripherals.",
            True,
            "USB001"
        )
        self.rooms["usb_ports"] = self.usb_ports
        
        self.ethernet = room.Room(
            "Ethernet Port",
            "The connection point for wired networking. High-speed data transfers occur here, linking this computer to the broader network.",
            True,
            "ETH001"
        )
        self.rooms["ethernet"] = self.ethernet

    def createItems(self):
        """
        Create the items related to computer components and the viruses
        """
        # Tools and useful items
        self.cpu_package.add_items({
            'instruction_manual': '# System Architecture Guide\n\nWelcome to ComputerQuest!\n\nYou are inside a computer system infected with multiple viruses. Your mission is to explore the system, learn about computer architecture, and locate all the viruses hiding in different components.\n\nBasic commands:\n-go : followed by a direction (n, s, e, w, up, down)\n-take : pick up an item\n-look : examine your surroundings or a specific item\n-read : read text content of items\n-scan : use on areas to detect virus presence\n-quarantine : use on viruses once found\n\nThe system has multiple levels, from the CPU to storage to networking. Each area represents a real computer architecture component with its own function. Learn about them as you explore!'
        })
        
        self.core1_cu.add_items({
            'decoder_tool': 'An instruction decoder tool that can help analyze suspicious code patterns.'
        })
        
        self.core1_registers.add_items({
            'register_log': 'A log showing recent register state changes. Some unusual patterns are highlighted.'
        })
        
        # Add items to Core 2 components
        self.core2_cu.add_items({
            'parallel_instructions': 'A guide showing how the control unit manages parallel instruction execution across multiple cores.'
        })
        
        self.core2_alu.add_items({
            'vector_operations': 'Documentation about SIMD (Single Instruction, Multiple Data) vector operations that process multiple data points simultaneously.'
        })
        
        self.core2_registers.add_items({
            'thread_state': 'A snapshot of register states showing how different threads maintain separate execution contexts.'
        })
        
        # Clues and viruses - note the new locations matching the updated architecture
        self.core1_alu.add_items({
            'strange_calculation': 'A record of unusual calculation patterns that seem to be used for encryption.'
        })
        
        self.l3_cache.add_items({
            'memory_leak': 'Evidence of a program gradually consuming more memory than it should.'
        })
        
        # The viruses - in their specific locations matching the updated diagram
        self.ssd.add_items({
            'boot_sector_virus': 'A virus that has infected the boot sector of the drive, activating before the operating system loads.'
        })
        
        self.kernel.add_items({
            'rootkit_virus': 'A sophisticated rootkit that has embedded itself in the kernel, hiding its presence from standard detection methods.'
        })
        
        self.ram_dimm1.add_items({
            'memory_resident_virus': 'A virus that stays entirely in RAM, modifying programs as they are loaded from storage.'
        })
        
        self.bios.add_items({
            'firmware_virus': 'A virus that has infected the system firmware, persisting even through operating system reinstalls.'
        })
        
        self.network_interface.add_items({
            'packet_sniffer_virus': 'A virus that captures and redirects sensitive network traffic.'
        })

    def createPlayer(self):
        """
        Create player object with starting position and inventory
        """
        playerItems = {
            'antivirus_tool': 'A basic antivirus scanner that can detect and quarantine viruses once they\'re found.',
            'system_mapper': 'A tool showing a map of the computer architecture you\'ve explored so far.'
        }
        
        # Start the player in the CPU Package
        self.player = player.Player(self.cpu_package, playerItems, False, "Security Program")

    def connectRooms(self):
        """
        Connect all the rooms according to modern computer architecture
        """
        # Connect CPU Package to cores and caches
        self.cpu_package.connect_to(self.core1, 'n')
        self.cpu_package.connect_to(self.core2, 'ne')
        self.cpu_package.connect_to(self.l3_cache, 's')
        
        # Connect Core 1 to its components
        self.core1.connect_to(self.core1_cu, 'n')
        self.core1.connect_to(self.core1_alu, 'e')
        self.core1.connect_to(self.core1_registers, 'w')
        self.core1.connect_to(self.core1_l1, 's')
        self.core1.connect_to(self.l2_cache1, 'se')
        
        # Add return connections for Core 1 components
        self.core1_cu.connect_to(self.core1, 's')
        self.core1_alu.connect_to(self.core1, 'w')
        self.core1_registers.connect_to(self.core1, 'e')
        self.core1_l1.connect_to(self.core1, 'n')
        
        # Connect Core 2 to its components
        self.core2.connect_to(self.core2_cu, 'n')
        self.core2.connect_to(self.core2_alu, 'e')
        self.core2.connect_to(self.core2_registers, 'w')
        self.core2.connect_to(self.core2_l1, 's')
        self.core2.connect_to(self.l2_cache2, 'sw')
        self.core2.connect_to(self.cpu_package, 'sw')
        
        # Add return connections for Core 2 components
        self.core2_cu.connect_to(self.core2, 's')
        self.core2_alu.connect_to(self.core2, 'w')
        self.core2_registers.connect_to(self.core2, 'e')
        self.core2_l1.connect_to(self.core2, 'n')
        
        # Connect L2 and L3 caches
        self.l2_cache1.connect_to(self.core1, 'nw')  # Return path to Core 1
        self.l2_cache1.connect_to(self.l3_cache, 's')
        self.l2_cache2.connect_to(self.core2, 'n')   # Return path to Core 2
        self.l2_cache2.connect_to(self.l3_cache, 's')
        
        # Connect L3 to Memory Controller and back to CPU Package
        self.l3_cache.connect_to(self.memory_controller, 's')
        self.l3_cache.connect_to(self.cpu_package, 'n')  # Return path
        
        # Connect Memory Controller to RAM
        self.memory_controller.connect_to(self.ram_dimm1, 'w')
        self.memory_controller.connect_to(self.ram_dimm2, 'sw')
        self.memory_controller.connect_to(self.ram_dimm3, 'nw')
        self.memory_controller.connect_to(self.ram_dimm4, 'n')
        self.memory_controller.connect_to(self.l3_cache, 'n')  # Return path
        
        # Connect RAM to conceptual components and back to memory controller
        self.ram_dimm1.connect_to(self.kernel, 'w')
        self.ram_dimm1.connect_to(self.memory_controller, 'e')  # Return path
        
        self.ram_dimm2.connect_to(self.virtual_memory, 'w')
        self.ram_dimm2.connect_to(self.memory_controller, 'ne')  # Return path
        
        self.ram_dimm3.connect_to(self.memory_controller, 'se')  # Return path
        self.ram_dimm4.connect_to(self.memory_controller, 's')   # Return path
        
        # Connect conceptual components back to RAM
        self.kernel.connect_to(self.ram_dimm1, 'e')
        self.virtual_memory.connect_to(self.ram_dimm2, 'e')
        
        # Connect CPU Package to PCH via DMI Link (bidirectional)
        self.cpu_package.connect_to(self.pch, 'd')  # Down represents the DMI Link
        self.pch.connect_to(self.cpu_package, 'u')  # Up to return to CPU
        
        # Connect PCH to its internal components (with return paths)
        self.pch.connect_to(self.storage_controller, 'n')
        self.storage_controller.connect_to(self.pch, 's')  # Return path
        
        self.pch.connect_to(self.pcie_controller, 'e')
        self.pcie_controller.connect_to(self.pch, 'w')  # Return path
        
        self.pch.connect_to(self.network_interface, 's')
        self.network_interface.connect_to(self.pch, 'n')  # Return path
        
        self.pch.connect_to(self.bios, 'w')
        self.bios.connect_to(self.pch, 'e')  # Return path
        
        # Connect storage components (with return paths)
        self.storage_controller.connect_to(self.sata_ports, 'w')
        self.sata_ports.connect_to(self.storage_controller, 'e')  # Return path
        
        self.sata_ports.connect_to(self.ssd, 'nw')
        self.ssd.connect_to(self.sata_ports, 'se')  # Return path
        
        self.sata_ports.connect_to(self.hdd, 'sw')
        self.hdd.connect_to(self.sata_ports, 'ne')  # Return path
        
        # Connect PCIe components (with return paths)
        self.pcie_controller.connect_to(self.pcie_x16, 's')
        self.pcie_x16.connect_to(self.pcie_controller, 'n')  # Return path
        
        self.pcie_controller.connect_to(self.pcie_x1_1, 'se')
        self.pcie_x1_1.connect_to(self.pcie_controller, 'nw')  # Return path
        
        self.pcie_controller.connect_to(self.pcie_x1_2, 'sw')
        self.pcie_x1_2.connect_to(self.pcie_controller, 'ne')  # Return path
        
        self.pcie_x16.connect_to(self.gpu, 'w')
        self.gpu.connect_to(self.pcie_x16, 'e')  # Return path
        
        # Connect external ports (with return paths)
        self.pch.connect_to(self.usb_ports, 'ne')
        self.usb_ports.connect_to(self.pch, 'sw')  # Return path
        
        self.pch.connect_to(self.ethernet, 'se')
        self.ethernet.connect_to(self.pch, 'nw')  # Return path
        
        # Connect Virtual Memory to storage (conceptual link)
        self.virtual_memory.connect_to(self.storage_controller, 's')
        self.storage_controller.connect_to(self.virtual_memory, 'n')  # Return path

    def setup(self):
        """
        Setup the modern computer architecture world
        """
        self.makeRooms()
        self.connectRooms()
        self.createItems()
        self.createPlayer()

if __name__ == "__main__":
    init = Map()
    init.setup()