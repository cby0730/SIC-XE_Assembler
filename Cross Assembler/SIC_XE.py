from itertools import zip_longest
from typing import Optional
no_operand = {'FIX': 'C4', 'FLOAT': 'C0', 'HIO': 'F4', 'NORM': 'C8', 'RSUB': '4C', 'SIO': 'F0', 'TIO': 'F8'}

one_operand = {"ADD": '18', "ADDF": '58', 'AND': '40', 'CLEAR': 'B4', 'COMP': '28', 'COMPF': '88', 'DIV': '24', 'DIVF': '64', 'J': '3C', 'JEQ': '30'
, 'JGT': '34', 'JLT': '38', 'JSUB': '48', 'LDA': '00', 'LDB': '68', 'LDF': '70', 'LDL': '08', 'LDS': '6C', 'LDT': '74', 'LDX': '04'
, 'LPS': 'D0', 'MUL': '20', 'MULF': '60', 'OR': '44', 'RD': 'D8', 'SSK': 'EC', 'STA': '0C', 'STB': '78', 'STF': '80', 'STI': 'D4', 'LDCH': '50', 'STCH': '54'
, 'STL': '14', 'STS': '7C', 'STSW': 'E8', 'STT': '84', 'STX': '10', 'SUB': '1C', 'SUBF': '5C', 'SVC': 'B0', 'TD': 'E0', 'TIX': '2C', "TIXR" : 'B8', 'WD': 'DC' }

two_operand_reg = {'ADDR': '90', 'COMPR': 'A0', 'DIVR': '9C', 'MULR': '98', 'RMO': 'AC', 'SUBR': '94'}
two_operand_n = {'SHIFTL': 'A4', 'SHIFTR': 'A8'}

opcode_table = {"ADD" : [3, '18'], "ADDF" : [3,'58'], "ADDR" : [2,'90'],"AND" : [3, '40'], "CLEAR" : [2, 'B4'], "COMPF" : [3, '88'], "COMPR" : [2, 'A0'], "COMP" : [3, '28']
, "DIVF" : [3, '64'], "DIVR" : [2, '9C'], "DIV" : [3, '24'], "FIX" : [1, 'C4'], "FLOAT" : [1, 'C0'], "HIO" : [1, 'F4'], "J" : [3, '3C']
, "JEQ" : [3, '30'], "JGT" : [3, '34'], "JLT" : [3, '38'], "JSUB" : [3, '48'], "LDA" : [3, '00'], "LDB" : [3, '68'], "LDCH" : [3, '50'], "LDF" : [3, '70']
, "LDL" : [3, '08'], "LDS" : [3, '6C'], "LDT" : [3, '74'], "LDX" : [3, '04'], "LPS" : [3, 'E0'], "UML" : [3, '20'], "MULF" : [3, '60'], "MULR" : [2, '98'], "NORM" : [1, 'C8']
, "OR" : [3, '44'], "RD" : [3, 'D8'], "RMO" : [2, 'AC'], "RSUB" : [3, '4C'], "SHIFTL" : [2, 'A4'], "SHIFTR" : [2, 'A8'], "SIO" : [1, 'F0'], "SSK" : [3, 'EC'], "STA" : [3, '0C']
, "STB" : [3, '78'], "STCH" : [3, '54'], "STF" : [3, '80'], "STI" : [3, 'D4'], "STL" : [3, '14'], "STSW" : [3, 'E8'], "STS" : [3, '7C'], "STT" : [3, '84'], "STX" : [3, '10']
, "SUBF" : [3, '5C'], "SUBR" : [2, '94'], "SUB" : [3, '1C'], "SVC" : [2, 'B0'], "TD" : [3, 'E0'], "TIO" : [1, 'F8'], "TIXR" : [2, 'B8'], "TIX" : [3, '2C'], "WD" : [3, 'DC']}

def hash(input, list) :
    return_num = 0
    for a in input :
        return_num += ord(a)
    return_num = return_num%100

    for index in range(len(list)) :
        if input == list[index] :
            return index
    
    while list[return_num] != '' :
        return_num += 1
        if return_num > 99 :
            return_num = 0
    return return_num

def is_digit(input) :
    if input[-1] == 'H' :
        for char in input[:-1] : #If any of char is not in the range, return false
            if not((char>='0' and char <= '9') or (char>='a' and char <= 'f') or (char>='A' and char <= 'F')) :
                return False
        return True
    elif not input.isdigit() : #If still not a digit, return false
        return False
    else : #Return True
        return True

def remove_enter(input) :
    if input[-1] == '\n' :
        return input[:-1]
    else :
        return input

def insert_zero(input, number) :
    number = number - len(input)

    temp = ''
    for i in range(number) :
        temp = temp + '0'
    temp = temp + input

    return temp

def hex2(a) :
    return a>0 and hex(a) or hex(a&0xfff)

