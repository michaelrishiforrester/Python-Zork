#!/usr/bin/env python3
"""
Unit tests for the ComputerArchitecture class
"""

import unittest
from unittest.mock import patch
from computerquest.world.architecture import ComputerArchitecture
from computerquest.models.component import Component
from computerquest.models.player import Player

class TestComputerArchitecture(unittest.TestCase):
    """Test cases for the ComputerArchitecture class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create architecture with setup mocked
        with patch.object(ComputerArchitecture, 'setup'):
            self.arch = ComputerArchitecture()
    
    def test_init(self):
        """Test architecture initialization"""
        self.assertIsNone(self.arch.player)
        self.assertEqual(self.arch.rooms, {})
        self.assertEqual(self.arch.name, "KodeKloud Computer Quest")
    
    def test_setup(self):
        """Test full setup process"""
        # Use real setup with subcomponents mocked
        with patch.object(ComputerArchitecture, 'make_components'), \
             patch.object(ComputerArchitecture, 'connect_components'), \
             patch.object(ComputerArchitecture, 'create_items'), \
             patch.object(ComputerArchitecture, 'create_player'):
            
            self.arch.setup()
            
            # Check each method was called
            ComputerArchitecture.make_components.assert_called_once_with(self.arch)
            ComputerArchitecture.connect_components.assert_called_once_with(self.arch)
            ComputerArchitecture.create_items.assert_called_once_with(self.arch)
            ComputerArchitecture.create_player.assert_called_once_with(self.arch)
    
    def test_make_components(self):
        """Test making components"""
        # Call the real method
        self.arch.make_components()
        
        # Check rooms dictionary
        self.assertGreater(len(self.arch.rooms), 0)
        
        # Check some specific components
        self.assertIn("cpu_package", self.arch.rooms)
        self.assertIn("core1", self.arch.rooms)
        self.assertIn("memory_controller", self.arch.rooms)
        self.assertIn("ram_dimm1", self.arch.rooms)
        self.assertIn("network_interface", self.arch.rooms)
        self.assertIn("bios", self.arch.rooms)
        self.assertIn("ssd", self.arch.rooms)
        self.assertIn("kernel", self.arch.rooms)
        
        # Check component properties
        cpu = self.arch.rooms["cpu_package"]
        self.assertEqual(cpu.name, "CPU Package")
        self.assertTrue(cpu.lit)
        self.assertEqual(cpu.id, "CPU000")
        
        # Check properties of other component types
        ram = self.arch.rooms["ram_dimm1"]
        self.assertEqual(ram.name, "RAM DIMM 1")
        self.assertTrue("volatile memory" in ram.desc.lower())
        
        network = self.arch.rooms["network_interface"]
        self.assertTrue("network" in network.name.lower())
        self.assertTrue("packet" in network.desc.lower())
    
    def test_connect_components(self):
        """Test connecting components"""
        # Make components first
        self.arch.make_components()
        
        # Test initial state
        cpu = self.arch.rooms["cpu_package"]
        self.assertEqual(len(cpu.doors), 0)
        self.assertEqual(len(cpu.openDoors), 0)
        
        # Connect components
        self.arch.connect_components()
        
        # Check CPU connections
        cpu = self.arch.rooms["cpu_package"]
        self.assertGreater(len(cpu.doors), 0)
        
        # Check specific connections
        self.assertIn("n", cpu.doors)  # North to core1
        self.assertEqual(cpu.doors["n"], self.arch.rooms["core1"])
        
        self.assertIn("ne", cpu.doors)  # Northeast to core2
        self.assertEqual(cpu.doors["ne"], self.arch.rooms["core2"])
        
        self.assertIn("s", cpu.doors)  # South to L3 cache
        self.assertEqual(cpu.doors["s"], self.arch.rooms["l3_cache"])
        
        self.assertIn("d", cpu.doors)  # Down to PCH
        self.assertEqual(cpu.doors["d"], self.arch.rooms["pch"])
        
        # Check Core 1 connections
        core1 = self.arch.rooms["core1"]
        self.assertIn("s", core1.doors)  # Should connect back to CPU
        self.assertEqual(core1.doors["s"], cpu)
        
        # Check memory controller connections
        memory_ctrl = self.arch.rooms["memory_controller"]
        self.assertIn("w", memory_ctrl.doors)  # West to RAM DIMM 1
        self.assertEqual(memory_ctrl.doors["w"], self.arch.rooms["ram_dimm1"])
        
        # Check RAM connections
        ram1 = self.arch.rooms["ram_dimm1"]
        self.assertIn("w", ram1.doors)  # West to kernel
        self.assertEqual(ram1.doors["w"], self.arch.rooms["kernel"])
        
        # Check peripheral connections
        pcie_ctrl = self.arch.rooms["pcie_controller"]
        self.assertIn("s", pcie_ctrl.doors)  # South to PCIe x16
        self.assertEqual(pcie_ctrl.doors["s"], self.arch.rooms["pcie_x16"])
        
        # Check for bidirectional connections
        # If A connects to B in direction X, B should connect to A in opposite direction
        for room_id, room in self.arch.rooms.items():
            for direction, connected_room in room.doors.items():
                # Check the back connection exists
                if direction == "n":
                    self.assertIn(room, connected_room.doors.get("s", {}).values(), 
                        f"{room_id} connects north to {connected_room.name} but no reverse connection exists")
                elif direction == "s":
                    self.assertIn(room, connected_room.doors.get("n", {}).values())
                elif direction == "e":
                    self.assertIn(room, connected_room.doors.get("w", {}).values())
                elif direction == "w":
                    self.assertIn(room, connected_room.doors.get("e", {}).values())
    
    def test_create_items(self):
        """Test item creation"""
        # Make components first
        self.arch.make_components()
        
        # Create items
        self.arch.create_items()
        
        # Check CPU package items
        cpu = self.arch.rooms["cpu_package"]
        self.assertIn("instruction_manual", cpu.items)
        self.assertTrue("Guide" in cpu.items["instruction_manual"])
        
        # Check core components items
        core1_cu = self.arch.rooms["core1_cu"]
        self.assertIn("decoder_tool", core1_cu.items)
        
        core1_registers = self.arch.rooms["core1_registers"]
        self.assertIn("register_log", core1_registers.items)
        
        # Check virus locations
        ssd = self.arch.rooms["ssd"]
        self.assertIn("boot_sector_virus", ssd.items)
        
        kernel = self.arch.rooms["kernel"]
        self.assertIn("rootkit_virus", kernel.items)
        
        ram1 = self.arch.rooms["ram_dimm1"]
        self.assertIn("memory_resident_virus", ram1.items)
        
        bios = self.arch.rooms["bios"]
        self.assertIn("firmware_virus", bios.items)
        
        network = self.arch.rooms["network_interface"]
        self.assertIn("packet_sniffer_virus", network.items)
    
    def test_create_player(self):
        """Test player creation"""
        # Make components first
        self.arch.make_components()
        
        # Create player
        self.arch.create_player()
        
        # Check player created
        self.assertIsNotNone(self.arch.player)
        self.assertIsInstance(self.arch.player, Player)
        
        # Check starting location
        self.assertEqual(self.arch.player.location, self.arch.rooms["cpu_package"])
        
        # Check starting inventory
        self.assertIn("antivirus_tool", self.arch.player.items)
        self.assertIn("system_mapper", self.arch.player.items)
        
        # Check player name
        self.assertEqual(self.arch.player.name, "Security Program")

if __name__ == "__main__":
    unittest.main()