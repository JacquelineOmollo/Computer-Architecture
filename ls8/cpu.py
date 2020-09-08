"""CPU functionality."""
import sys


HLT = 0b00000001  # Halt
LDI = 0b10000010  # Set the value of a register to an integer
PRN = 0b01000111  # Print
MUL = 0b10100010  # Multiply


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes
        self.reg = [0] * 8 # 8 register
        self.pc = 0
        self.running = True
        
    if len(sys.argv) != 2:
            print("Usage: ls8.py filename")
            sys.exit(1)
        
        
    def load(self,filename):
        """Load a program into memory."""
        address = 0
        
        print(sys.argv)
        
        try:
            with open(self.filename) as file:
                for line in file:
                    split_comment = line.split("#")
                    
                    number = split_comment[0].strip()
                    
                    if number == "":
                        continue
                    
                    if number[0] == "1" or number[0] == "0":
                        num = number[:8]
                        
                    self.ram[address] = int(num, 2)
                    address += 1
                        
        except FileNotFoundError:
            print(f"{sys.argv[0]} : {sys.argv[1]} file not found")
            sys.exit(2)
       

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b, MUL):
        """ALU operations."""

        if op == MUL:
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        

        
        while self.running:
            #Reads memory for reg and stores results in IR
            IR = self.ram_read(self.pc)
            #Reads bytes with pc+1
            operand_a = self.ram_read(self.pc + 1)
             #Reads bytes with pc+2
            operand_b = self.ram_read(self.pc + 2)
            
            self.pc += 1 + (IR >> 6)
            
            alu_command = ((IR >> 5) & 0b001) == 1
            
            if alu_command:
                self.alu(IR, operand_a, operand_b)
            
            if IR == LDI:
               self.reg[operand_a] = operand_b
               
            elif IR == PRN:
               print(self.reg[operand_a])

            elif IR == HLT:
                   self.running = False
                   
           
       