class lexical_analysis:

    #Set three hash table
    t5 = ['']*100
    t6 = ['']*100
    t7 = ['']*100
    #Set three hash table

    #Set "token table" and "position table"
    #line = list()
    #position = list()
    #Set "token table" and "position table"

    location = []
    line_information = []

    def get_token(self):
        ''''''
        filename = input('Please input a file name(.txt is no need to type in) : ')
        filename += '.txt'
        f = open(filename, 'r')

        #output_file = open('output.txt', 'w')

        a = input("Please input SIC(input 0) or SIC/XE(input 1) :")

        delima = [',', '#', '@', '=', '?', ':', ';', '.', '*', '+', '-', '/']
        sperate = [' ', '\t', '\n']
        temp = ''

        syntax = SIC_syntax_error()
        assembler = SIC_object_code()
        syntax_xe = SICXE_syntax_analysis()
        assembler_xe = SICXE_object_code()
        keep_str_flag = 0
        instrucion = {}
        
        #Catch every lines
        for str_line in f :

            str_flag = 0
            #print(str_line)
            #output_file.write(remove_enter(str_line)+'\n')
            site = []
            list = []
            temp_line_information = {}

            #Get every char in the line
            for char in str_line :
                
                if char == '.' and str_flag == 0 : #comment
                    if temp != '' : #If there is something in the temp, append first
                        list.append(temp)
                        site.append(self.find_table(temp))
                        temp = ''
                    list.append('.') 
                    site.append(self.find_table('.'))
                    break #everything behind the '.' is no need to get, so skip to the next line

                elif char == '\'' : #Meaning String
                    if temp != '' and str_flag == 1 : #Occur to the second ', append and find
                        list.append(temp) #C ==> String type
                        site.append(self.str_table(temp)) #Special function for dealing String
                        list.append('\'')
                        site.append(self.find_table('\''))
                        temp = ''
                        str_flag = 0
                    elif temp != '' and str_flag == 2 :
                        list.append(temp.strip()) #X ==> number type
                        site.append(self.find_table(temp.strip()+'H')) #Because it is a hex number
                        list.append('\'')
                        site.append(self.find_table('\''))
                        temp = ''
                        str_flag = 0
                    else :
                        if temp.upper() == 'C' : #Occur to the first ' , judge C or X
                            str_flag = 1
                        elif temp.upper() == 'X' :
                            str_flag = 2
                        temp = ''
                        list.append('\'')
                        site.append(self.find_table('\''))

                elif char in sperate and str_flag == 0 : #Occur to the sperate, append and find
                    if temp != '' :
                        list.append(temp.strip())
                        site.append(self.find_table(temp.strip()))
                        temp = ''

                elif char in delima and str_flag == 0 : #Occur to the delima, append and find both of temp and delima
                    if temp != '' : #Append temp first if there is something in it
                        list.append(temp.strip())
                        site.append(self.find_table(temp.strip()))
                        temp = ''
                    temp += char #Then append the delima
                    list.append(temp.strip())
                    site.append(self.find_table(temp.strip()))
                    temp = ''

                else :
                    temp += char
                
                if str_flag != 0 :
                    keep_str_flag = str_flag #Track down the wether it is C'EOF or X'F1'

            if temp != '' : # If there still have a token in temp
                list.append(temp.strip())
                site.append(self.find_table(temp.strip()))
                temp = ''

            if a.upper() == '0' :
                instrucion = syntax.syntax(list, site, keep_str_flag) #Check Syntax and return instruction information

                if len(self.line_information) == 0 :
                    line_number = assembler.pass1(instrucion, assembler.LOCCTR, 0)
                else :
                    line_number = assembler.pass1(instrucion, assembler.LOCCTR, self.line_information[-1]['location']) #pass 1, put label into label table and return current line
                
                if line_number == None and str_line.strip() == "" : # If the line is empty
                    pass
                else :
                    temp_line_information = {'location' : line_number, 'instruction' : str_line.strip('\n'), 'instruction_info' : instrucion}
                    self.line_information.append(temp_line_information)
            
            elif a.upper() == '1' :
                instrucion = syntax_xe.syntax(list, site, keep_str_flag) #Check Syntax and return instruction information

                if len(self.line_information) == 0 :
                    line_number = assembler_xe.pass1(instrucion, assembler_xe.LOCCTR, 0)
                else :
                    line_number = assembler_xe.pass1(instrucion, assembler_xe.LOCCTR, self.line_information[-1]['location']) #pass 1, put label into label table and return current line
                
                if line_number == None and str_line.strip() == "" : # If the line is empty
                    pass
                else :
                    temp_line_information = {'location' : line_number, 'instruction' : str_line.strip('\n'), 'instruction_info' : instrucion}
                    self.line_information.append(temp_line_information)

            keep_str_flag = 0 #Initial the flag which track down the wether it is C'EOF or X'F1'
        
        if a.upper() == '0' :
            self.line_information = assembler.pass2(self.line_information)
        elif a.upper() == '1' :
            self.line_information = assembler_xe.pass2(self.line_information)
        
        f.close()

    def find_table(self, input) :

        t1 = open('Table1.table', 'r') #Find table1
        count = 1
        for str in t1 :
            if input.upper() == str.strip().upper() :
                t1.close()
                return [1, count] 
            count += 1 
        t1.close()

        t2 = open('Table2.table', 'r') #Find table2
        count = 1
        for str in t2  :
            if input.upper() == str.strip().upper() : #If find the same, return the table number and position
                t2.close()
                return [2, count]
            count += 1 
        t2.close()

        t3 = open('Table3.table', 'r') #Find table3
        count = 1
        for str in t3 :
            if input.upper() == str.strip().upper() : #If find the same, return the table number and position
                t3.close()
                return [3, count] 
            count += 1 
        t3.close()

        t4 = open('Table4.table', 'r') #Find table4
        count = 1
        for str in t4 :
            if input.upper() == str.strip().upper() : #If find the same, return the table number and position
                t4.close()
                return [4, count] 
            count += 1
        t4.close()

        #If input is not in table 1、2、3 and 4, then use the table 5 and 6

        if is_digit(input) : #If it is a number, give it to the hash function and put in the hash index
            if input[-1] == 'H' :
                index = hash(input[:-1], self.t6) # X'05', hex type. Change it from 05H to 05.
            else:
                index = hash(input, self.t6) # pure digit, dec
            self.t6[index] = input
            return [6,index]
        else : #If it is a message, give it to the hash function and put in the hash index
            index = hash(input, self.t5) 
            self.t5[index] = input
            return [5,index]
            
        #If input is not in table 1、2、3 and 4, then use the table 5 and 6

    def str_table(self, input) : # If it is a String, give it to the hash function and put in the hash index
        index = hash(input, self.t7)
        self.t7[index] = input
        return [7,index]

class SIC_syntax_error :

    def syntax(self, token, kind, c_or_x) :

        opcode = 1
        persudo = 2
        label = 5
        seperate = [4, 1]
        str = [4,9]
        reg = 3
        operand = [5, 6, 7]
        def_label = [6, 7]

        if len(token) == 0 and len(kind) == 0 : #prevent empty list
            return
        elif token[0].upper().strip() == '.' :
            return
        elif token[0].upper().strip() == 'LTORG' :
            return_line = {'opcode' : token[0]}
            return return_line

        if token[-1] == '.' :
            token.pop()
#==============================================================================================================================
        if kind[0][0] == label : #When the first token is label

            if kind[1][0] == persudo : # e.g THREE WORD 3, one label, one persudo, one integer or string

                if kind[2] == str and kind[4] == str : # EOF BYTE C'EOF', one label, one persudo, ' interger or string '
                    if kind[3][0] in def_label :
                        if c_or_x == 1 :
                            return_line = {'label' : token[0], 'opcode' : token[1], 'string' : token[3] }
                            return return_line
                        else :
                            return_line = {'label' : token[0], 'opcode' : token[1], 'hex' : token[3] }
                            return return_line
                    else :
                        print('syntax error')
                else :
                    
                    if len(token) == 5: 
                        if token[1].upper().strip() == 'EQU' and kind[2][0] == label and kind[4][0] == label : #MAXLEN EQU BUFEND-BUFFER
                            return_line = {'label' : token[0], 'opcode' : token[1],'symbol' : token[2], 'operator' : token[3], 'symbol2' : token[4] }
                            return return_line
                        else :
                            print('syntax error')

                    if kind[2][0] in def_label : # INPUT BYTE 1 or BUFFER EQU 3
                        return_line = {'label' : token[0], 'opcode' : token[1], 'operand' : token[2] }
                        return return_line

                    elif kind[2][0] == 4 and token[1].upper().strip() != 'WORD' : # LENGTH EQU *
                        return_line = {'label' : token[0], 'opcode' : token[1], 'delimiter' : token[2] }
                        return return_line

                    elif kind[2][0] == label and token[1].upper().strip() != 'WORD' : #LENGTH EQU BUFFER
                        return_line = {'label' : token[0], 'opcode' : token[1], 'symbol' : token[2] }
                        return return_line

                    else :
                        print("syntax error") #the thing to define label must be in the table 6 or 7

            elif kind[1][0] == opcode : #When opcode is the second
                
                if token[1].upper().strip() in one_operand.keys() : # one operand kind

                    if len(token) == 3 : # ex. ENDFIL LDA LENGTH, three token, one label, one opcode, one operand
                        if kind[2][0] in operand :
                            return_line = {'label' : token[0], 'opcode' : token[1], 'symbol' : token[2] }
                            return return_line
                        else :
                            print("syntax error")

                    elif len(token) == 4 : # ENDFIL LDA =3277

                        if token[2].upper().strip() == '=' : #Literal
                            return_line = {'label' : token[0], 'opcode' : token[1], 'literal' : token[3]}
                            return return_line

                        else :
                            print("syntax error")

                    elif len(token) == 5 : # e.g ENDFIL STCH BUFFER,X
                    
                        if kind[2][0] == label and kind[3] == seperate and token[4].upper().strip() == 'X':
                            return_line = {'label' : token[0], 'opcode' : token[1], 'symbol' : token[2], 'operand2' : token[4] }
                            return return_line
                        else :
                            print('syntax error')

                    elif len(token) == 6 : # e.g ENDFIL LDA =C'EOF' or ENDFIL LDA =X'F1'

                        if kind[3] == str and kind[5] == str and token[2].upper().strip() == '=' :
                            if c_or_x == 1 :
                                return_line = {'label' : token[0], 'string' : 'C', 'opcode' : token[1], 'literal' : token[4], 'format' : 3}
                                return return_line
                            else :
                                return_line = {'label' : token[0], 'hex' : 'X', 'opcode' : token[1], 'literal' : token[4], 'format' : 3}
                                return return_line

                    else :
                        print("syntax error")
                
                else :
                    print("syntax error")

            else :
                print("syntax error")
