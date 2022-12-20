import re
import numpy as np





#instruction_txt = "add r16 r2 r0"
#instruction_txt = "add r2 r6 100"
instruction_txt = "sub r1 r2 r3"
instru_bin = 000000|00000|00000|0000|00000000000
instru_bin << 2
print(bin(instru_bin))
#file = open('instructions_test.txt',"r")
#file = open('test_fibo.txt',"r")
#file.close()


#Gestion des labels

labels={}##la ou l'on va mettre les labels
instructions = []#tableau ou l'on met les instructions
label_use = {}##la ou on met les adrees des labels 

#

re_comment = re.compile("\s*#.*$")
re_label = re.compile("^([a-zA-Z_.9]+):$")
re_add = re.compile("^add\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_test = re.compile("\d")
re_addi= re.compile("^add\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_sub = re.compile("^sub\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_subi = re.compile("^sub\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_load = re.compile("^load\s+r(\d+),")
re_mul = re.compile("^mul\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_muli = re.compile("^mul\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_div = re.compile("^div\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_divi = re.compile("^div\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_and = re.compile("^and\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_andi = re.compile("^and\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_or = re.compile("^or\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_ori = re.compile("^or\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_xor = re.compile("^xor\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_xori = re.compile("^xor\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_shl = re.compile("^shl\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_shli = re.compile("^shl\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_slt = re.compile("^slt\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_slti = re.compile("^slt\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_shr = re.compile("^shr\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_shri = re.compile("^shr\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_sle = re.compile("^sle\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_slei = re.compile("^slei\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")
re_seq = re.compile("^seq\s+r(\d+)\s+r(\d+)\s+r(\d+)$")
re_seqi = re.compile("^seqi\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$")

#ADD
#txt_file = open('instructions_test.txt','r')
txt_file = open('test_fibo.txt','r')
#txt_file = open('test2.txt','r')
tableau = np.zeros(220)
a=0

DICT = {
        'add':{
            'opcode':2,
            'regex':"^add\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'addi':{
            'opcode':3,
            'regex':"^add\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'sub':{
           'opcode':4,
           'regex':"^sub\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
           'typ':"R"
        },
        'subi':{
           'opcode':5,
           'regex':"^sub\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
           'typ':"I"
        },
        'mul':{
            'opcode':6,
            'regex':"^mul\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'muli':{
            'opcode':7,
            'regex':"^mul\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'div':{
            'opcode':8,
            'regex':"^div\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'divi':{
            'opcode':9,
            'regex':"^div\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'and':{
            'opcode':10,
            'regex':"^and\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'andi':{
            'opcode':11,
            'regex':"^and\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'or':{
            'opcode':12,
            'regex':"^or\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'ori':{
            'opcode':13,
            'regex':"^or\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'xor':{
            'opcode':14,
            'regex':"^xor\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'xori':{
            'opcode':15,
            'regex':"^xor\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'shl':{
            'opcode':16,
            'regex':"^shl\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'shli':{
            'opcode':17,
            'regex':"^shl\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'shr':{
            'opcode':18,
            'regex':"^shr\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"I"
        },
        'shri':{
            'opcode':19,
            'regex':"^shr\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },


        'slt':
        {
            'opcode':20,
            'regex':"^slt\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },
        'slti':
        {
            'opcode':21,
            'regex':"^slt\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'sle':
        {
            'opcode':22,
            'regex':"^sle\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
        },

        'slei':
        {
            'opcode':23,
            'regex':"^sle\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",##Erreur dans le regex de sle
            'typ':"I"
        },

        'seq':
        {
            'opcode':24,
            'regex':"^seq\s+r(\d+)\s+r(\d+)\s+r(\d+)$",
            'typ':"R"
            

        },

        'seqi':
        {
            'opcode':25,
            'regex':"^seq\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'load':{
            'opcode':27,
            'regex':"^load\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'store':{
            'opcode':29,
            'regex':"^store\s+r(\d+),?\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"I"
        },
        'jump':
        {
            'opcode':30,
            'regex':"^jmp\s+r(\d+)\s+r(\d+)$",
            'typ':"JR"
        },
        
        'jumpi':
        {
            'opcode':31,
            'regex':"^jmp\s+(-?(0x)?[0-9a-fA-F]+)\s+r(\d+)$",
            'typ':"JI"
        },
         'jump_label':{
            'opcode':31,
            'regex':"^jmp\s+(\w+),?\s+r(\d+)",
            'typ':"JR_la"
        },
        'braz':
        {
            'opcode':32,
            'regex':"^braz\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"B"
        },

        'brazn':
        {
            'opcode':33,
            'regex':"^branz\s+r(\d+),?\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"B"
        },

        'braz_label':{
            'opcode':32,
            'regex':"^braz\s+r(\d+),?\s+((-?\w+)|([.]+(\w)))",
            'typ':"B_lab"
        },
        'brazn_label':{
            'opcode':33,
            'regex':"^branz\s+r(\d+),?\s+((-?\w+)|([.]+(\w)))",
            'typ':"B_lab"
        },

        'scall':
        {
            'opcode':34,
            'regex':"^scall\s+(-?(0x)?[0-9a-fA-F]+)$",
            'typ':"S"
        },
        'stop':
        {
            'opcode':35,
            'regex':"^stop$",
            'typ':"H"
        },
        'label':
        {
            'regex':"\w+|[.+\w+]",
            'typ':"label"
        }



        
#"""'scall1':
#{
#}
#"""
    

    }

while True:
    line = txt_file.readline()
    if not line:
        break
    line = line.strip()
    line = re_comment.sub('',line)
    if len(line)==0:
        continue

    

    
    print("La ligne est",line)
    for i in DICT:
        rec1= re.compile(DICT[i]['regex'])
        
        rec2= rec1.match(line)
        #print("La ligne est",line)

    ##C'est ici que l'on parcourt les lignes de toutes les instructions
        if rec2:
            if DICT[i]['typ']=="R":
                print("R reconnu")
                OP_CODE = DICT[i]['opcode'] 
                RD = int(rec2.group(1))
                RS1 = int(rec2.group(2))
                RS2 = int(rec2.group(3))
                print("L'opcode de l'instruction est",OP_CODE)
                OP_CODE = OP_CODE<<26
                RD = RD <<21
                RS1 = RS1 <<16
                RS2 = RS2 <<11
                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OP_CODE|RD|RS1|RS2
                print("L'instruction en binaire est",bin(instruction))
                print("==============")
                
                tableau[a]=instruction
                a=a+1
                break

            if DICT[i]['typ']=="I":
                print("I RECONNU")
                OP_CODE = DICT[i]['opcode'] 
                RD = int(rec2.group(1))
                RS = int(rec2.group(2))
                IM = int(rec2.group(3))
                print("L'opcode de l'instruction est",OP_CODE)

                OP_CODE = OP_CODE<<26
                RD = RD <<21
                RS = RS <<16
                IM = IM & 0x0000ffff
                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OP_CODE|RD|RS|IM
                print("L'instruction en binaire est",bin(instruction))
                print("==============")
                print(bin(instruction))
                print(len(bin(instruction)))

                tableau[a]=instruction
                a = a+1
                break

            ##Il s'agit d'une instrtuction comportant un label

            if DICT[i]['typ']=="JR":
                print("Il s'agit d'un jump sans label avec de type r")
                OP_CODE = DICT[i]['opcode'] 
                print("L'opcode de l'instruction est ",OP_CODE)
                OP_CODE = OP_CODE<<26
                RD = int(rec2.group(1))
                RA = int(rec2.group(2))

                
                RD = RD << 21
                RA =RA<<16
                

                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OP_CODE|RD|RA
                print("L'instruction en binaire est",bin(instruction))
                print("==============")
                
                tableau[a]=instruction
                a=a+1
                break



            if DICT[i]['typ']=="JI":
                print("Il s'agit d'un jump sans label avec de type ")
                OP_CODE = DICT[i]['opcode'] 
                print("L'opcode de l'instruction est ",OP_CODE)
                OP_CODE = OP_CODE<<26
                RD = int(rec2.group(1))
                addr = int(rec2.group(2))

                
                RD = RD << 21
                #RA =RA<<16
                

                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OP_CODE|RD|addr
                print("L'instruction en binaire est",bin(instruction))
                print("==============")
                
                tableau[a]=instruction
                a=a+1
                break


            if DICT[i]['typ']=="JR_la":
                print("Il s'agit d'une instruction jump  avec un label\n")


                OP_CODE = DICT[i]['opcode'] 
                print("L'opcode de l'instruction est ",OP_CODE)
                OP_CODE = OP_CODE<<26
                print("L'opcode de l'instruction en binaire est ",OP_CODE)
                RD = int(rec2.group(2))
                instruction = OP_CODE|RD
                print("L'instruction comportant le label sans l'adresse est maintenant",((instruction)))

                print("LA ligne avec le label avant d'etre split",line)
                ##print(line.split())
                print("========")
                print("Maintenant on a split")
                print("========")
                line = line.split()
                ##print(line)
                print(line[1])
                print("RD va etre égal à",line[2])
                label_use[a]= str(line[1])
                tableau[a]=instruction
                a=a+1
                break





            if DICT[i]['typ']=="B_lab":
                print("Il s'agit d'une instruction bran avec un label\n")


                OP_CODE = DICT[i]['opcode'] 
                print("L'opcode de l'instruction est ",OP_CODE)
                RS = int(rec2.group(1))
                OP_CODE = OP_CODE<<26
                RS = RS<<21
                print("L'opcode de l'instruction en binaire est ",OP_CODE)
                instruction = OP_CODE|RS
                print("L'instruction comportant le label sans l'adresse est maintenant",((instruction)))

                print("LA ligne avec le label avant d'etre split",line)
                ##print(line.split())
                print("========")
                print("Maintenant on a split")
                print("========")
                line = line.split()
                ##print(line)
                print(line[2])
                label_use[a]= str(line[2])
                print("LA clé slah indice va etre le label",line[2])
                tableau[a]=instruction
                a=a+1
                break


            ##Il s'agit d'un label


            if DICT[i]['typ']=="label":
                print("Il s'agit ici du label\n")
                #line = line.split(":")
                #print("La ligne va etre enfin la clé va etre  ,",line[0])
                print(">J> kla clé a aller cherher va etre ",line)
                labels[str(line)]=a
                
                break

            if DICT[i]['typ']=="B":
                print("B reconnu")
                OP_CODE = DICT[i]['opcode'] 
                RS = int(rec2.group(1))
                addr = int(rec2.group(2))
                
                print("L'opcode de l'instruction est",OP_CODE)
                print("Le registre testé est",RS)
                print("L'adresse à laquelle on va est ",addr)
                OP_CODE = OP_CODE<<26
                RS = RS<<21
                addr = addr 
                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OP_CODE|RS|addr
                print("L'instruction en binaire est",bin(instruction))
                print("==============")
                print(bin(instruction))
                print(len(bin(instruction)))

                tableau[a]=instruction
                a = a+1
                break
            
            if DICT[i]['typ']=="S":
                print("S RECONNU")
                OP_CODE = DICT[i]['opcode'] 
                n = int(rec2.group(1))
                
                print("L'opcode de l'instruction est",OP_CODE)
                print("Le n reconnu est ",n)
                OP_CODE = OP_CODE<<26
                
                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OP_CODE|n
                print("L'instruction en binaire est",bin(instruction))
                print("==============")
                print(bin(instruction))
                print(len(bin(instruction)))

                tableau[a]=instruction
                a = a+1
                break
            if DICT[i]['typ']=="H":
                OPCODE = DICT[i]['opcode']
                OPCODE = OPCODE <<26
                print("C'est l'instruction stop")
                print("L'opcode de l'instruction est",OPCODE)
                print("L'opcode de l'instruction est",bin(OP_CODE))
                print("===========")
                print("===========")

                instruction = OPCODE

                tableau[a]=instruction
                a = a+1
                break
            



##On s'occupe maintenant des labels

print("========")
print("========")
print("Les labels sont",labels)
print("========")
print("========")
print("Les labels_use sont",label_use)
print("========")
print("========")
print("On s'occupe maintenant des labels")
for i in label_use:
    a = i#adress est égale à l'adresse ou une instruction comportait un label
    print("L'adrresse à laquelle on revient pour le label est  ",a)
    print("Il y a actuellement dans le tableau ",tableau[a])
    print("On va remplacer par",labels[label_use[i]])
    tableau[a]= int(tableau[a])|labels[label_use[i]]
    print("La nouvelle instruction est ",tableau[a])
    print("La nouvelle instruction en binaire est ",bin(int(tableau[a])))
    f2 = int(tableau[a])


    print("=======")
    print("=======")
    print("=======")
    print("=======")
    print("Vérification du label")
    
    

    opcode2 = (f2 >> 26) & 0x3f
    ra2 =( bin(int(f2)) )
    """print("on a un opcode de",opcode2)
    print("On va au registre  ",ra2)"""


    

print("Letableau est",tableau)
"""for i in range(len(tableau)):
    print (bin(int(tableau[i])))"""


#Ecriture du fichier de sortie
v=0
v=int(v)

import struct

out_file = open('fichier.bin','wb')

for num in tableau:

    out_file.write(struct.pack('<L',int(num)))



out_file.close    