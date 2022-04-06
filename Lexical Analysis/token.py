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

class lexical_analysis:

    #Set three hash table
    t5 = ['']*100
    t6 = ['']*100
    t7 = ['']*100
    #Set three hash table

    #Set "token table" and "position table"
    token = list()
    position = list()
    #Set "token table" and "position table"

    def get_token(self):
        filename = input('Please input a file name : ')
        filename += '.txt'
        f = open(filename, 'r')
        output_file = open('output.txt', 'w')
        #strin = open('Table7.table', 'w')
        #digit = open('Table6.table', 'w')
        #message = open('Table5.table', 'w')


        delima = [',', '#', '@', '=', '?', ':', ';', '.', '*', '+', '-', '/']
        sperate = [' ', '\t', '\n']
        temp = ''
        
        #Catch every lines
        for str_line in f :

            str_flag = 0
            print(str_line)
            output_file.write(remove_enter(str_line)+'\n')
            site = []
            list = []

            #Get every char in the line
            for char in str_line :
                
                if char == '.' and str_flag == 0 : #comment
                    if temp != '' : #If there is something in the temp, append first
                        list.append(temp.strip())
                        site.append(self.find_table(temp.strip()))
                        temp = ''
                    list.append('.') 
                    site.append(self.find_table('.'))
                    break #everything behind the '.' is no need to get, so skip to the next line

                elif char == '\'' : #Meaning String
                    if temp != '' and str_flag == 1 : #Occur to the second ', append and find
                        list.append(temp.strip()) #C ==> String type
                        site.append(self.str_table(temp.strip())) #Special function for dealing String
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
                        if temp == 'C' : #Occur to the first ' , judge C or X
                            str_flag = 1
                        elif temp == 'X' :
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

            if temp != '' :
                list.append(temp.strip())
                site.append(self.find_table(temp.strip()))
                temp = ''

            for a in list : #Print token
                #print(a, end = '\t')
                self.token.append(a)

            for b in site : #Print position
                print('('+str(b[0])+','+str(b[1])+')', end = '\t')
                output_file.write('('+str(b[0])+','+str(b[1])+')')
                self.position.append(b)
            output_file.write('\n')
            print('\n')

        #Put every member in the list int the file
        '''for str5 in self.t5 :
            if str5 != '' :
                message.write(str5+'\n')
            else :
                message.write('\n')

        for str6 in self.t6 :
            if str6 != '' :
                digit.write(str6+'\n')
            else :
                digit.write('\n')
        
        for str7 in self.t7 :
            if str7 != '' :
                strin.write(str7+'\n')
            else :
                strin.write('\n')'''
        
        #Put every member in the list int the file

        f.close()
        output_file.close()
        #strin.close()
        #digit.close()
        #message.close()

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

test = lexical_analysis()
test.get_token()