#==============================================================================================================================                
        elif kind[0][0] == opcode : # if the first token is opcode

            if token[0].upper().strip() in no_operand.keys() : # no operand kind
                
                if len(token) == 1 : # ex. RSUB, one token, one opcode, no operand
                    return_line = {'opcode' : token[0]}
                    return return_line
                else :
                    print("syntax error")

            elif token[0].upper().strip() in one_operand.keys() : # one operand kind

                if len(token) == 2 : # ex. LDA LENGTH, two token, one opcode, one operand
                    if kind[1][0] in operand :
                        return_line = {'opcode' : token[0], 'symbol' : token[1] }
                        return return_line
                    else :
                        print("syntax error")

                elif len(token) == 3 : # LDA =3277 

                    if token[1].strip() == '=' and kind[2][0] == 6 : #Literal
                        return_line = {'opcode' : token[0], 'literal' : token[2]}
                        return return_line

                    else :
                        print("syntax error")

                elif len(token) == 4 : # e.g STCH BUFFER,X, four token, one opcode, one buffer, one seperate, one index address
                    
                    if kind[1][0] == label and kind[2] == seperate and token[3].upper().strip() == 'X':
                        return_line = {'opcode' : token[0], 'symbol' : token[1], 'operand2' : token[3] }
                        return return_line
                    else :
                        print('syntax error')

                elif len(token) == 5 : # e.g LDA =C'EOF' or LDA =X'F1'

                    if kind[2] == str and kind[4] == str and token[1].upper().strip() == '=' :
                        if c_or_x == 1 :
                            return_line = {'opcode' : token[0], 'string' : 'C', 'literal' : token[3]}
                            return return_line
                        else :
                            return_line = {'opcode' : token[0], 'hex' : 'X', 'literal' : token[3]}
                            return return_line

                else :
                    print("syntax error")
            
            else :
                print("syntax error")
#==============================================================================================================================
        elif token[0].upper().strip() == 'END' :
            
            if kind[1][0] == label : # e.g END FIRST
                return_line = {'opcode' : token[0], 'symbol' : token[1]}
                return return_line
            else :
                print("syntax error")
#==============================================================================================================================
        elif kind[0][0] == persudo : # e.g WORD 3, one persudo, one integer or string

            if kind[1] == str and kind[3] == str : # BYTE C'EOF', one persudo, ' interger or string '
                if kind[2][0] in def_label :
                    if c_or_x == 1 :
                        return_line = { 'opcode' : token[0], 'string' : token[2] }
                        return return_line
                    else :
                        return_line = { 'opcode' : token[0], 'hex' : token[2] }
                        return return_line
                else :
                    print('syntax error')
            else :

                if kind[1][0] in def_label and token[0].upper() != 'EQU' : # BYTE 1
                    return_line = {'opcode' : token[0], 'operand' : token[1] }
                    return return_line

                else :
                    print("syntax error") #the thing to define label must be in the table 6 or 7
#==============================================================================================================================
        else :
            print("syntax error")

class SIC_object_code :

    label_table = dict()
    literal = dict()
    literal_list = []
    literal_table = []
    literal_address = []
    starting_address = hex(0)
    LOCCTR = hex(0)

    def pass1(self, instruction, cur_line, last_line) : # cur_line will be 0xabc format

        if not instruction :
            return

        if instruction['opcode'].upper().strip() == 'START' : # initial the first line
            self.starting_address = hex(int(instruction['operand'], 16))
            self.LOCCTR = self.starting_address
            return self.LOCCTR

        if 'label' in instruction.keys() : # First token is label
            if instruction['label'] in self.label_table.keys() :
                print('Duplicate label') #Found same label
            else :
                self.label_table.setdefault(instruction['label'], cur_line[2:])#Insert new label in label table

        if 'literal' in instruction.keys() : # There is a literal in instruction
            self.literal_table.append(cur_line) #Insert new label in label table

            if 'string' in instruction.keys() :
                self.literal.setdefault('=C\''+instruction['literal']+'\'', instruction['literal'])
            elif 'hex' in instruction.keys() :
                self.literal.setdefault('=X\''+instruction['literal']+'\'', instruction['literal']) 
            else :
                self.literal.setdefault(instruction['literal'], instruction['literal'])

        if instruction['opcode'].upper().strip() == 'LTORG' or instruction['opcode'].upper().strip() == 'END' :
            for value in self.literal_table :
                self.literal_address.append(hex(int(last_line, 16) - int(value, 16))[2:])
            self.literal_table.clear()
            
            temp_dict = self.literal.copy()
            self.literal_list.append(temp_dict)
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16)*len(temp_dict))
            self.literal.clear()
            return

        if instruction['opcode'].upper().strip() == 'BYTE' :  # Caculate the length of BYTE, two cases: C and X

            if 'string' in instruction.keys() : # e.g EOF BYTE C'EOF', length is 3
                self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16))
            else : # e.g INPUT BYTE X'F1', length is 1
                self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x1', 16))

        elif instruction['opcode'].upper().strip() == 'RESW' : # Caculate the length of RESW
            self.LOCCTR = hex(int(cur_line[2:], 16) + int(hex(int(instruction['operand'])), 16)*3)

        elif instruction['opcode'].upper().strip() == 'RESB' :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int(hex(int(instruction['operand'])), 16))

        elif instruction['opcode'].upper().strip() == 'EQU' :
            if 'operator' in instruction.keys() :

                if instruction['operator'] == '-' :
                    if instruction['symbol'] in self.label_table.keys() : #If 
                        a = int(self.label_table[instruction['symbol']], 16)
                    else :
                        a = 0
                    if instruction['symbol2'] in self.label_table.keys() :
                        b = int(self.label_table[instruction['symbol2']], 16)
                    else :
                        b = 0
                    cur_line = hex(a - b)
                    cur_line = hex(int(cur_line, 16)&0xffff)

                elif instruction['operator'] == '+' :
                    if instruction['symbol'] in self.label_table.keys() : #If 
                        a = int(self.label_table[instruction['symbol']], 16)
                    else :
                        a = 0
                    if instruction['symbol2'] in self.label_table.keys() :
                        b = int(self.label_table[instruction['symbol2']], 16)
                    else :
                        b = 0
                    cur_line = hex(a + b)

                self.label_table[instruction['label']] = cur_line[2:]

            elif 'operand' in instruction :
                cur_line = hex(int(instruction['operand']))
                self.label_table[instruction['label']] = cur_line[2:]

            elif 'delimiter' in instruction :
                self.label_table[instruction['label']] = cur_line[2:]
                cur_line = self.LOCCTR
            
            else :
                cur_line = '0x' + self.label_table[instruction['symbol']]
                self.label_table[instruction['label']] = cur_line[2:]
        
        else :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16))

        return cur_line

    def pass2(self, all_instruction) :

        instruction_list = []

        for i in range(len(all_instruction)) :

            val = all_instruction[i]

            #print('now:', val['instruction_info']['opcode'].upper().strip())
            if not val :
                continue
            
            elif val['instruction'].strip()[0] == '.' :
                val.setdefault('object_code', '')
                instruction_list.append(val)
                continue

            elif val['instruction_info']['opcode'].upper().strip() == 'START' :
                val.setdefault('object_code', '')
                instruction_list.append(val)
                continue

            if val['instruction_info']['opcode'].upper().strip() in opcode_table.keys() :

                if 'symbol' in val['instruction_info'].keys() :
                    
                    if val['instruction_info']['symbol'] in self.label_table.keys() and 'operand2' in val['instruction_info'].keys() : # LDA BUFFER,X
                        temp_code = opcode_table[val['instruction_info']['opcode'].upper().strip()][1] + hex(int(self.label_table[val['instruction_info']['symbol']], 16) + int('0x8000',16))[2:]
                        # opcode + (symbol address + 0x8000), because X = 1
                        val.setdefault('object_code', temp_code.upper())
                        instruction_list.append(val)
                    elif val['instruction_info']['symbol'] in self.label_table.keys() : # LDA BUFFER
                        temp_code = opcode_table[val['instruction_info']['opcode'].upper().strip()][1] + self.label_table[val['instruction_info']['symbol']]
                        # opcode + symbol address
                        val.setdefault('object_code', temp_code.upper())
                        instruction_list.append(val)

                    else : #External reference or undefined symbol
                        temp_code = opcode_table[val['instruction_info']['opcode'].upper().strip()][1] + '0000'
                        val.setdefault('object_code', temp_code.upper())
                        instruction_list.append(val)

                elif 'literal' in val['instruction_info'].keys() : #LDA =5
                    temp_code = opcode_table[val['instruction_info']['opcode'].upper().strip()][1] + insert_zero(self.literal_address.pop(0), 4)
                    val.setdefault('object_code', temp_code.upper())
                    instruction_list.append(val)

                else : #Fix
                    temp_code = opcode_table[val['instruction_info']['opcode'].upper().strip()][1] + '0000'
                    val.setdefault('object_code', temp_code.upper())
                    instruction_list.append(val)
            
            elif val['instruction_info']['opcode'].upper().strip() == 'BYTE' :

                if 'string' in val['instruction_info'].keys() : #C'EOF'
                    temp_str = val['instruction_info']['string'].encode('utf-8')
                    val.setdefault('object_code', temp_str.hex().upper())
                    instruction_list.append(val)

                else : #X'F1'
                    val.setdefault('object_code', val['instruction_info']['hex'])
                    instruction_list.append(val)

            elif val['instruction_info']['opcode'].upper().strip() == 'WORD' :
                val.setdefault('object_code', insert_zero(hex(int(val['instruction_info']['operand']))[2:], 6))
                instruction_list.append(val)

            elif val['instruction_info']['opcode'] == 'LTORG' or val['instruction_info']['opcode'] == 'END':

                if len(self.literal_list) > 0 :
                    val.setdefault('object_code', '')
                    instruction_list.append(val)
                    
                    literal = self.literal_list.pop(0)
                    loc = hex(int(all_instruction[i-1]['location'][2:], 16) + int('0x3', 16))

                    for literal_key, literal_value in literal.items() :
                        
                        if literal_key[1] == 'C' :
                            temp = {'location' : loc,'instruction' : '*\t'+literal_key, 'object_code' : insert_zero(literal_value.encode('utf-8').hex(), 6)}
                            loc = hex(int(loc, 16) + int('0x3', 16))
                        elif literal_key[1] == 'X' :
                            temp = {'location' : loc,'instruction' : '*\t'+literal_key, 'object_code' : insert_zero(literal_value.upper(), 6)}
                            loc = hex(int(loc, 16) + int('0x1', 16))
                        else :
                            temp = {'location' : loc,'instruction' : '*\t'+literal_key, 'object_code' : insert_zero(literal_value.upper(), 6)}
                            loc = hex(int(loc, 16) + int('0x3', 16))

                        instruction_list.append(temp)
                        loc = hex(int(loc, 16) + int('0x3', 16))
                
                else :
                    val.setdefault('object_code', '')
                    instruction_list.append(val)

            else :
                val.setdefault('object_code', '')
                instruction_list.append(val)

        output = open('Output.txt', 'w')
        count = 5
        output.write('Line\tLoc\tSource\tstatement\tObject code\n\n')
        for val in instruction_list :
            output.write(str(count) + '\t') 
            if val['location'] != None :
                output.write(val['location'][2:].upper())
            output.write('\t' + val['instruction'] + '\t' + val['object_code'] + '\n')
            count = count + 5
        output.close()

        return instruction_list

