#!/usr/bin/env python3
"""
Educational minigames for ComputerQuest
"""

class CPUPipelineMinigame:
    """
    Educational minigame that teaches CPU pipeline concepts
    Can be triggered when player reaches CPU_Core with sufficient CPU knowledge
    """
    def __init__(self, game):
        self.game = game
        self.instructions = [
            # Each instruction has: opcode, operands, current_stage, cycles_per_stage
            # Stages: 0=fetch, 1=decode, 2=execute, 3=memory, 4=writeback, 5=complete
            {"opcode": "LOAD", "operands": "R1, [0x1000]", "current_stage": 0, "cycles_per_stage": [1, 1, 1, 2, 1]},
            {"opcode": "ADD", "operands": "R2, R1, #5", "current_stage": 0, "cycles_per_stage": [1, 1, 2, 0, 1]},
            {"opcode": "SUB", "operands": "R3, R2, #2", "current_stage": 0, "cycles_per_stage": [1, 1, 2, 0, 1]},
            {"opcode": "STORE", "operands": "R3, [0x1004]", "current_stage": 0, "cycles_per_stage": [1, 1, 1, 2, 0]},
            {"opcode": "JUMP", "operands": "LABEL1", "current_stage": 0, "cycles_per_stage": [1, 1, 1, 0, 0]}
        ]
        self.cycle = 0
        self.max_cycles = 20
        self.pipelined = True  # Toggle between pipelined and non-pipelined
        self.stalled = False
        self.data_hazards = []
        self.structural_hazards = []
        self.completed = False
        self.score = 0
        
        # Register state
        self.registers = {"R1": 0, "R2": 0, "R3": 0, "PC": 0}
        self.memory = {0x1000: 42, 0x1004: 0}
        
        # Stage names for display
        self.stage_names = ["Fetch", "Decode", "Execute", "Memory", "Writeback", "Complete"]
        
    def toggle_pipeline(self):
        """Toggle between pipelined and non-pipelined execution"""
        self.pipelined = not self.pipelined
        # Reset the simulation
        self.reset()
        return f"CPU is now running in {'pipelined' if self.pipelined else 'non-pipelined'} mode."
        
    def reset(self):
        """Reset the simulation to initial state"""
        self.cycle = 0
        for instr in self.instructions:
            instr["current_stage"] = 0
        self.registers = {"R1": 0, "R2": 0, "R3": 0, "PC": 0}
        self.memory = {0x1000: 42, 0x1004: 0}
        self.data_hazards = []
        self.structural_hazards = []
        self.completed = False
        self.score = 0
        return "CPU pipeline simulation reset."
        
    def step(self):
        """Advance the simulation by one cycle"""
        if self.completed:
            return "Simulation complete. Use 'reset' to start again."
            
        self.cycle += 1
        if self.cycle > self.max_cycles:
            return "Maximum cycle count reached. Simulation terminated."
            
        # Advance each instruction according to pipeline rules
        if self.pipelined:
            self._step_pipelined()
        else:
            self._step_non_pipelined()
            
        # Check if all instructions are complete
        if all(instr["current_stage"] == 5 for instr in self.instructions):
            self.completed = True
            
            # Calculate score based on how efficiently the pipeline was used
            efficiency = len(self.instructions) * 5 / self.cycle
            self.score = int(efficiency * 100)
            
            return self.get_status() + f"\n\nSimulation complete in {self.cycle} cycles!\nPipeline Efficiency: {efficiency:.2f}\nScore: {self.score}/100"
        
        return self.get_status()
        
    def _step_pipelined(self):
        """Process one cycle in pipelined mode"""
        # Process instructions in reverse order (from most progressed to least)
        # This prevents multiple instructions from advancing to the same stage in one cycle
        instructions_by_stage = sorted(
            enumerate(self.instructions), 
            key=lambda x: x[1]["current_stage"], 
            reverse=True
        )
        
        # Track which stages are in use this cycle
        stages_in_use = set()
        
        for idx, instr in instructions_by_stage:
            current_stage = instr["current_stage"]
            
            # Skip completed instructions
            if current_stage == 5:
                continue
                
            # Check for structural hazards (same stage used by multiple instructions)
            if current_stage in stages_in_use and current_stage < 5:
                self.structural_hazards.append(f"Instruction {idx+1} stalled at {self.stage_names[current_stage]} stage due to structural hazard")
                continue
                
            # Check for data hazards (dependencies between instructions)
            hazard = self._check_data_hazards(idx)
            if hazard:
                self.data_hazards.append(hazard)
                continue
                
            # Mark this stage as in use
            stages_in_use.add(current_stage)
            
            # Execute the instruction's current stage
            self._execute_stage(idx, instr, current_stage)
            
            # Advance to next stage if current stage is complete
            instr["cycles_per_stage"][current_stage] -= 1
            if instr["cycles_per_stage"][current_stage] <= 0:
                instr["current_stage"] += 1
                # If we moved to a new stage, record it as in use too
                if instr["current_stage"] < 5:
                    stages_in_use.add(instr["current_stage"])
    
    def _step_non_pipelined(self):
        """Process one cycle in non-pipelined mode"""
        # In non-pipelined mode, only one instruction is active at a time
        for idx, instr in enumerate(self.instructions):
            # Find the first non-completed instruction
            if instr["current_stage"] < 5:
                current_stage = instr["current_stage"]
                
                # Execute the stage
                self._execute_stage(idx, instr, current_stage)
                
                # Advance if current stage is complete
                instr["cycles_per_stage"][current_stage] -= 1
                if instr["cycles_per_stage"][current_stage] <= 0:
                    instr["current_stage"] += 1
                
                # Only process one instruction per cycle in non-pipelined mode
                break
    
    def _check_data_hazards(self, instr_idx):
        """Check for data hazards between instructions"""
        instr = self.instructions[instr_idx]
        current_stage = instr["current_stage"]
        
        # Only check for hazards in decode and execute stages
        if current_stage not in [1, 2]:
            return None
            
        # Extract register dependencies
        depends_on = set()
        writes_to = set()
        
        # Determine register dependencies based on instruction type
        opcode = instr["opcode"]
        operands = instr["operands"].split(", ")
        
        if opcode == "LOAD":
            writes_to.add(operands[0])  # Register being loaded into
        elif opcode == "ADD" or opcode == "SUB":
            writes_to.add(operands[0])  # Destination register
            depends_on.add(operands[1])  # Source register
            # operands[2] might be immediate or register
            if operands[2].startswith("R"):
                depends_on.add(operands[2])
        elif opcode == "STORE":
            depends_on.add(operands[0])  # Register being stored
        
        # Check if any previous instructions write to registers this one depends on
        for prev_idx in range(instr_idx):
            prev_instr = self.instructions[prev_idx]
            prev_stage = prev_instr["current_stage"]
            
            # Skip if previous instruction is completed writeback
            if prev_stage >= 5:
                continue
                
            # Determine what registers the previous instruction writes to
            prev_writes_to = set()
            prev_opcode = prev_instr["opcode"]
            prev_operands = prev_instr["operands"].split(", ")
            
            if prev_opcode == "LOAD":
                prev_writes_to.add(prev_operands[0])
            elif prev_opcode == "ADD" or prev_opcode == "SUB":
                prev_writes_to.add(prev_operands[0])
            
            # Check for overlap between what this instruction depends on and what previous ones write to
            conflict = depends_on.intersection(prev_writes_to)
            if conflict:
                return f"Instruction {instr_idx+1} stalled due to data dependency on register(s) {', '.join(conflict)}"
        
        return None
    
    def _execute_stage(self, idx, instr, stage):
        """Execute the current stage of an instruction"""
        opcode = instr["opcode"]
        operands = instr["operands"].split(", ")
        
        # Only perform actual execution in appropriate stages
        if stage == 2:  # Execute stage
            if opcode == "ADD":
                dest_reg = operands[0]
                src_reg = operands[1]
                if operands[2].startswith("#"):
                    value = int(operands[2][1:])
                else:
                    value = self.registers[operands[2]]
                self.registers[dest_reg] = self.registers[src_reg] + value
            elif opcode == "SUB":
                dest_reg = operands[0]
                src_reg = operands[1]
                if operands[2].startswith("#"):
                    value = int(operands[2][1:])
                else:
                    value = self.registers[operands[2]]
                self.registers[dest_reg] = self.registers[src_reg] - value
                
        elif stage == 3:  # Memory stage
            if opcode == "LOAD":
                dest_reg = operands[0]
                mem_addr = int(operands[1].strip("[]"), 16)
                self.registers[dest_reg] = self.memory[mem_addr]
            elif opcode == "STORE":
                src_reg = operands[0]
                mem_addr = int(operands[1].strip("[]"), 16)
                self.memory[mem_addr] = self.registers[src_reg]
    
    def get_status(self):
        """Return a formatted status of the CPU pipeline simulation"""
        result = f"CPU Pipeline Simulation - Cycle {self.cycle}\n"
        result += f"Mode: {'Pipelined' if self.pipelined else 'Non-Pipelined'}\n\n"
        
        # Display the pipeline stages
        result += "Pipeline Status:\n"
        result += "  " + "".join(f"{name:<10}" for name in self.stage_names) + "\n"
        
        for i, instr in enumerate(self.instructions):
            line = f"{i+1}: "
            for stage in range(6):
                if instr["current_stage"] == stage:
                    line += f"[{instr['opcode']}] "
                elif instr["current_stage"] > stage:
                    line += "[DONE]    "
                else:
                    line += "[    ]    "
            line += f" {instr['opcode']} {instr['operands']}"
            result += line + "\n"
        
        # Display register and memory state
        result += "\nRegister State:\n"
        for reg, value in self.registers.items():
            result += f"  {reg}: {value}\n"
        
        result += "\nMemory State:\n"
        for addr, value in self.memory.items():
            result += f"  0x{addr:04x}: {value}\n"
        
        # Display hazards
        if self.data_hazards or self.structural_hazards:
            result += "\nHazards This Cycle:\n"
            for hazard in self.data_hazards + self.structural_hazards:
                result += f"  - {hazard}\n"
            
        return result

    def explain(self):
        """Provide an educational explanation of CPU pipelining"""
        return """
CPU PIPELINE EXPLANATION:

A CPU pipeline breaks instruction execution into stages that can run in parallel.
The 5 basic stages are:

1. Fetch: Get the instruction from memory
2. Decode: Determine what the instruction does
3. Execute: Perform the operation (ALU)
4. Memory: Access memory if needed
5. Writeback: Store the result in registers

Pipelined execution allows multiple instructions to be processed simultaneously,
with each in a different stage. This increases throughput (instructions per second).

However, pipelining introduces hazards:
- Data Hazards: When an instruction depends on data from a previous instruction
- Structural Hazards: When two instructions need the same hardware resource
- Control Hazards: When the program flow changes (branches, jumps)

This simulation demonstrates how pipelining improves performance and
shows the impact of data and structural hazards.

Try toggling between pipelined and non-pipelined modes to compare!
"""

class MemoryHierarchyMinigame:
    """Placeholder for a memory hierarchy simulation minigame"""
    def __init__(self, game):
        self.game = game
        
    def explain(self):
        """Provide educational explanation about memory hierarchy"""
        return """
MEMORY HIERARCHY EXPLANATION:

The memory hierarchy in a computer balances speed, capacity, and cost:

1. CPU Registers: Fastest but very limited capacity
2. Cache Memory: Very fast, small capacity (L1, L2, L3)
3. Main Memory (RAM): Slower than cache, much larger capacity
4. Storage (SSD/HDD): Very large capacity, but much slower access

When the CPU needs data, it looks in this order:
1. Check if data is in registers
2. If not, check L1 cache
3. If not, check L2 cache
4. If not, check L3 cache
5. If not, retrieve from main memory (RAM)
6. If not in RAM, load from storage

This creates a "memory hierarchy" with speed decreasing and 
capacity increasing as you move down the hierarchy.

This system takes advantage of two principles:
- Temporal Locality: Recently used data will likely be used again soon
- Spatial Locality: Data near recently used data will likely be needed soon

For future implementation of this minigame!
"""