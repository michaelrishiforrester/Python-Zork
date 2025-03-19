#!/usr/bin/env python3
"""
ComponentVisualizer for ComputerQuest - Provides visual representations of computer components
"""

import math
import random

class ComponentVisualizer:
    """
    Visualizes computer components to enhance educational experience
    Note: This class has dependencies on Pygame but will operate in text-only mode without it
    """
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.surface = None
        self.text_mode = True
        
        # Try to import pygame, fall back to text mode if unavailable
        try:
            import pygame
            import pygame.font
            self.pygame = pygame
            self.surface = pygame.Surface((width, height))
            self.text_mode = False
            
            # Initialize font
            pygame.font.init()
            self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 18)
            self.small_font = pygame.font.SysFont('Arial', 14)
            
        except ImportError:
            print("Pygame not available - visualizations will be shown in text format")
        
        # Colors
        self.colors = {
            "cpu": (220, 100, 100),  # Red
            "memory": (100, 220, 100),  # Green
            "storage": (100, 100, 220),  # Blue
            "network": (220, 220, 100),  # Yellow
            "bus": (220, 100, 220),  # Purple
            "io": (100, 220, 220),  # Cyan
            "background": (30, 30, 50),  # Dark blue
            "text": (240, 240, 240),  # Light gray
            "highlight": (255, 255, 100)  # Bright yellow
        }
        
        # Animation variables
        self.animation_ticks = 0
        self.particles = []
    
    def render_cpu(self, clock_speed=3.6, cores=4, cache=8):
        """Visualize CPU architecture"""
        if self.text_mode:
            return self.render_cpu_text(clock_speed, cores, cache)
            
        # If running in graphical mode, use pygame for visualization    
        self.surface.fill(self.colors["background"])
        
        # CPU dimensions
        cpu_width = 300
        cpu_height = 300
        cpu_x = (self.width - cpu_width) // 2
        cpu_y = (self.height - cpu_height) // 2
        
        # Draw CPU package
        self.pygame.draw.rect(self.surface, self.colors["cpu"], 
                        (cpu_x, cpu_y, cpu_width, cpu_height))
        self.pygame.draw.rect(self.surface, self.colors["text"], 
                        (cpu_x, cpu_y, cpu_width, cpu_height), 3)
        
        # Draw CPU cores
        core_width = cpu_width // 3
        core_height = cpu_height // 3
        
        for i in range(cores):
            row = i // 2
            col = i % 2
            core_x = cpu_x + core_width * col + core_width//2
            core_y = cpu_y + core_height * row + core_height//2
            
            # Core body
            self.pygame.draw.rect(self.surface, (240, 240, 240), 
                            (core_x - core_width//3, core_y - core_height//3, 
                             core_width//1.5, core_height//1.5))
            
            # Core details
            self.pygame.draw.line(self.surface, (50, 50, 50), 
                            (core_x - core_width//4, core_y), 
                            (core_x + core_width//4, core_y), 2)
            self.pygame.draw.line(self.surface, (50, 50, 50), 
                            (core_x, core_y - core_height//4), 
                            (core_x, core_y + core_height//4), 2)
            
            # Core label
            core_label = self.small_font.render(f"Core {i+1}", True, (0, 0, 0))
            self.surface.blit(core_label, 
                             (core_x - core_label.get_width()//2, 
                              core_y + core_height//4 + 5))
        
        # Draw cache
        cache_height = cpu_height // 6
        cache_y = cpu_y + cpu_height - cache_height - 10
        
        self.pygame.draw.rect(self.surface, (150, 200, 255), 
                        (cpu_x + 20, cache_y, cpu_width - 40, cache_height))
        cache_label = self.small_font.render(f"L3 Cache ({cache}MB)", True, (0, 0, 0))
        self.surface.blit(cache_label, 
                         (cpu_x + cpu_width//2 - cache_label.get_width()//2, 
                          cache_y + cache_height//2 - cache_label.get_height()//2))
        
        # Draw CPU pins
        for i in range(20):
            pin_x = cpu_x + (i * 15) + 10
            self.pygame.draw.line(self.surface, (200, 200, 200), 
                            (pin_x, cpu_y + cpu_height), 
                            (pin_x, cpu_y + cpu_height + 15), 2)
        
        # Draw title and specs
        title = self.title_font.render("CPU Architecture", True, self.colors["text"])
        self.surface.blit(title, (self.width//2 - title.get_width()//2, 20))
        
        specs = self.text_font.render(f"Clock Speed: {clock_speed}GHz | Cores: {cores} | Cache: {cache}MB", 
                                     True, self.colors["text"])
        self.surface.blit(specs, (self.width//2 - specs.get_width()//2, 50))
        
        # Draw clock cycle animation
        self.animation_ticks += 1
        cycle_x = 100
        cycle_y = 100
        cycle_radius = 30
        
        if cores >= 1:
            angle = (self.animation_ticks % 60) * 6  # 6 degrees per tick
            end_x = cycle_x + int(math.cos(math.radians(angle)) * cycle_radius)
            end_y = cycle_y + int(math.sin(math.radians(angle)) * cycle_radius)
            
            self.pygame.draw.circle(self.surface, (50, 50, 50), (cycle_x, cycle_y), cycle_radius, 1)
            self.pygame.draw.line(self.surface, self.colors["highlight"], 
                            (cycle_x, cycle_y), (end_x, end_y), 2)
            
            clock_label = self.small_font.render("Clock", True, self.colors["text"])
            self.surface.blit(clock_label, (cycle_x - clock_label.get_width()//2, 
                                           cycle_y - cycle_radius - 20))
        
        # Educational text
        info_text = [
            "CPU (Central Processing Unit):",
            "- Executes instructions to process data",
            "- Contains multiple cores for parallel processing",
            "- Uses cache memory for faster data access",
            "- Clock speed determines how many cycles per second",
            "- Connected to system via socket on motherboard"
        ]
        
        for i, line in enumerate(info_text):
            text = self.small_font.render(line, True, self.colors["text"])
            self.surface.blit(text, (20, self.height - 150 + i*20))
        
        return self.surface

    def render_cpu_text(self, clock_speed=3.6, cores=4, cache=8):
        """Visualize CPU architecture in text-only mode"""
        result = "++" + "-" * 50 + "++\n"
        result += "|" + "CPU ARCHITECTURE".center(52) + "|\n"
        result += "|" + f"Clock Speed: {clock_speed}GHz | Cores: {cores} | Cache: {cache}MB".center(52) + "|\n"
        result += "+" + "-" * 50 + "+\n"
        
        # ASCII art CPU
        cpu_art = [
            "    +---------------------------+    ",
            "    |                           |    ",
            "    |    +-----+     +-----+    |    ",
            "    |    |CPU 1|     |CPU 2|    |    ",
            "    |    +-----+     +-----+    |    ",
            "    |                           |    ",
            "    |    +-----+     +-----+    |    ",
            "    |    |CPU 3|     |CPU 4|    |    ",
            "    |    +-----+     +-----+    |    ",
            "    |                           |    ",
            "    |    +-------------------+  |    ",
            "    |    |     L3 Cache      |  |    ",
            "    |    +-------------------+  |    ",
            "    |                           |    ",
            "    +---------------------------+    ",
            "       | | | | | | | | | | | |      ",
            "       v v v v v v v v v v v v      "
        ]
        
        for line in cpu_art:
            result += "|" + line.center(52) + "|\n"
            
        result += "+" + "-" * 50 + "+\n\n"
        
        # Educational text
        info_text = [
            "CPU (Central Processing Unit):",
            "- Executes instructions to process data",
            "- Contains multiple cores for parallel processing",
            "- Uses cache memory for faster data access",
            "- Clock speed determines how many cycles per second",
            "- Connected to system via socket on motherboard"
        ]
        
        for line in info_text:
            result += line + "\n"
            
        return result
        
    def render_memory_hierarchy(self):
        """Visualize memory hierarchy with animation"""
        if self.text_mode:
            return self.render_memory_hierarchy_text()
            
        self.surface.fill(self.colors["background"])
        
        # Title
        title = self.title_font.render("Memory Hierarchy", True, self.colors["text"])
        self.surface.blit(title, (self.width//2 - title.get_width()//2, 20))
        
        # Setup memory diagram
        levels = [
            {"name": "CPU Registers", "size": "KB", "speed": "0.5ns", "width": 60, "color": (220, 100, 100)},
            {"name": "L1 Cache", "size": "64KB", "speed": "1ns", "width": 100, "color": (220, 150, 100)},
            {"name": "L2 Cache", "size": "256KB", "speed": "3ns", "width": 150, "color": (220, 180, 100)},
            {"name": "L3 Cache", "size": "8MB", "speed": "10ns", "width": 200, "color": (190, 190, 100)},
            {"name": "RAM", "size": "16GB", "speed": "100ns", "width": 280, "color": (100, 200, 100)},
            {"name": "SSD", "size": "1TB", "speed": "10μs", "width": 340, "color": (100, 180, 180)},
            {"name": "HDD", "size": "4TB", "speed": "10ms", "width": 380, "color": (100, 100, 200)}
        ]
        
        # Calculate total height
        total_height = len(levels) * 50 + (len(levels) - 1) * 20
        start_y = (self.height - total_height) // 2
        
        # Draw the memory levels
        for i, level in enumerate(levels):
            level_height = 50
            level_y = start_y + i * (level_height + 20)
            level_x = (self.width - level["width"]) // 2
            
            # Draw level box
            self.pygame.draw.rect(self.surface, level["color"], 
                            (level_x, level_y, level["width"], level_height))
            self.pygame.draw.rect(self.surface, self.colors["text"], 
                            (level_x, level_y, level["width"], level_height), 2)
            
            # Level name
            name_text = self.small_font.render(level["name"], True, (0, 0, 0) if sum(level["color"]) > 380 else (255, 255, 255))
            self.surface.blit(name_text, 
                             (level_x + level["width"]//2 - name_text.get_width()//2, 
                              level_y + 10))
            
            # Size and speed
            details_text = self.small_font.render(f"{level['size']} | {level['speed']}", True, (0, 0, 0) if sum(level["color"]) > 380 else (255, 255, 255))
            self.surface.blit(details_text, 
                             (level_x + level["width"]//2 - details_text.get_width()//2, 
                              level_y + 30))
        
        # Draw connecting lines
        for i in range(len(levels) - 1):
            top_level = levels[i]
            bottom_level = levels[i+1]
            
            top_y = start_y + i * (50 + 20) + 50
            bottom_y = top_y + 20
            
            top_width = top_level["width"]
            bottom_width = bottom_level["width"]
            
            top_center_x = (self.width - top_width) // 2 + top_width // 2
            bottom_center_x = (self.width - bottom_width) // 2 + bottom_width // 2
            
            self.pygame.draw.line(self.surface, self.colors["text"], 
                            (top_center_x, top_y), 
                            (bottom_center_x, bottom_y), 2)
        
        # Add data access animation
        self.animation_ticks += 1
        
        # Create new particles occasionally
        if self.animation_ticks % 30 == 0:
            # Data request going down the hierarchy
            self.particles.append({
                "x": self.width // 2,
                "y": start_y - 20,
                "type": "request",
                "lifetime": 100,
                "direction": "down",
                "target_level": random.randint(1, len(levels) - 1),
                "current_level": -1
            })
        
        # Update and draw particles
        for particle in self.particles[:]:
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                continue
                
            particle["lifetime"] -= 1
            
            # Determine target y-position based on direction and target level
            if particle["direction"] == "down":
                if particle["current_level"] < particle["target_level"]:
                    # Moving to next level
                    next_level = particle["current_level"] + 1
                    target_y = start_y + next_level * (50 + 20) + 25  # Center of the level
                    
                    # Move toward target
                    if particle["y"] < target_y:
                        particle["y"] += 2
                    else:
                        particle["current_level"] = next_level
                        # If reached target, start moving back up
                        if particle["current_level"] == particle["target_level"]:
                            particle["direction"] = "up"
                            # Create a "data found" particle
                            self.particles.append({
                                "x": particle["x"],
                                "y": particle["y"],
                                "type": "data",
                                "lifetime": 100,
                                "direction": "up",
                                "target_level": 0,
                                "current_level": particle["current_level"]
                            })
            else:  # direction == "up"
                if particle["current_level"] > particle["target_level"]:
                    # Moving to previous level
                    next_level = particle["current_level"] - 1
                    target_y = start_y + next_level * (50 + 20) + 25  # Center of the level
                    
                    # Move toward target
                    if particle["y"] > target_y:
                        particle["y"] -= 3  # Move up faster
                    else:
                        particle["current_level"] = next_level
            
            # Draw the particle
            if particle["type"] == "request":
                color = (255, 200, 100)  # Orange for requests
                radius = 4
            else:  # type == "data"
                color = (100, 255, 200)  # Cyan for data
                radius = 6
                
            self.pygame.draw.circle(self.surface, color, (particle["x"], int(particle["y"])), radius)
        
        # Educational text
        info_text = [
            "Memory Hierarchy:",
            "- Balances speed, size, and cost",
            "- Faster memory is smaller and more expensive",
            "- CPU checks each level in order when requesting data",
            "- Takes advantage of locality of reference",
            "- Hit: Data found at current level",
            "- Miss: Must check next level down"
        ]
        
        # Draw text box for info
        text_box_x = 20
        text_box_y = self.height - 160
        text_box_width = 300
        text_box_height = 150
        
        self.pygame.draw.rect(self.surface, (50, 50, 70), 
                        (text_box_x, text_box_y, text_box_width, text_box_height))
        self.pygame.draw.rect(self.surface, self.colors["text"], 
                        (text_box_x, text_box_y, text_box_width, text_box_height), 2)
        
        for i, line in enumerate(info_text):
            text = self.small_font.render(line, True, self.colors["text"])
            self.surface.blit(text, (text_box_x + 10, text_box_y + 10 + i*20))
        
        return self.surface

    def render_memory_hierarchy_text(self):
        """Visualize memory hierarchy in text-only mode"""
        result = "++" + "-" * 50 + "++\n"
        result += "|" + "MEMORY HIERARCHY".center(52) + "|\n"
        result += "+" + "-" * 50 + "+\n\n"
        
        # Memory levels
        levels = [
            {"name": "CPU Registers", "size": "KB", "speed": "0.5ns", "width": 10},
            {"name": "L1 Cache", "size": "64KB", "speed": "1ns", "width": 16},
            {"name": "L2 Cache", "size": "256KB", "speed": "3ns", "width": 22},
            {"name": "L3 Cache", "size": "8MB", "speed": "10ns", "width": 28},
            {"name": "RAM", "size": "16GB", "speed": "100ns", "width": 34},
            {"name": "SSD", "size": "1TB", "speed": "10μs", "width": 40},
            {"name": "HDD", "size": "4TB", "speed": "10ms", "width": 46}
        ]
        
        for i, level in enumerate(levels):
            box_width = level["width"]
            padding = (50 - box_width) // 2
            result += "|" + " " * padding + "+" + "-" * box_width + "+" + " " * padding + "|\n"
            
            name_line = f"{level['name']} ({level['size']} | {level['speed']})"
            name_padding = (box_width - len(name_line)) // 2
            if name_padding < 0:
                name_padding = 0
                name_line = name_line[:box_width]
            
            result += "|" + " " * padding + "|" + " " * name_padding + name_line + " " * (box_width - len(name_line) - name_padding) + "|" + " " * padding + "|\n"
            result += "|" + " " * padding + "+" + "-" * box_width + "+" + " " * padding + "|\n"
            
            # Add connecting arrow
            if i < len(levels) - 1:
                result += "|" + " " * 25 + "v" + " " * 26 + "|\n"
        
        result += "+" + "-" * 50 + "+\n\n"
        
        # Educational text
        info_text = [
            "Memory Hierarchy:",
            "- Balances speed, size, and cost",
            "- Faster memory is smaller and more expensive",
            "- CPU checks each level in order when requesting data",
            "- Takes advantage of locality of reference",
            "- Hit: Data found at current level",
            "- Miss: Must check next level down"
        ]
        
        for line in info_text:
            result += line + "\n"
            
        return result
        
    def render_network_stack(self):
        """Visualize the network protocol stack in text-only mode - 
        placeholder for actual implementation"""
        if self.text_mode:
            return self.render_network_stack_text()
        
        # The actual implementation would be here as in the componentvisual.txt
        # For brevity, returning a simpler version
        self.surface.fill(self.colors["background"])
        
        # Title
        title = self.title_font.render("Network Protocol Stack (Placeholder)", True, self.colors["text"])
        self.surface.blit(title, (self.width//2 - title.get_width()//2, 20))
        
        return self.surface
        
    def render_network_stack_text(self):
        """Visualize network stack in text-only mode"""
        result = "++" + "-" * 50 + "++\n"
        result += "|" + "NETWORK PROTOCOL STACK".center(52) + "|\n"
        result += "+" + "-" * 50 + "+\n\n"
        
        layers = [
            "Application Layer (HTTP, FTP, SMTP, DNS)",
            "Transport Layer (TCP, UDP)",
            "Internet Layer (IP, ICMP, ARP)",
            "Link Layer (Ethernet, WiFi, PPP)",
            "Physical Layer (Cables, Radio, Fiber)"
        ]
        
        for i, layer in enumerate(layers):
            result += "+" + "-" * 50 + "+\n"
            result += "|" + layer.center(50) + "|\n"
            
            # Add arrow
            if i < len(layers) - 1:
                result += "|" + " " * 24 + "↕" + " " * 25 + "|\n"
        
        result += "+" + "-" * 50 + "+\n\n"
        
        # Educational text
        info_text = [
            "Network Protocol Stack:",
            "- Data encapsulation when sending (down)",
            "- Data decapsulation when receiving (up)",
            "- Each layer adds its own headers/trailers",
            "- Provides abstraction between layers",
            "- Each layer has a specific role",
            "- Based on the OSI or TCP/IP model"
        ]
        
        for line in info_text:
            result += line + "\n"
            
        return result
        
    def render_storage_hierarchy(self):
        """Visualize storage systems and data organization in text-only mode -
        placeholder for actual implementation"""
        if self.text_mode:
            return self.render_storage_hierarchy_text()
            
        # The actual implementation would be here as in the componentvisual.txt
        # For brevity, returning a simpler version
        self.surface.fill(self.colors["background"])
        
        # Title
        title = self.title_font.render("Storage Systems (Placeholder)", True, self.colors["text"])
        self.surface.blit(title, (self.width//2 - title.get_width()//2, 20))
        
        return self.surface
        
    def render_storage_hierarchy_text(self):
        """Visualize storage systems in text-only mode"""
        result = "++" + "-" * 50 + "++\n"
        result += "|" + "STORAGE SYSTEMS".center(52) + "|\n"
        result += "+" + "-" * 50 + "+\n\n"
        
        # HDD vs SSD
        result += "HDD (Hard Disk Drive)         SSD (Solid State Drive)\n"
        result += "+" + "-" * 24 + "+        +" + "-" * 24 + "+\n"
        result += "|  " + "[]===O".center(20) + "  |        |  " + "[][][][][]".center(20) + "  |\n"
        result += "|  " + "Mechanical".center(20) + "  |        |  " + "No Moving Parts".center(20) + "  |\n"
        result += "|  " + "Slower".center(20) + "  |        |  " + "Faster".center(20) + "  |\n"
        result += "|  " + "Magnetic".center(20) + "  |        |  " + "Flash Memory".center(20) + "  |\n"
        result += "+" + "-" * 24 + "+        +" + "-" * 24 + "+\n\n"
        
        # Data organization
        result += "Data Organization:\n"
        result += "Files → File System → Logical Blocks → Physical Storage\n\n"
        
        # Educational text
        info_text = [
            "Storage Systems:",
            "- HDD: Mechanical, uses magnetic platters",
            "- SSD: Solid-state, uses flash memory cells",
            "- Data is organized hierarchically",
            "- File systems manage the mapping",
            "- Trade-offs: Speed vs. Capacity vs. Cost"
        ]
        
        for line in info_text:
            result += line + "\n"
            
        return result