class SICXE_syntax_analysis :

    def syntax(self, token, kind, c_or_x) :

        opcode = 1
        persudo = 2
        label = 5
        seperate = [4, 1]
        str = [4,9]
        reg = 3
        operand = [5]
        integer = 6
        def_label = [6, 7]

        if len(token) == 0 and len(kind) == 0 : #prevent empty list
            return
        elif token[0].strip() == '.' :
            return
        elif token[0].upper().strip() == 'BASE' :
            return_line = {'opcode' : token[0], 'symbol' : token[1]}
            return return_line
        elif token[0].upper().strip() == 'LTORG' :
            return_line = {'opcode' : token[0]}
            return return_line

        if token[-1] == '.' :
            token.pop()
#==============================================================================================================================
        if kind[0][0] == label : #When the first token is label

            if kind[1][0] == persudo : # e.g THREE WORD 3, one label, one persudo, one integer or string

                if kind[2] == str and kind[4] == str : # EOF BYTE C'EOF', one label, one persudo, ' interger or string '
                    if kind[3][0] in def_label :
                        if c_or_x == 1 :
                            return_line = {'label' : token[0], 'opcode' : token[1], 'string' : token[3] }
                            return return_line
                        else :
                            return_line = {'label' : token[0], 'opcode' : token[1], 'hex' : token[3] }
                            return return_line
                    else :
                        print('syntax error')
                else :
                    
                    if len(token) == 5: 
                        if token[1].upper().strip() == 'EQU' and kind[2][0] == label and kind[4][0] == label : #MAXLEN EQU BUFEND-BUFFER
                            return_line = {'label' : token[0], 'opcode' : token[1],'symbol' : token[2], 'operator' : token[3], 'symbol2' : token[4] }
                            return return_line
                        else :
                            print('syntax error')

                    if kind[2][0] in def_label : # INPUT BYTE 1 or BUFFER EQU 3
                        return_line = {'label' : token[0], 'opcode' : token[1], 'operand' : token[2] }
                        return return_line

                    elif len(token) == 3 and kind[2][0] == 4 and token[1].upper().strip() != 'WORD' : # LENGTH EQU *
                        return_line = {'label' : token[0], 'opcode' : token[1], 'delimiter' : token[2] }
                        return return_line

                    elif len(token) == 3 and kind[2][0] == label and token[1].upper().strip() != 'WORD' : #LENGTH EQU BUFFER
                        return_line = {'label' : token[0], 'opcode' : token[1], 'symbol' : token[2] }
                        return return_line

                    else :
                        print("syntax error") #the thing to define label must be in the table 6 or 7

            elif kind[1][0] == opcode : #When opcode is the second
                
                if token[1].upper().strip() in one_operand.keys() : # one operand kind
                    
                    if len(token) == 3 : # ex. ENDFIL LDA LENGTH, three token, one label, one opcode, one operand
                        if kind[2][0] in operand :
                            return_line = {'label' : token[0], 'opcode' : token[1], 'symbol' : token[2], 'format' : 3 }
                            return return_line

                        elif kind[2][0] == reg : # ENDFIL CLEAR b
                            return_line = {'label' : token[0], 'opcode' : token[1], 'operand' : token[2], 'format' : 2 }
                            return return_line

                        elif kind[2][0] == integer : # ENDFIL comp 0
                            return_line = {'label' : token[0], 'opcode' : token[1], 'address' : token[2], 'format' : 3 }
                            return return_line

                        else :
                            print("syntax error")

                    elif len(token) == 4 : # ENDFIL LDA #5 or ENDFIL LDA =3277 or ENDFIL j @CLOOP or ENDFIL LDA #LENGTH

                        if token[2].strip() == '#' and kind[3][0] == 6 : #Immediate value
                            return_line = {'label' : token[0], 'opcode' : token[1], 'immediate' : token[3], 'format' : 3}
                            return return_line

                        elif token[2].strip() == '=' and kind[3][0] == 6 : #Literal
                            return_line = {'label' : token[0], 'opcode' : token[1], 'literal' : token[3], 'format' : 3}
                            return return_line

                        elif token[2].strip() == '@' and kind[3][0] == 5 : #Indirect addressing
                            return_line = {'label' : token[0], 'opcode' : token[1], 'indirect' : '@', 'literal' : token[3], 'format' : 3 }
                            return return_line

                        elif token[2].strip() == '#' and kind[3][0] == 5 : #direct addressing
                            return_line = {'label' : token[0],'opcode' : token[1], 'immediate' : '#', 'symbol' : token[3], 'format' : 3}
                            return return_line

                        else :
                            print("syntax error")

                    elif len(token) == 5 : # e.g ENDFIL STCH BUFFER,X
                    
                        if kind[2][0] == label and kind[3] == seperate and token[4].upper().strip() == 'X':
                            return_line = {'label' : token[0], 'opcode' : token[1], 'symbol' : token[2], 'index' : token[4], 'format' : 3 }
                            return return_line
                        else :
                            print('syntax error')

                    elif len(token) == 6 : # e.g ENDFIL LDA =C'EOF' or ENDFIL LDA =X'F1'
                        
                        if kind[3] == str and kind[5] == str and token[2].upper().strip() == '=' :
                            if c_or_x == 1 :
                                return_line = {'label' : token[0], 'string' : 'C', 'opcode' : token[1], 'literal' : token[4], 'format' : 3}
                                return return_line
                            else :
                                return_line = {'label' : token[0], 'hex' : 'X', 'opcode' : token[1], 'literal' : token[4], 'format' : 3}
                                return return_line

                    else :
                        print("syntax error")
                
                else :
                    print("syntax error")

            elif len(token) > 1 and token[1].upper().strip() == '+' : # Format 4

                if token[2].upper().strip() in one_operand.keys() : #CLOOP +JSUB RDREC

                    if len(token) == 4 : # ex. CLOOP +JSUB RDREC, three token, one label, one opcode, one operand
                        if kind[3][0] in operand :
                            return_line = {'label' : token[0], 'opcode' : token[2], 'symbol' : token[3], 'format' : 4 }
                            return return_line

                        elif kind[3][0] == reg : # ENDFIL +CLEAR b
                            return_line = {'label' : token[0], 'opcode' : token[2], 'operand' : token[3], 'format' : 4 }
                            return return_line

                        elif kind[3][0] == integer : # ENDFIL +comp 0
                            return_line = {'label' : token[0], 'opcode' : token[2], 'address' : token[3], 'format' : 4 }
                            return return_line

                        else :
                            print("syntax error")
                    
                    elif len(token) == 5 : # ENDFIL +LDA #5 or ENDFIL +LDA =3277 or ENDFIL +J @CLOOP or ENDFIL +LDA #LENGTH

                        if token[3].strip() == '#' and kind[4][0] == 6 : #Immediate value
                            return_line = {'label' : token[0], 'opcode' : token[2], 'immediate' : token[4], 'format' : 4 }
                            return return_line

                        elif token[3].strip() == '=' and kind[4][0] == 6 : #Literal
                            return_line = {'label' : token[0], 'opcode' : token[2], 'literal' : token[4], 'format' : 4 }
                            return return_line

                        elif token[3].strip() == '@' and kind[4][0] == 5 : #Indirect addressing
                            return_line = {'label' : token[0], 'opcode' : token[2], 'indirect' : '@', 'literal' : token[4], 'format' : 4 }
                            return return_line

                        elif token[3].strip() == '#' and kind[4][0] == 5 : #direct addressing
                            return_line = {'label' : token[0],'opcode' : token[2], 'immediate' : '#', 'symbol' : token[4], 'format' : 4}
                            return return_line

                        else :
                            print("syntax error")

                    elif len(token) == 6 : # e.g ENDFIL +STCH BUFFER,X
                    
                        if kind[3][0] == label and kind[4] == seperate and token[5].upper().strip() == 'X':
                            return_line = {'label' : token[0], 'opcode' : token[2], 'symbol' : token[3], 'index' : token[5], 'format' : 4 }
                            return return_line
                        else :
                            print('syntax error')

                    elif len(token) == 7 : # e.g ENDFIL +LDA =C'EOF' or ENDFIL +LDA =X'F1'
                        
                        if kind[4] == str and kind[6] == str and token[3].upper().strip() == '=' :
                            if c_or_x == 1 :
                                return_line = {'opcode' : token[2], 'string' : 'C', 'literal' : token[5], 'format' : 4}
                                return return_line
                            else :
                                return_line = {'opcode' : token[2], 'hex' : 'X', 'literal' : token[5], 'format' : 4}
                                return return_line

                    else :
                        print("syntax error")
                
                else :
                    print("syntax error")

            else :
                print("syntax error")
