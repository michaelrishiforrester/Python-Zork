import room


class Player:

    def __init__(self, location=None, items={}, NPC=False, n=None):
        """
        new Player constructor
            location and items are OPTIONAL parameters
            The values in the param list are DEFAULT values
        """
        self.location = location #defines starting laction for the player
        self.items = items #defines staring items for the player
        self.health = 100 #defines starting health for player
        self.com = NPC #defines if player object is an NPC or not
        self.name = n #defines player name
        self.death = False #boolean to check if object is dead
        
        # Additional attributes for ComputerQuest
        self.found_viruses = []
        self.quarantined_viruses = []
        self.knowledge = {
            "cpu": 0,
            "memory": 0,
            "storage": 0,
            "networking": 0,
            "security": 0
        }

        if self.com == True:
            self.location.play.append(self)
    
    def __str__(self):
        """
        get string representation of Player
        """
        return self.name if self.name else "Security Program"

    def go(self, direction):
        """
        go in a direction
        """
        room = self.location #defines room you are in
        direct = list(room.doors) #gets the list of directions you can move
        if direction in direct:
            self.location = room.doors[direction] #puts player object in room if they can move there
            if self.com == True:
                self.location.play.append(room.play.pop(self)) #if player object is and NPC this will upadte the room list or NPC's
            return True
        else:
            return False

    def look(self, item=None):
        """
        look around, or look at an item
        """
        room = self.location #gets room you are in
        if item != None:
            try:
                return(item+room.items[item]) #gets item description and item name then returns it to the processer
            except:
                return 'item "'+item+'" not found' #returns item name if item wasnt in the room
        else:
            return room.print_details() #returns the rooms description if items were not listed

    def take(self, item):
        """
        take an item
        """
        if len(self.items) == 8:
            #Stop code if you've maxed out on items
            return
        if item in self.location.items:
            #Takes item out of the room dictionary and places it in the player's dictionary
            self.items.update({item:self.location.items.pop(item)})
        for k, v in self.location.items.items():
            #checks if item is in a container and pulls it out
            if type(v) == type(dict()):
                for l, w in v.items():
                    if l == item:
                        v.pop(l)
                        break
    
    def drop(self, item):
        """
        drop an item
        """
        #takes item out of player dictionary and places it in the room
        if item in self.items:
            d = self.items[item] #gets item description
            self.items.pop(item) #removes item from player
            self.location.items.update({item:d}) #places item  in room

    def kill(self, npc, dam):
        """
        lose health
        """
        if dam > 0:
            npc.health -= dam #subtracts health from player you are fighting and vice versa (NPC's are a bit glitchy right now and cannot be implemented just yet)
            if npc.health <= 0:
                npc.dead() #"kills" the npc or player
                return 'Killed'
            return 'Hit'
        else:
            return 'Missed'
    def dead(self):
        """
        die
        """
        self.death = True #updates death boolean
        rem = self.items
        for x, y in rem.items():
            self.location.items.update({x:self.items[x]}) #removes items and places them in the room
        self.items = {}
        if self.com:
            self.location.play.remove(self)
            
    def scan(self, target=None):
        """
        Scan for viruses in current location or specific item
        """
        # Check if player has the scanner tool
        if 'antivirus_tool' not in self.items:
            return "You need an antivirus tool to perform a scan."
        
        # Scanning a specific item
        if target:
            # Check if item is in room
            if target in self.location.items:
                item_desc = self.location.items[target]
                if 'virus' in target.lower():
                    if target not in self.found_viruses:
                        self.found_viruses.append(target)
                        # Increase security knowledge when finding a virus
                        self.knowledge['security'] += 1
                    return f"ALERT! {target} detected. This is a malicious program that should be quarantined immediately."
                else:
                    return f"No virus detected in {target}."
            # Check if item is in inventory
            elif target in self.items:
                if 'virus' in target.lower():
                    if target not in self.found_viruses:
                        self.found_viruses.append(target)
                        self.knowledge['security'] += 1
                    return f"ALERT! {target} detected. This is a malicious program in your inventory that should be quarantined immediately."
                else:
                    return f"No virus detected in {target}."
            else:
                return f"There's no {target} here to scan."
        
        # Scanning the entire room
        else:
            # Check for viruses in the room
            viruses_here = [item for item in self.location.items if 'virus' in item.lower()]
            
            if viruses_here:
                result = "SECURITY ALERT! Virus scan detected the following threats:\n"
                for virus in viruses_here:
                    if virus not in self.found_viruses:
                        self.found_viruses.append(virus)
                        self.knowledge['security'] += 1
                    result += f"- {virus}\n"
                result += "\nUse 'quarantine [virus]' to contain these threats."
                return result
            else:
                # Increase knowledge related to the current component when scanning
                if 'cpu' in self.location.name.lower() or 'alu' in self.location.name.lower() or 'register' in self.location.name.lower():
                    self.knowledge['cpu'] += 1
                elif 'memory' in self.location.name.lower() or 'ram' in self.location.name.lower() or 'cache' in self.location.name.lower():
                    self.knowledge['memory'] += 1
                elif 'drive' in self.location.name.lower() or 'disk' in self.location.name.lower() or 'ssd' in self.location.name.lower() or 'hdd' in self.location.name.lower():
                    self.knowledge['storage'] += 1
                elif 'network' in self.location.name.lower() or 'interface' in self.location.name.lower():
                    self.knowledge['networking'] += 1
                
                return "Scan complete. No viruses detected in this location."
    
    def quarantine(self, virus_name):
        """
        Quarantine a detected virus
        """
        # Check if player has the antivirus tool
        if 'antivirus_tool' not in self.items:
            return "You need an antivirus tool to quarantine viruses."
            
        # Check if the virus exists and has been found
        if virus_name not in self.found_viruses:
            return f"You haven't detected a virus named '{virus_name}' yet. Try scanning first."
            
        # Check if virus is already quarantined
        if virus_name in self.quarantined_viruses:
            return f"The {virus_name} has already been quarantined."
            
        # Check if virus is in the current room
        if virus_name in self.location.items:
            # Remove the virus
            description = self.location.items.pop(virus_name)
            
            # Add to quarantined list
            self.quarantined_viruses.append(virus_name)
            
            # Add a neutralized version to the room
            self.location.items[f"quarantined_{virus_name}"] = f"A neutralized version of {virus_name}, safely contained and no longer a threat."
            
            # Increase security knowledge
            self.knowledge['security'] += 2
            
            return f"Success! The {virus_name} has been quarantined and can no longer harm the system."
            
        # Check if virus is somehow in inventory
        elif virus_name in self.items:
            # Remove the virus
            description = self.items.pop(virus_name)
            
            # Add to quarantined list
            self.quarantined_viruses.append(virus_name)
            
            # Add a neutralized version to inventory
            self.items[f"quarantined_{virus_name}"] = f"A neutralized version of {virus_name}, safely contained and no longer a threat."
            
            # Increase security knowledge
            self.knowledge['security'] += 2
            
            return f"Success! The {virus_name} has been quarantined from your inventory and can no longer harm the system."
            
        else:
            return f"The {virus_name} is not in this location. You need to find where it's hiding."
    
    def check_progress(self):
        """
        Check progress on virus discovery and quarantine
        """
        result = "Mission Status Report:\n"
        result += "--------------------\n"
        
        result += f"Viruses Found: {len(self.found_viruses)}\n"
        if self.found_viruses:
            result += "- " + "\n- ".join(self.found_viruses) + "\n"
            
        result += f"\nViruses Quarantined: {len(self.quarantined_viruses)}\n"
        if self.quarantined_viruses:
            result += "- " + "\n- ".join(self.quarantined_viruses) + "\n"
            
        return result
        
    def knowledge_report(self):
        """
        Display knowledge gained about computer architecture
        """
        total = sum(self.knowledge.values())
        
        result = "Computer Architecture Knowledge:\n"
        result += "------------------------------\n"
        
        for topic, level in self.knowledge.items():
            stars = "★" * level + "☆" * (5 - level)
            result += f"{topic.capitalize()}: {stars} ({level}/5)\n"
            
        result += f"\nTotal Knowledge: {total}/25"
        
        return result
        
    def advanced_scan(self, target=None):
        """
        Advanced scanning that can reveal hidden viruses and their properties
        Requires higher knowledge levels in respective areas
        """
        # Check if player has advanced scanning capability
        required_tools = {
            'antivirus_tool': "You need an antivirus tool to perform a scan.",
            'decoder_tool': "A more advanced decoder tool would help analyze code patterns."
        }
        
        missing_tools = [tool for tool, msg in required_tools.items() if tool not in self.items]
        if missing_tools:
            return required_tools[missing_tools[0]]
        
        # Knowledge requirements for different component types
        required_knowledge = {
            'cpu': {'cpu': 2, 'security': 1},
            'memory': {'memory': 2, 'security': 1},
            'storage': {'storage': 2, 'security': 1},
            'network': {'networking': 2, 'security': 1},
            'firmware': {'security': 3}
        }
        
        # Determine component type
        component_type = 'other'
        loc_name = self.location.name.lower()
        if any(x in loc_name for x in ['cpu', 'alu', 'control', 'register']):
            component_type = 'cpu'
        elif any(x in loc_name for x in ['memory', 'ram', 'cache']):
            component_type = 'memory'
        elif any(x in loc_name for x in ['ssd', 'hdd', 'drive', 'disk', 'storage']):
            component_type = 'storage'
        elif any(x in loc_name for x in ['network', 'interface']):
            component_type = 'network'
        elif any(x in loc_name for x in ['bios', 'firmware', 'uefi']):
            component_type = 'firmware'
        
        # Check knowledge requirements
        if component_type in required_knowledge:
            for knowledge_area, level in required_knowledge[component_type].items():
                if self.knowledge[knowledge_area] < level:
                    return f"You need more knowledge of {knowledge_area} (level {level}) to perform an advanced scan in this component."
        
        # Scanning logic similar to regular scan but with enhanced capabilities
        if target:
            # Scanning a specific item with enhanced capabilities
            if target in self.location.items:
                item_desc = self.location.items[target]
                
                # Detect both obvious and hidden viruses
                if 'virus' in target.lower() or 'malicious' in item_desc.lower() or 'suspicious' in item_desc.lower():
                    virus_type = None
                    if 'boot' in target.lower() or 'boot' in item_desc.lower():
                        virus_type = "boot_sector_virus"
                    elif 'root' in target.lower() or 'kernel' in item_desc.lower():
                        virus_type = "rootkit_virus"
                    elif 'memory' in target.lower() or 'ram' in item_desc.lower():
                        virus_type = "memory_resident_virus"
                    elif 'firm' in target.lower() or 'bios' in item_desc.lower():
                        virus_type = "firmware_virus"
                    elif 'packet' in target.lower() or 'network' in item_desc.lower():
                        virus_type = "packet_sniffer_virus"
                    
                    if virus_type and virus_type not in self.found_viruses:
                        self.found_viruses.append(virus_type)
                        self.knowledge['security'] += 2
                    
                    return f"ADVANCED SCAN RESULTS:\n\nThreat detected in {target}!\n" + \
                           f"Virus Type: {virus_type if virus_type else 'Unknown'}\n" + \
                           f"Threat Level: High\n" + \
                           f"Analysis: {item_desc}\n\n" + \
                           f"Recommended action: Quarantine immediately."
                else:
                    return f"Advanced scan complete. No threats detected in {target}."
                    
            # Item not in location, check inventory
            elif target in self.items:
                item_desc = self.items[target]
                
                # Detect both obvious and hidden viruses in inventory
                if 'virus' in target.lower() or 'malicious' in item_desc.lower() or 'suspicious' in item_desc.lower():
                    virus_type = None
                    if 'boot' in target.lower() or 'boot' in item_desc.lower():
                        virus_type = "boot_sector_virus"
                    elif 'root' in target.lower() or 'kernel' in item_desc.lower():
                        virus_type = "rootkit_virus"
                    elif 'memory' in target.lower() or 'ram' in item_desc.lower():
                        virus_type = "memory_resident_virus"
                    elif 'firm' in target.lower() or 'bios' in item_desc.lower():
                        virus_type = "firmware_virus"
                    elif 'packet' in target.lower() or 'network' in item_desc.lower():
                        virus_type = "packet_sniffer_virus"
                    
                    if virus_type and virus_type not in self.found_viruses:
                        self.found_viruses.append(virus_type)
                        self.knowledge['security'] += 2
                    
                    return f"ADVANCED SCAN RESULTS:\n\nThreat detected in your inventory item {target}!\n" + \
                           f"Virus Type: {virus_type if virus_type else 'Unknown'}\n" + \
                           f"Threat Level: High\n" + \
                           f"Analysis: {item_desc}\n\n" + \
                           f"Recommended action: Quarantine immediately."
                else:
                    return f"Advanced scan complete. No threats detected in {target}."
            else:
                return f"There's no {target} here to scan."
        
        # Scanning the entire room with enhanced capabilities
        else:
            # Regular virus checks
            viruses_here = [item for item in self.location.items if 'virus' in item.lower()]
            
            # Hidden virus checks based on item descriptions
            hidden_threats = []
            for item, desc in self.location.items.items():
                if 'virus' not in item.lower() and ('suspicious' in desc.lower() or 'malicious' in desc.lower()):
                    hidden_threats.append(item)
            
            if viruses_here or hidden_threats:
                result = "ADVANCED SECURITY SCAN RESULTS:\n\n"
                
                if viruses_here:
                    result += "Confirmed threats:\n"
                    for virus in viruses_here:
                        if virus not in self.found_viruses:
                            self.found_viruses.append(virus)
                            self.knowledge['security'] += 1
                        result += f"- {virus}\n"
                        
                if hidden_threats:
                    result += "\nSuspicious items requiring further analysis:\n"
                    for item in hidden_threats:
                        result += f"- {item}\n"
                    
                result += "\nUse 'analyze [item]' for detailed threat assessment and 'quarantine [virus]' to contain threats."
                return result
            else:
                # Increase knowledge based on the current component
                self._increase_component_knowledge()
                
                return f"Advanced scan complete. No threats detected in {self.location.name}."

    def analyze(self, target):
        """
        Deeply analyze an item to reveal hidden properties or connections to viruses
        """
        if 'decoder_tool' not in self.items:
            return "You need a decoder tool to perform detailed analysis."
            
        # Check if item exists
        if target in self.location.items:
            item_desc = self.location.items[target]
            
            # Analysis results based on item type
            if 'log' in target:
                return f"Analysis of {target}:\n\n" + \
                      f"The log contains entries showing {item_desc}\n" + \
                      f"Pattern analysis reveals evidence of {'suspicious' if 'suspicious' in item_desc or 'unusual' in item_desc else 'normal'} activity."
            
            elif 'calculation' in target or 'anomaly' in target:
                return f"Analysis of {target}:\n\n" + \
                      f"The data patterns show {item_desc}\n" + \
                      f"This could be a sign of a {'virus attempting to hide its operations' if 'suspicious' in item_desc or 'unusual' in item_desc else 'normal system process'}."
                      
            elif 'packet' in target:
                return f"Analysis of {target}:\n\n" + \
                      f"The packet contains {item_desc}\n" + \
                      f"Traffic analysis indicates this may be {'data exfiltration' if 'suspicious' in item_desc or 'unusual' in item_desc else 'normal network traffic'}."
            
            else:
                # Generic analysis for other items
                suspicious_terms = ['suspicious', 'unusual', 'strange', 'abnormal', 'unexpected']
                is_suspicious = any(term in item_desc.lower() for term in suspicious_terms)
                
                if is_suspicious:
                    virus_hint = ""
                    if 'boot' in item_desc.lower():
                        virus_hint = "This may be related to a boot sector infection."
                    elif 'kernel' in item_desc.lower() or 'root' in item_desc.lower():
                        virus_hint = "This could indicate rootkit activity in the system."
                    elif 'memory' in item_desc.lower():
                        virus_hint = "This pattern is consistent with memory-resident malware."
                    elif 'firmware' in item_desc.lower() or 'bios' in item_desc.lower():
                        virus_hint = "This suggests possible firmware compromising."
                    elif 'network' in item_desc.lower() or 'packet' in item_desc.lower():
                        virus_hint = "This is characteristic of network traffic interception."
                    
                    return f"Analysis of {target}:\n\n" + \
                          f"SECURITY ALERT: This item shows signs of suspicious activity.\n" + \
                          f"Details: {item_desc}\n" + \
                          f"{virus_hint}"
                else:
                    return f"Analysis of {target}:\n\n" + \
                          f"No suspicious patterns detected. This appears to be a normal {target}.\n" + \
                          f"Description: {item_desc}"
        
        # Check in inventory
        elif target in self.items:
            item_desc = self.items[target]
            
            # Analysis results for inventory items (similar logic as above)
            suspicious_terms = ['suspicious', 'unusual', 'strange', 'abnormal', 'unexpected']
            is_suspicious = any(term in item_desc.lower() for term in suspicious_terms)
            
            if is_suspicious:
                virus_hint = ""
                if 'boot' in item_desc.lower():
                    virus_hint = "This may be related to a boot sector infection."
                elif 'kernel' in item_desc.lower() or 'root' in item_desc.lower():
                    virus_hint = "This could indicate rootkit activity in the system."
                elif 'memory' in item_desc.lower():
                    virus_hint = "This pattern is consistent with memory-resident malware."
                elif 'firmware' in item_desc.lower() or 'bios' in item_desc.lower():
                    virus_hint = "This suggests possible firmware compromising."
                elif 'network' in item_desc.lower() or 'packet' in item_desc.lower():
                    virus_hint = "This is characteristic of network traffic interception."
                
                return f"Analysis of {target} in your inventory:\n\n" + \
                      f"SECURITY ALERT: This item shows signs of suspicious activity.\n" + \
                      f"Details: {item_desc}\n" + \
                      f"{virus_hint}"
            else:
                return f"Analysis of {target} in your inventory:\n\n" + \
                      f"No suspicious patterns detected. This appears to be a normal {target}.\n" + \
                      f"Description: {item_desc}"
        else:
            return f"There's no {target} here to analyze."

    def _increase_component_knowledge(self):
        """Helper method to increase knowledge based on current location"""
        if 'cpu' in self.location.name.lower() or 'alu' in self.location.name.lower() or 'register' in self.location.name.lower():
            self.knowledge['cpu'] = min(5, self.knowledge['cpu'] + 1)
        elif 'memory' in self.location.name.lower() or 'ram' in self.location.name.lower() or 'cache' in self.location.name.lower():
            self.knowledge['memory'] = min(5, self.knowledge['memory'] + 1)
        elif 'drive' in self.location.name.lower() or 'disk' in self.location.name.lower() or 'ssd' in self.location.name.lower() or 'hdd' in self.location.name.lower():
            self.knowledge['storage'] = min(5, self.knowledge['storage'] + 1)
        elif 'network' in self.location.name.lower() or 'interface' in self.location.name.lower():
            self.knowledge['networking'] = min(5, self.knowledge['networking'] + 1)
