import json
import os
import time
from datetime import datetime

class SaveLoadSystem:
    """
    Handles saving and loading game state
    """
    def __init__(self, game):
        self.game = game
        self.save_directory = os.path.join(os.path.expanduser("~"), ".kodekloud_quest", "saves")
        
        # Create save directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory, exist_ok=True)
    
    def save_game(self, save_name=None):
        """
        Save the current game state
        """
        # Generate default save name if none provided
        if not save_name:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            save_name = f"kodekloud_quest_save_{timestamp}"
        
        # Ensure it has .json extension
        if not save_name.endswith('.json'):
            save_name += '.json'
            
        save_path = os.path.join(self.save_directory, save_name)
        
        try:
            # Create a dictionary with all game state data
            game_state = {
                'version': '1.0',  # For compatibility checking in future versions
                'timestamp': time.time(),
                'save_name': save_name,
                'turns': self.game.turns,
                'player': {
                    'location': self.game.player.location.id,
                    'items': self.game.player.items,
                    'health': self.game.player.health,
                    'name': self.game.player.name,
                    'found_viruses': self.game.player.found_viruses,
                    'quarantined_viruses': self.game.player.quarantined_viruses,
                    'knowledge': self.game.player.knowledge
                },
                'components': {},
                'game_state': {
                    'game_over': self.game.game_over,
                    'victory': self.game.victory,
                    'all_viruses_found': self.game.all_viruses_found
                }
            }
            
            # Save each component's state
            for room_id, room in self.game.game_map.rooms.items():
                game_state['components'][room.id] = {
                    'items': room.items,
                    'visited': room.visited,
                    'error_state': getattr(room, 'error_state', False),
                    'power_state': getattr(room, 'power_state', True)
                }
            
            # Write to file
            with open(save_path, 'w') as save_file:
                json.dump(game_state, save_file, indent=2)
                
            return f"Game saved to {save_name}"
            
        except Exception as e:
            return f"Error saving game: {str(e)}"
    
    def load_game(self, save_name):
        """
        Load a previously saved game
        """
        # Ensure it has .json extension
        if not save_name.endswith('.json'):
            save_name += '.json'
            
        save_path = os.path.join(self.save_directory, save_name)
        
        if not os.path.exists(save_path):
            return f"Save file '{save_name}' not found."
            
        try:
            # Load the game state
            with open(save_path, 'r') as save_file:
                game_state = json.load(save_file)
                
            # Check version compatibility
            if game_state.get('version', '0.0') != '1.0':
                return "Save file is from an incompatible game version."
                
            # Load game state
            self.game.turns = game_state['turns']
            self.game.game_over = game_state['game_state']['game_over']
            self.game.victory = game_state['game_state']['victory']
            self.game.all_viruses_found = game_state['game_state']['all_viruses_found']
            
            # Load player state
            player_location_id = game_state['player']['location']
            player_location = None
            for room_id, room in self.game.game_map.rooms.items():
                if room.id == player_location_id:
                    player_location = room
                    break
                    
            if not player_location:
                return "Error: Could not find player's location in the game world."
                
            self.game.player.location = player_location
            self.game.player.items = game_state['player']['items']
            self.game.player.health = game_state['player']['health']
            self.game.player.name = game_state['player']['name']
            self.game.player.found_viruses = game_state['player']['found_viruses']
            self.game.player.quarantined_viruses = game_state['player']['quarantined_viruses']
            self.game.player.knowledge = game_state['player']['knowledge']
            
            # Load component states
            for room_id, room in self.game.game_map.rooms.items():
                if room.id in game_state['components']:
                    room_state = game_state['components'][room.id]
                    room.items = room_state['items']
                    room.visited = room_state['visited']
                    if hasattr(room, 'error_state'):
                        room.error_state = room_state.get('error_state', False)
                    if hasattr(room, 'power_state'):
                        room.power_state = room_state.get('power_state', True)
                        
            # Also update the map_grid to match visited rooms
            for room_id, room in self.game.game_map.rooms.items():
                if room_id in self.game.map_grid and room.visited:
                    self.game.map_grid[room_id]['visited'] = True
            
            # Update progress system if it exists
            if hasattr(self.game, 'progress'):
                self.game.progress.update()
                
            return f"Game loaded from {save_name}"
            
        except Exception as e:
            return f"Error loading game: {str(e)}"
    
    def list_saves(self):
        """
        List all available save files
        """
        try:
            saves = [f for f in os.listdir(self.save_directory) if f.endswith('.json')]
            
            if not saves:
                return "No save files found."
            
            result = "Available save files:\n"
            for i, save_file in enumerate(saves, 1):
                # Try to read save metadata
                save_path = os.path.join(self.save_directory, save_file)
                try:
                    with open(save_path, 'r') as f:
                        save_data = json.load(f)
                        timestamp = datetime.fromtimestamp(save_data['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                        turns = save_data['turns']
                        player_location = None
                        for room_id, room in self.game.game_map.rooms.items():
                            if room.id == save_data['player']['location']:
                                player_location = room.name
                                break
                    
                    result += f"{i}. {save_file[:-5]} - {timestamp} - Turn {turns} - {player_location}\n"
                except:
                    result += f"{i}. {save_file[:-5]} (metadata unavailable)\n"
            
            return result
            
        except Exception as e:
            return f"Error listing save files: {str(e)}"
    
    def delete_save(self, save_name):
        """
        Delete a save file
        """
        # Ensure it has .json extension
        if not save_name.endswith('.json'):
            save_name += '.json'
            
        save_path = os.path.join(self.save_directory, save_name)
        
        if not os.path.exists(save_path):
            return f"Save file '{save_name}' not found."
            
        try:
            os.remove(save_path)
            return f"Save file '{save_name}' deleted."
        except Exception as e:
            return f"Error deleting save file: {str(e)}"


# Commands to be added to process_cmd() in Game class:
"""
elif command == 'save':
    if len(cmd_list) > 1:
        return self.save_load.save_game(cmd_list[1])
    else:
        return self.save_load.save_game()
elif command == 'load':
    if len(cmd_list) > 1:
        return self.save_load.load_game(cmd_list[1])
    else:
        return "Please specify a save file to load. Use 'saves' to list available saves."
elif command in ['saves', 'listsaves']:
    return self.save_load.list_saves()
elif command == 'deletesave':
    if len(cmd_list) > 1:
        return self.save_load.delete_save(cmd_list[1])
    else:
        return "Please specify a save file to delete."
"""