#==============================================================================================================================                
        elif kind[0][0] == opcode : # if the first token is opcode

            if token[0].upper().strip() in no_operand.keys() : # no operand kind
                
                if token[0].upper().strip() == 'RSUB' and len(token) == 1:
                    return_line = {'opcode' : token[0], 'format' : 3}
                    return return_line

                elif len(token) == 1 and token[0].upper().strip() != 'RSUB' : # ex. TIO, one token, one opcode, no operand
                    return_line = {'opcode' : token[0], 'format' : 1}
                    return return_line
                else :
                    print("syntax error")

            elif token[0].upper().strip() in one_operand.keys() : # one operand kind

                if len(token) == 2 : # ex. LDA LENGTH, two token, one opcode, one operand
                    if kind[1][0] in operand and token[0].upper().strip() != 'CLEAR' :
                        return_line = {'opcode' : token[0], 'symbol' : token[1], 'format' : 3 }
                        return return_line

                    elif kind[1][0] == reg :
                        return_line = {'opcode' : token[0], 'operand' : token[1], 'format' : 2 }
                        return return_line

                    elif kind[1][0] == integer and token[0].upper().strip() != 'CLEAR' : # comp 0
                        return_line = {'opcode' : token[0], 'address' : token[1], 'format' : 3 }
                        return return_line

                    else :
                        print("syntax errorrrrrrrr")

                elif len(token) == 3 : # LDA #5 or LDA =3277 or J @RETADR or LDB #LENGTH

                    if token[1].strip() == '#' and kind[2][0] == 6 : #Immediate value
                        return_line = {'opcode' : token[0], 'immediate' : token[2], 'format' : 3}
                        return return_line

                    elif token[1].strip() == '=' and kind[2][0] == 6 : #Literal
                        return_line = {'opcode' : token[0], 'literal' : token[2], 'format' : 3}
                        return return_line

                    elif token[1].strip() == '@' and kind[2][0] == 5 : #Indirect addressing
                        return_line = {'opcode' : token[0], 'indirect' : '@', 'symbol' : token[2], 'format' : 3}
                        return return_line

                    elif token[1].strip() == '#' and kind[2][0] == 5 : #direct addressing
                        return_line = {'opcode' : token[0], 'immediate' : '#', 'symbol' : token[2], 'format' : 3}
                        return return_line

                    else :
                        print("syntax error")

                elif len(token) == 4 : # e.g STCH BUFFER,X, four token, one opcode, one buffer, one seperate, one index address
                    
                    if kind[1][0] == label and kind[2] == seperate and token[3].upper().strip() == 'X':
                        return_line = {'opcode' : token[0], 'symbol' : token[1], 'index' : token[3], 'format' : 3 }
                        return return_line
                    else :
                        print('syntax error')

                elif len(token) == 5 : # e.g LDA =C'EOF' or LDA =X'F1'

                    if kind[2] == str and kind[4] == str and token[1].upper().strip() == '=' :
                        if c_or_x == 1 :
                            return_line = {'opcode' : token[0], 'string' : 'C', 'literal' : token[3], 'format' : 3}
                            return return_line
                        else :
                            return_line = {'opcode' : token[0], 'hex' : 'X', 'literal' : token[3], 'format' : 3}
                            return return_line
                    else :
                        print("syntax error")

                else :
                    print("syntax error")

            elif token[0].upper().strip() in two_operand_reg.keys() : # two reg

                if len(token) == 4 : # ex. ADDR r1, r2, two token, one opcode, two operand

                    if kind[2] == seperate : #There must have ',' between the two operand
                        if kind[1][0] == reg and kind[3][0] == reg : 
                            return_line = {'opcode' : token[0], 'operand' : token[1], 'operand2' : token[3], 'format' : 2 }
                            return return_line
                        else :
                            print("syntax error")
                    else :
                        print("syntax error")
                else :
                    print("syntax error")

            elif token[0].upper().strip() in two_operand_n.keys() : # one reg, one integer

                if len(token) == 4 : # ex. SHIFTL r1, n, two token, one opcode, one operand, one int

                    if kind[2] == seperate : #There must have ',' between the two operand
                        if kind[1][0] == reg and kind[3][0] == 6 : #The second operand must be int 
                            return_line = {'opcode' : token[0], 'operand' : token[1], 'immediate' : token[3], 'format' : 2 }
                            return return_line
                        else :
                            print("syntax error")
                    else :
                        print("syntax error")
                else :
                    print("syntax error")
            
            else :
                print("syntax error")
