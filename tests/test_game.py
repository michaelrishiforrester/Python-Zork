#!/usr/bin/env python3
"""
Unit tests for the Game class
"""

import unittest
from unittest.mock import patch, MagicMock, call
import io
import sys
from computerquest.game import Game, CPUPipelineMinigame, SaveLoadSystem
from computerquest.models.component import Component
from computerquest.models.player import Player
from computerquest.commands import CommandProcessor

class TestGame(unittest.TestCase):
    """Test cases for the Game class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Patch the setup functions to avoid actual world creation for unit tests
        with patch('computerquest.world.architecture.ComputerArchitecture.setup'):
            self.game = Game()
            
            # Create mock player
            self.game.player = MagicMock()
            self.game.player.location = Component(name="Test Location", description="A test location")
            self.game.player.found_viruses = []
            self.game.player.quarantined_viruses = []
            self.game.player.knowledge = {"cpu": 0, "memory": 0, "storage": 0, "networking": 0, "security": 0}
            
            # Create mock map
            self.game.game_map = MagicMock()
            self.game.game_map.rooms = {
                "room1": Component(name="Room 1", description="First room"),
                "room2": Component(name="Room 2", description="Second room"),
                "room3": Component(name="Room 3", description="Third room")
            }
            
            # Reset game state
            self.game.turns = 0
            self.game.game_over = False
            self.game.all_viruses_found = False
            self.game.victory = False
            
            # Mock map grid
            self.game.map_grid = {
                "room1": {"visited": True},
                "room2": {"visited": False},
                "room3": {"visited": False}
            }
    
    def test_init(self):
        """Test game initialization"""
        with patch('computerquest.world.architecture.ComputerArchitecture.setup'):
            game = Game()
            
            # Check basic initialization
            self.assertIsNotNone(game.game_map)
            self.assertEqual(game.turns, 0)
            self.assertFalse(game.game_over)
            self.assertFalse(game.all_viruses_found)
            self.assertFalse(game.victory)
            
            # Check subsystems were created
            self.assertIsNotNone(game.progress)
            self.assertIsNotNone(game.visualizer)
            self.assertIsNone(game.current_minigame)
            self.assertIsNone(game.current_visualization)
            self.assertIsNotNone(game.save_load)
            self.assertIsNotNone(game.command_processor)
            self.assertIsNotNone(game.map_grid)
    
    @patch('builtins.print')
    @patch('builtins.input', return_value="help")
    def test_start(self, mock_input, mock_print):
        """Test the main game loop"""
        # Setup command processor mock
        self.game.command_processor = MagicMock()
        self.game.command_processor.process.return_value = "Command executed"
        
        # Set game_over to True after one loop
        def set_game_over(*args, **kwargs):
            self.game.game_over = True
            return "Command executed"
            
        self.game.command_processor.process.side_effect = set_game_over
        
        # Run the game loop
        self.game.start()
        
        # Check input was processed
        mock_input.assert_called_once()
        self.game.command_processor.process.assert_called_once_with("help")
        
        # Check output
        mock_print.assert_called_with("\nCommand executed")
    
    @patch('builtins.print')
    def test_display_welcome(self, mock_print):
        """Test welcome message display"""
        self.game.display_welcome()
        
        # Check print calls contain expected elements
        welcome_calls = [call for call in mock_print.call_args_list if "Welcome to the KodeKloud Computer Architecture Quest" in str(call)]
        self.assertGreater(len(welcome_calls), 0)
    
    def test_move(self):
        """Test player movement"""
        # Set up mock objects
        prev_location = Component(name="Previous Location", description="Starting point")
        new_location = Component(name="New Location", description="Destination")
        
        self.game.player.location = prev_location
        self.game.player.go.return_value = True  # Successful move
        
        # After moving, location changes to new_location
        def side_effect_go(direction):
            self.game.player.location = new_location
            return True
            
        self.game.player.go.side_effect = side_effect_go
        
        # Add room to map
        self.game.game_map.rooms = {"new_room": new_location}
        
        # Test successful move
        result = self.game.move("north")
        
        # Check results
        self.game.player.go.assert_called_with("n")  # Direction normalized to 'n'
        self.assertEqual(self.game.turns, 1)  # Turn counter increased
        self.assertIn("Moved from Previous Location to New Location", result)
        self.assertIn(new_location.desc, result)
        
        # Test failed move
        self.game.player.go.side_effect = None
        self.game.player.go.return_value = False  # Failed move
        
        result = self.game.move("west")
        self.assertIn("no connection", result.lower())
    
    @patch('computerquest.utils.map_renderer.render_map')
    def test_display_map(self, mock_render_map):
        """Test map display"""
        mock_render_map.return_value = "ASCII Map Output"
        
        # Set current location to a room in map_grid
        for room_id, room in self.game.game_map.rooms.items():
            if room_id in self.game.map_grid:
                self.game.player.location = room
                break
        
        result = self.game.display_map()
        
        # Check map renderer was called
        mock_render_map.assert_called_once()
        self.assertEqual(result, "ASCII Map Output")
    
    def test_show_help(self):
        """Test help display"""
        help_text = self.game.show_help()
        
        # Check help text contains important command categories
        self.assertIn("KODEKLOUD COMPUTER QUEST COMMANDS", help_text)
        self.assertIn("Movement:", help_text)
        self.assertIn("Exploration:", help_text)
        self.assertIn("Inventory:", help_text)
        self.assertIn("Security Functions:", help_text)
    
    def test_start_cpu_minigame(self):
        """Test starting CPU minigame"""
        # Test without required knowledge
        self.game.player.knowledge = {"cpu": 2}  # Below required level
        result = self.game.start_cpu_minigame()
        self.assertIn("need more knowledge", result.lower())
        self.assertIsNone(self.game.current_minigame)
        
        # Test with required knowledge
        self.game.player.knowledge = {"cpu": 5}  # Above required level
        result = self.game.start_cpu_minigame()
        self.assertIsNotNone(self.game.current_minigame)
        self.assertIsInstance(self.game.current_minigame, CPUPipelineMinigame)
        self.assertIn("CPU Pipeline", result)
    
    def test_handle_visualization(self):
        """Test visualization handling"""
        # Test without type specified
        result = self.game.handle_visualization()
        self.assertIn("Please specify what to visualize", result)
        
        # Test CPU visualization
        result = self.game.handle_visualization("cpu")
        self.assertEqual(self.game.current_visualization, "cpu")
        self.assertIn("CPU Visualization", result)
        
        # Test memory visualization
        result = self.game.handle_visualization("memory")
        self.assertEqual(self.game.current_visualization, "memory")
        self.assertIn("Memory Hierarchy Visualization", result)
        
        # Test stopping visualization
        prev_viz = self.game.current_visualization
        result = self.game.handle_visualization("stop")
        self.assertIsNone(self.game.current_visualization)
        self.assertIn(f"Stopped {prev_viz} visualization", result)
        
        # Test unknown visualization type
        result = self.game.handle_visualization("unknown")
        self.assertIn("Unknown visualization type", result)
    
    def test_handle_simulation(self):
        """Test simulation handling"""
        # Test without active simulation
        result = self.game.handle_simulation()
        self.assertIn("No active simulation", result)
        
        # Start a simulation
        self.game.start_cpu_minigame()
        
        # Test without action specified
        result = self.game.handle_simulation()
        self.assertIn("Please specify a simulation action", result)
        
        # Test step action
        result = self.game.handle_simulation("step")
        self.assertIn("Advanced pipeline by one step", result)
        
        # Test toggle action
        result = self.game.handle_simulation("toggle")
        self.assertIn("Toggled pipeline mode", result)
        
        # Test reset action
        result = self.game.handle_simulation("reset")
        self.assertIn("Reset pipeline simulation", result)
        
        # Test stop action
        result = self.game.handle_simulation("stop")
        self.assertIsNone(self.game.current_minigame)
        self.assertIn("Simulation stopped", result)
        
        # Test unknown action
        self.game.start_cpu_minigame()
        result = self.game.handle_simulation("unknown")
        self.assertIn("Unknown simulation action", result)
    
    def test_get_component_info(self):
        """Test educational component information"""
        # Test valid topics
        cpu_info = self.game.get_component_info("cpu")
        self.assertIn("CPU (Central Processing Unit)", cpu_info)
        
        memory_info = self.game.get_component_info("memory")
        self.assertIn("Computer Memory Hierarchy", memory_info)
        
        # Test unknown topic with suggestions
        unknown_result = self.game.get_component_info("processor")
        self.assertIn("not found", unknown_result)
        self.assertIn("Did you mean", unknown_result)
        self.assertIn("cpu", unknown_result.lower())
        
        # Test completely unknown topic
        very_unknown = self.game.get_component_info("xyzabc")
        self.assertIn("No information available", very_unknown)
    
    def test_display_motherboard(self):
        """Test motherboard diagram display"""
        result = self.game.display_motherboard()
        
        # Check diagram contains key components
        self.assertIn("KodeKloud Computer Quest Motherboard Layout", result)
        self.assertIn("CPU Package", result)
        self.assertIn("Core 1", result)
        self.assertIn("L3 Cache", result)
        self.assertIn("RAM DIMM", result)
        self.assertIn("PCH", result)
        self.assertIn("Virus Locations", result)
    
    def test_victory_message(self):
        """Test victory message generation"""
        self.game.turns = 42
        
        # Mark some rooms as visited
        for room in self.game.game_map.rooms.values()[:2]:
            room.visited = True
            
        # Set knowledge levels
        self.game.player.knowledge = {"cpu": 3, "memory": 2, "storage": 1, "networking": 0, "security": 5}
        
        result = self.game.victory_message()
        
        # Check message contains expected elements
        self.assertIn("CONGRATULATIONS", result)
        self.assertIn("Turns taken: 42", result)
        self.assertIn("Thank you for playing", result)
    
    def test_prefix_matching(self):
        """Test helper methods for prefix matching"""
        # Setup test data
        self.game.command_processor.commands = {
            "look": None,
            "load": None,
            "location": None
        }
        
        self.game.player.location.items = {
            "document": "A document",
            "desk": "A desk",
            "door": "A door"
        }
        
        self.game.player.items = {
            "tablet": "A tablet",
            "tool": "A tool"
        }
        
        # Test exact matches
        self.assertEqual(self.game._match_command_prefix("look"), "look")
        self.assertEqual(self.game._match_item_prefix("document"), "document")
        self.assertEqual(self.game._match_inventory_item_prefix("tablet"), "tablet")
        
        # Test unique prefix matches
        self.assertEqual(self.game._match_command_prefix("loo"), "look")
        self.assertEqual(self.game._match_item_prefix("doc"), "document")
        self.assertEqual(self.game._match_inventory_item_prefix("ta"), "tablet")
        
        # Test ambiguous prefix (should return original)
        self.assertEqual(self.game._match_command_prefix("lo"), "lo")  # Ambiguous: look, load, location
        self.assertEqual(self.game._match_item_prefix("d"), "d")       # Ambiguous: document, desk, door
        
        # Test non-matching prefix
        self.assertEqual(self.game._match_command_prefix("xyz"), "xyz")
        self.assertEqual(self.game._match_item_prefix("xyz"), "xyz")
        self.assertEqual(self.game._match_inventory_item_prefix("xyz"), "xyz")

class TestCPUPipelineMinigame(unittest.TestCase):
    """Test cases for the CPU Pipeline Minigame"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game = MagicMock()
        self.minigame = CPUPipelineMinigame(self.game)
    
    def test_explain(self):
        """Test explanation text"""
        result = self.minigame.explain()
        self.assertIn("CPU Pipeline Minigame", result)
    
    def test_get_status(self):
        """Test status display"""
        result = self.minigame.get_status()
        self.assertIn("CPU Pipeline status", result)
    
    def test_step(self):
        """Test stepping the simulation"""
        result = self.minigame.step()
        self.assertIn("Advanced pipeline by one step", result)
    
    def test_toggle_pipeline(self):
        """Test toggling pipeline mode"""
        result = self.minigame.toggle_pipeline()
        self.assertIn("Toggled pipeline mode", result)
    
    def test_reset(self):
        """Test resetting the simulation"""
        result = self.minigame.reset()
        self.assertIn("Reset pipeline simulation", result)

class TestSaveLoadSystem(unittest.TestCase):
    """Test cases for the SaveLoadSystem"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game = MagicMock()
        self.save_system = SaveLoadSystem(self.game)
    
    def test_save_game(self):
        """Test saving game"""
        # Test with default name
        result = self.save_system.save_game()
        self.assertIn("Game saved with name: autosave", result)
        
        # Test with custom name
        result = self.save_system.save_game("custom_save")
        self.assertIn("Game saved with name: custom_save", result)
    
    def test_load_game(self):
        """Test loading game"""
        result = self.save_system.load_game("test_save")
        self.assertIn("Game loaded: test_save", result)
    
    def test_list_saves(self):
        """Test listing saved games"""
        result = self.save_system.list_saves()
        self.assertIn("Available saved games", result)
    
    def test_delete_save(self):
        """Test deleting a saved game"""
        result = self.save_system.delete_save("test_save")
        self.assertIn("Deleted save: test_save", result)

if __name__ == "__main__":
    unittest.main()