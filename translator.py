# Translator: ASM instructions to hex


OP_CODES = {
	'halt': 0, 'add': 1, 'sub': 2, 'mult': 3, 'div': 4, 'and': 5, 'or': 6,
	'xor': 7, 'shl': 8, 'shr': 9, 'slt': 10, 'sle': 11, 'seq': 12, 'load': 13,
	'store': 14, 'jmp': 15, 'braz': 16, 'branz': 17, 'scall': 18
}


# loads instructions in assembly from file and stores them in a list
def load_ASM(fileName):

	# place lines from file in array and remove trailing whitespaces
	lines = [line.rstrip('\n') for line in open(fileName)]
	# remove empty lines
	lines = [line for line in lines if line != '']
	print("-------")
	print(lines)
	print("-------")
	return lines


# receives a list of assembly instructions and converts them into lists of numbers
def analyze_instructions(asmInstructions):

	# transform each instruction into a list of words
	asmInstructions = [instruction.split() for instruction in asmInstructions]

    

	numInstructions = []
	print(asmInstructions)
	# convert each word in instruction into a number
	for asmInstr in asmInstructions:
		print(asmInstr)
		numInstr = []

		# convert operation name to operation code
		numInstr.append(OP_CODES[asmInstr[0]])

		# convert registers and immediates to num values
		if len(asmInstr) > 1:

			# remove 1st character ('r') of word and keep only number
			# 'r15' -> 15
			numInstr.append(int(asmInstr[1][1:]))

			# 0 if value is a register, 1 if value is an immediate value
			if asmInstr[2][0] == 'r':
				numInstr.append(0)
			else:
				numInstr.append(1)

			# remove 1st character ('r' or '#') of word and keep only number
			# 'r15' -> 15 | '#300' -> 300
			numInstr.append(int(asmInstr[2][1:]))

            
			if len(asmInstr) > 3:
				print("bon")
				numInstr.append(int(asmInstr[3][1:]))

		numInstructions.append(numInstr)

	return numInstructions


# receives a list of lists of numbers and converts them into hex instructions
def compute_hex_instructions(numInstructions):

	hexInstructions = []


    


	for numInstr in numInstructions:
		print(numInstructions)

		opcode = numInstr[0]
		if len(numInstr)>1:
			rd = numInstr[1]
		if len(numInstr)>2:
			rs = numInstr[2]
		if len(numInstr)>3:
			im = numInstr[3]

		opcode = opcode <<26
		rd = rd << 21
		rs = rs << 16
		im =(im )& (0x4f)
		valbin = opcode|rd|rs|im

        
		decInstr = 0
		decInstr += numInstr[0] << 26
        
		if len(numInstr) > 1:
			decInstr += numInstr[1] << 22
			decInstr += numInstr[2] << 21
		if len(numInstr)>3:	
			decInstr += numInstr[3] << 5
		if len(numInstr)>4:	
			decInstr += numInstr[4]
        
        
		hexInstructions.append(hex(decInstr))
        




		print(bin(valbin))
        
	return hexInstructions
	#print(hexInstructions)


# receives a list of hex instructions and a file name and writes instructions into file
def output_hex_instructions(hexInstructions, fileName):

	outputFile = open(fileName, 'w')
	for instr in hexInstructions:
		outputFile.write(instr + '\n')


inputFileName = 'asmInstructions.txt'
outputFileName = 'hexInstructions.txt'

asmInstructions = load_ASM(inputFileName)
print(asmInstructions)
numInstructions = analyze_instructions(asmInstructions)
hexInstructions = compute_hex_instructions(numInstructions)

output_hex_instructions(hexInstructions, outputFileName)