#==============================================================================================================================
        elif token[0].upper().strip() == '+' :

            if kind[1][0] == opcode : # if the second token is opcode

                if token[1].upper().strip() in no_operand.keys() : # no operand kind
                    
                    if len(token) == 2 : # ex. +RSUB, one token, one opcode, no operand
                        return_line = {'opcode' : token[1], 'format' : 4}
                        return return_line
                    else :
                        print("syntax error")

                elif token[1].upper().strip() in one_operand.keys() : # one operand kind

                    if len(token) == 3 : # ex. +LDA LENGTH, two token, one opcode, one operand
                        if kind[2][0] in operand :
                            return_line = {'opcode' : token[1], 'symbol' : token[2], 'format' : 4 }
                            return return_line

                        elif kind[2][0] == reg : # +CLEAR b
                            return_line = {'opcode' : token[1], 'operand' : token[2], 'format' : 4 }
                            return return_line

                        elif kind[2][0] == integer : # +comp 0
                            return_line = {'opcode' : token[1], 'address' : token[2], 'format' : 4 }
                            return return_line

                        else :
                            print("syntax error")

                    elif len(token) == 4 : # +LDA #5 or +LDA =3277 or +J @RETADR or +LDB #LENGTH

                        if token[2].strip() == '#' and kind[3][0] == 6 : #Immediate value
                            return_line = {'opcode' : token[1], 'immediate' : token[3], 'format' : 4}
                            return return_line

                        elif token[2].strip() == '=' and kind[3][0] == 6 : #Literal
                            return_line = {'opcode' : token[1], 'literal' : token[3], 'format' : 4}
                            return return_line

                        elif token[2].strip() == '@' and kind[3][0] == 5 : #Indirect addressing
                            return_line = {'opcode' : token[1], 'indirect' : '@', 'symbol' : token[3], 'format' : 4}
                            return return_line

                        elif token[2].strip() == '#' and kind[3][0] == 5 : #direct addressing
                            return_line = {'opcode' : token[1], 'immediate' : '#', 'symbol' : token[3], 'format' : 4}
                            return return_line
                        
                        else :
                            print("syntax error")

                    elif len(token) == 5 : # e.g +STCH BUFFER,X, four token, one opcode, one buffer, one seperate, one index address
                        
                        if kind[2][0] == label and kind[3] == seperate and token[4].upper().strip() == 'X':
                            return_line = {'opcode' : token[1], 'symbol' : token[2], 'index' : token[4], 'format' : 4 }
                            return return_line
                        else :
                            print('syntax error')

                    elif len(token) == 6 : # e.g +LDA =C'EOF' or +LDA =X'F1'

                        if kind[3] == str and kind[5] == str and token[2].upper().strip() == '=' :
                            if c_or_x == 1 :
                                return_line = {'opcode' : token[1], 'string' : 'C', 'literal' : token[4], 'format' : 4}
                                return return_line
                            else :
                                return_line = {'opcode' : token[1], 'hex' : 'X', 'literal' : token[4], 'format' : 4}
                                return return_line

                    else :
                        print("syntax error")
                
                else :
                    print("syntax error")
#==============================================================================================================================
        elif token[0].upper().strip() == 'END' :
            
            if kind[1][0] == label : # e.g END FIRST
                return_line = {'opcode' : token[0], 'symbol' : token[1]}
                return return_line
            else :
                print("syntax error")
#==============================================================================================================================
        elif kind[0][0] == persudo : # e.g WORD 3, one persudo, one integer or string

            if kind[1] == str and kind[3] == str : # BYTE C'EOF', one persudo, ' interger or string '
                if kind[2][0] in def_label :
                    if c_or_x == 1 :
                        return_line = { 'opcode' : token[0], 'string' : token[2] }
                        return return_line
                    else :
                        return_line = { 'opcode' : token[0], 'hex' : token[2] }
                        return return_line
                else :
                    print('syntax error')
            else :

                if kind[1][0] in def_label and token[0].upper() != 'EQU' : # BYTE 1
                    return_line = {'opcode' : token[0], 'operand' : token[1] }
                    return return_line

                else :
                    print("syntax error") #the thing to define label must be in the table 6 or 7
#==============================================================================================================================
        else :
            print("syntax error")

class SICXE_object_code :

    label_table = dict()
    base = '0000'
    literal = dict()
    literal_list = []
    literal_table = []
    literal_address = []
    starting_address = hex(0)
    LOCCTR = hex(0)

    def pass1(self, instruction, cur_line, last_line) : # cur_line will be 0xabc format

        if not instruction :
            return

        if instruction['opcode'] == 'START' : # initial the first line
            self.starting_address = hex(int(instruction['operand'], 16))
            self.LOCCTR = self.starting_address
            return self.LOCCTR

        elif instruction['opcode'] == 'BASE' :
            self.base = instruction['symbol']
            self.LOCCTR = cur_line
            return
        #=========================================================================================================
        if 'label' in instruction.keys() : # First token is label

            if instruction['label'] == self.base : # put label address in base
                self.base = cur_line[2:]

            if instruction['label'] in self.label_table.keys() :
                print('Duplicate label') #Found same label
            else :
                self.label_table.setdefault(instruction['label'], cur_line[2:])#Insert new label in label table

        if 'literal' in instruction.keys() : # There is a literal in instruction
            self.literal_table.append(cur_line) #Insert new label in label table

            if 'string' in instruction.keys() :
                self.literal.setdefault('=C\''+instruction['literal']+'\'', instruction['literal'])
            elif 'hex' in instruction.keys() :
                self.literal.setdefault('=X\''+instruction['literal']+'\'', instruction['literal']) 
            else :
                self.literal.setdefault(instruction['literal'], instruction['literal'])

        if instruction['opcode'].upper().strip() == 'LTORG' or instruction['opcode'].upper().strip() == 'END' :
            for value in self.literal_table :
                self.literal_address.append(hex(int(last_line, 16) - int(value, 16))[2:])
            self.literal_table.clear()

            temp_dict = self.literal.copy()
            self.literal_list.append(temp_dict)
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16)*len(temp_dict))
            self.literal.clear()
            return
        #=========================================================================================================
        if instruction['opcode'].upper().strip() == 'BYTE' :  # Caculate the length of BYTE, two cases: C and X

            if 'string' in instruction.keys() : # e.g EOF BYTE C'EOF', length is 3
                self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16))
            else : # e.g INPUT BYTE X'F1', length is 1
                self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x1', 16))

        elif instruction['opcode'].upper().strip() == 'RESW' : # Caculate the length of RESW
            self.LOCCTR = hex(int(cur_line[2:], 16) + int(hex(int(instruction['operand'])), 16)*3)

        elif instruction['opcode'].upper().strip() == 'RESB' :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int(hex(int(instruction['operand'])), 16))

        elif 'format' in instruction.keys() and instruction['format'] == 1 :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int(hex(opcode_table[instruction['opcode'].upper().strip()][0]), 16))

        elif 'format' in instruction.keys() and instruction['format'] == 2 :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x2', 16))

        elif 'format' in instruction.keys() and instruction['format'] == 3 :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16))

        elif 'format' in instruction.keys() and instruction['format'] == 4 :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x4', 16))

        elif instruction['opcode'].upper().strip() == 'EQU' :
            if 'operator' in instruction.keys() :

                if instruction['operator'] == '-' :
                    if instruction['symbol'] in self.label_table.keys() : #If 
                        a = int(self.label_table[instruction['symbol']], 16)
                    else :
                        a = 0
                    if instruction['symbol2'] in self.label_table.keys() :
                        b = int(self.label_table[instruction['symbol2']], 16)
                    else :
                        b = 0
                    cur_line = hex(a - b)
                    cur_line = hex(int(cur_line, 16)&0xffff)

                elif instruction['operator'] == '+' :
                    if instruction['symbol'] in self.label_table.keys() : #If 
                        a = int(self.label_table[instruction['symbol']], 16)
                    else :
                        a = 0
                    if instruction['symbol2'] in self.label_table.keys() :
                        b = int(self.label_table[instruction['symbol2']], 16)
                    else :
                        b = 0
                    cur_line = hex(a + b)

                self.label_table[instruction['label']] = cur_line[2:]

            elif 'operand' in instruction :
                cur_line = hex(int(instruction['operand']))
                self.label_table[instruction['label']] = cur_line[2:]

            elif 'delimiter' in instruction :
                self.label_table[instruction['label']] = cur_line[2:]
                cur_line = self.LOCCTR
            
            else :
                cur_line = '0x' + self.label_table[instruction['symbol']]
                self.label_table[instruction['label']] = cur_line[2:]

        else :
            self.LOCCTR = hex(int(cur_line[2:], 16) + int('0x3', 16))

        return cur_line

    def pass2(self, all_instruction) :

        reg_table = {'B' : '3', 'S' : '4', 'T' : '5', 'F' : '6', 'A' : '0', 'X' : '1', 'L' : '2'}
        instruction_list = []

        for i in range(len(all_instruction)) :

            temp_val = all_instruction[i]
            val = temp_val['instruction_info']

            if not temp_val :
                continue

            elif temp_val['instruction'].strip()[0] == '.' :
                temp_val.setdefault('object_code', '')
                instruction_list.append(temp_val)
                continue

            elif not val :
                continue

            elif val['opcode'].upper().strip() == 'START' :
                temp_val.setdefault('object_code', '')
                instruction_list.append(temp_val)
                continue

            if i < len(all_instruction) - 1 :
                if all_instruction[i+1]['location'] != None :
                    program_counter = all_instruction[i+1]['location'][2:]
                elif  i < len(all_instruction) - 2 and all_instruction[i+2]['location'] != None :
                    program_counter = all_instruction[i+2]['location'][2:]

            if 'format' in val.keys() and val['format'] == 2 : # format 2

                op = opcode_table[val['opcode'].upper().strip()][1]

                if 'operand' in val.keys() and 'operand2' in val.keys() : # addr r1, r2
                    r1 = reg_table[val['operand'].upper()]
                    r2 = reg_table[val['operand2'].upper()]

                elif 'operand' in val.keys() : # clear b
                    r1 = reg_table[val['operand'].upper()]
                    r2 = '0'

                temp_val.setdefault('object_code', op+r1+r2)
                instruction_list.append(temp_val)

            elif 'format' in val.keys() and val['format'] == 4 :

                op = bin(int(opcode_table[val['opcode'].upper().strip()][1], 16))[2:-2]

                if 'immediate' in val.keys() : # +LDA #3277 or +LDB #LENGTH
                    nixbpe = '010001'
                elif 'indirect' in val.keys() : # +j @RETADR
                    nixbpe = '100001'
                elif 'index' in val.keys() : # +STCH BUFFER,X
                    nixbpe = '111001'
                elif 'literal' in val.keys() : # +LDA =3277
                    nixbpe = '110010' 
                    temp_object = hex(int(op+nixbpe, 2))[2:]
                    temp_object = insert_zero(temp_object, 3) + insert_zero(hex(int(self.literal_address.pop(0), 16)), 3)
                else : # +LDA BUFFER 
                    nixbpe = '110001'
                
                temp_object = hex(int(op+nixbpe, 2))[2:]
                if 'symbol' in val.keys() and 'immediate' in val.keys() : # +LDB #LENGTH
                    try :
                        temp_object = insert_zero(temp_object, 3) + insert_zero(self.label_table[val['symbol']], 5)
                    except :
                        print('Undefined symbol h')

                elif  'symbol' in val.keys() : # +j @RETADR or +LDA BUFFER or +STCH BUFFER,X
                    try :
                        temp_object = insert_zero(temp_object, 3) + insert_zero(self.label_table[val['symbol']], 5)
                    except :
                        print('Undefined symbol g')

                elif 'immediate' in val.keys() : # +LDA #4096
                    temp_object = insert_zero(temp_object, 3) + insert_zero(hex(int(val['immediate']))[2:], 5)
                else : # +comp 0 or RSUB
                    temp_object = insert_zero(temp_object, 3) + '00000'

                temp_val.setdefault('object_code', temp_object)
                instruction_list.append(temp_val)

            elif 'format' in val.keys() and val['format'] == 3 : # format 3

                op = bin(int(opcode_table[val['opcode'].upper().strip()][1], 16))[2:-2]

                if val['opcode'].upper() == 'RSUB' :

                    nixbpe = '110000'
                    temp_object = hex(int(op+nixbpe, 2))[2:] + '000'
                    temp_val.setdefault('object_code', temp_object)
                    instruction_list.append(temp_val)

                elif 'index' in val.keys() : #STCH BUFFER,X 

                    try :
                        temp_location = self.label_table[val['symbol']]
                    except :
                        print('Undefined symbol f')

                    temp_location = hex(int(temp_location, 16) - int(program_counter, 16))

                    if int(temp_location, 16) < 2047 and int(temp_location, 16) > -2048 : # with pc, Disp can show the number
                        nixbpe = '111010'
                        temp_object = hex(int(op+nixbpe, 2))[2:]

                        temp_location = hex2(int(temp_location, 16)) #If the original temp_location is -0x12(for example)
                        temp_object = insert_zero(temp_object, 3) + insert_zero(temp_location[2:], 3)
                    
                    else : # Disp can't show the number, have to use the BASE to caculate
                        nixbpe = '111100'
                        temp_object = hex(int(op+nixbpe, 2))[2:]
                        try :
                            temp_location = hex(int(self.label_table[val['symbol']], 16) - int(self.base, 16)) # Use BASE
                        except :
                            print('Undefined symbol e')

                        temp_location = hex2(int(temp_location, 16)) #If the original temp_location is -0x12(for example)
                        temp_object = insert_zero(temp_object, 3) + insert_zero(temp_location[2:], 3)

                    temp_val.setdefault('object_code', temp_object)
                    instruction_list.append(temp_val)

                elif 'immediate' in val.keys() or 'indirect' in val.keys() :

                    if 'immediate' in val.keys() and not 'symbol' in val.keys() : # LDA #5
                        nixbpe = '010000'

                        temp_object = hex(int(op+nixbpe, 2))[2:]
                        temp_object = insert_zero(temp_object, 3) + insert_zero(hex(int(val['immediate']))[2:], 3)

                    else : # J @RETADR or LDB #LENGTH
                        
                        try :
                            temp_location = self.label_table[val['symbol']]
                        except :
                            print('Undefined symbol d')

                        temp_location = hex(int(temp_location, 16) - int(program_counter, 16))

                        if int(temp_location, 16) < 2047 and int(temp_location, 16) > -2048 : # with pc, Disp can show the number

                            if 'indirect' in val.keys() :
                                nixbpe = '100010'
                            else :
                                nixbpe = '010010'

                            
                            temp_object = hex(int(op+nixbpe, 2))[2:]

                            temp_location = hex2(int(temp_location, 16)) #If the original temp_location is -0x12(for example)
                            temp_object = insert_zero(temp_object, 3) + insert_zero(temp_location[2:], 3)

                        else :

                            if 'indirect' in val.keys() :
                                nixbpe = '100100'
                            else :
                                nixbpe = '010100'  

                            temp_object = hex(int(op+nixbpe, 2))[2:]
                            try :
                                temp_location = hex(int(self.label_table[val['symbol']], 16) - int(self.base, 16)) # Use BASE
                            except :
                                print('Undefined symbol c')
                            
                            temp_location = hex2(int(temp_location, 16)) #If the original temp_location is -0x12(for example)
                            temp_object = insert_zero(temp_object, 3) + insert_zero(temp_location[2:], 3)

                    temp_val.setdefault('object_code', temp_object)
                    instruction_list.append(temp_val)

                elif 'literal' in val.keys() : # literal

                    nixbpe = '110010' 
                    temp_object = hex(int(op+nixbpe, 2))[2:]
                    temp_object = insert_zero(temp_object, 3) + insert_zero(hex(int(self.literal_address.pop(0), 16))[2:], 3)

                    temp_val.setdefault('object_code', temp_object)
                    instruction_list.append(temp_val)

                elif 'address' in val.keys() : # comp 0 or ENDFIL comp 0 

                    nixbpe = '110000' 
                    temp_object = hex(int(op+nixbpe, 2))[2:]
                    temp_object = insert_zero(temp_object, 3) + '000'

                    temp_val.setdefault('object_code', temp_object)
                    instruction_list.append(temp_val)

                else : # LDA LENGTH

                    try :
                        temp_location = self.label_table[val['symbol']]
                    except :
                        print('Undefined symbol b')

                    temp_location = hex(int(temp_location, 16) - int(program_counter, 16))

                    if int(temp_location, 16) < 2047 and int(temp_location, 16) > -2048 : # with pc, Disp can show the number
                        nixbpe = '110010'
                        temp_object = hex(int(op+nixbpe, 2))[2:]
                        temp_location = hex2(int(temp_location, 16)) #If the original temp_location is -0x12(for example)
                        temp_object = insert_zero(temp_object, 3) + insert_zero(temp_location[2:], 3)
                    
                    else : # Disp can't show the number, have to use the BASE to caculate
                        
                        nixbpe = '110100'
                        temp_object = hex(int(op+nixbpe, 2))[2:]
                        try :
                            temp_location = hex2(int(self.label_table[val['symbol']], 16) - int(self.base, 16)) # Use BASE
                        except :
                            print('Undefined symbol a')

                        temp_location = hex2(int(temp_location, 16)) #If the original temp_location is -0x12(for example)
                        temp_object = insert_zero(temp_object, 3) + insert_zero(temp_location[2:], 3)

                    temp_val.setdefault('object_code', temp_object)
                    instruction_list.append(temp_val)

            elif val['opcode'].upper().strip() == 'BYTE' :

                if 'string' in val.keys() : #C'EOF'
                    temp_str = val['string'].encode('utf-8')
                    temp_val.setdefault('object_code', temp_str.hex().upper())
                    instruction_list.append(temp_val)

                else : #X'F1'
                    temp_val.setdefault('object_code', val['hex'])
                    instruction_list.append(temp_val)

            elif val['opcode'].upper().strip() == 'WORD' :
                try :
                    temp_val.setdefault('object_code', insert_zero(hex(int(val['operand']))[2:], 6))
                except :
                    print('syntax errorrrrr')

                instruction_list.append(temp_val)

            elif 'format' in val.keys() and val['format'] == 1 : # format 1 

                op = opcode_table[val['opcode'].upper().strip()][1]

                temp_val.setdefault('object_code', op)
                instruction_list.append(temp_val)

            elif val['opcode'].upper().strip() == 'LTORG' or val['opcode'].upper().strip() == 'END':

                if len(self.literal_list) > 0 :
                    temp_val.setdefault('object_code', '')
                    instruction_list.append(temp_val)

                    literal = self.literal_list.pop(0)
                    loc = hex(int(all_instruction[i-1]['location'][2:], 16) + int('0x3', 16))

                    for literal_key, literal_value in literal.items() :
                        
                        if literal_key[1] == 'C' :
                            temp = {'location' : loc,'instruction' : '*\t'+literal_key, 'object_code' : insert_zero(literal_value.encode('utf-8').hex(), 6)}
                            loc = hex(int(loc, 16) + int('0x3', 16))
                        elif literal_key[1] == 'X' :
                            temp = {'location' : loc,'instruction' : '*\t'+literal_key, 'object_code' : insert_zero(literal_value.upper(), 6)}
                            loc = hex(int(loc, 16) + int('0x1', 16))
                        else :
                            temp = {'location' : loc,'instruction' : '*\t'+literal_key, 'object_code' : insert_zero(literal_value.upper(), 6)}
                            loc = hex(int(loc, 16) + int('0x3', 16))

                        instruction_list.append(temp)
                
                else :
                    temp_val.setdefault('object_code', '')
                    instruction_list.append(temp_val)

            else :
                temp_val.setdefault('object_code', '')
                instruction_list.append(temp_val)

        output = open('Output.txt', 'w')
        count = 5
        output.write('Line\tLocation\tSource\tcode\tObject code\n')
        output.write('----  -------- -------------------------                 -----------\n\n')
        for val in instruction_list :
            output.write(str(count) + '\t') 
            if val['location'] != None :
                output.write(insert_zero(val['location'][2:].upper(), 4))
            output.write('\t' + val['instruction'] + '\t' + val['object_code'].upper() + '\n')
            count = count + 5
        output.close()

        return instruction_list


test = lexical_analysis()
test.get_token()

for val in test.line_information :

    if not val :
        pass
    elif val['location'] == None :
        print(val['instruction'])
    else :
        print(insert_zero(val['location'][2:], 4) + '\t' + str(val['instruction']) + '\t' + str(val['object_code']))
