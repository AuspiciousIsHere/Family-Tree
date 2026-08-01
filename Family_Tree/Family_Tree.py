import tkinter as tk
from plantuml import PlantUML
from PIL import ImageTk, Image
import csv
from csv import writer
import pandas as pd
server = PlantUML('http://www.plantuml.com/plantuml/img/')

with open("sequence.txt", "w") as f:
            f.write("""
            @startuml
       
            @enduml
            """)
class HashTable:
    # Creating a Hash table
    #time compexity: O(size)
    def __init__(self, size):
        self._size = size
        self._table = [None] * size

    # Define the index of the givek Key
    def _hash(self, key):
        # Return a Hash Key
        # O(1)
        return int(key) % self._size

    # Define a method to insert a key-value pair into the hash table
    # best and average case: O(1) || worst case: O(size)
    def insert(self, key, value):
        # Compute the index for the key using the hash function
        index = self._hash(key)
        # If the index is empty, store the key-value pair as a tuple
        if self._table[index] is None:
            self._table[index] = (key, value)
        # If the index is occupied, handle the collision
        else:
            # Loop through the array until an empty slot is found
            while self._table[index] is not None:
                # Increment the index by one! If it reached the end, then go back and find an empty one
                index = (index + 1) % self._size
                # If the array is full, raise an exception
                if index == self._hash(key):
                    raise Exception("Hash table is full")
            # Store the key-value pair as a tuple in the empty slot
            self._table[index] = (key, value)

    # Define a method to search by Key
    # best and average case: O(1) || worst case: O(size)
    def search(self, key):

        key = int(key)
        # Same as before we get the index using Key
        index = self._hash(key)
        # If the index is empty, return None
        if self._table[index] is None:
            return None
        # If the index is not None, check if the key matches
        elif self._table[index][0] == key:
            # Return the value of the key
            return self._table[index][1]
        # If the index is not None and the key does not match, handle the collision
        else:
            # Loop through the array until the key is found or an empty slot is reached
            while self._table[index] is not None and self._table[index][0] != key:
                # increase the index by one and go back if neccessary
                index = (index + 1) % self._size
                # If the array is full, return None
                if index == self._hash(key):
                    return None
            # If the key is found, return the value within
            if self._table[index] is not None and self._table[index][0] == key:
                return self._table[index][1]
            # If the key is not found, return None
            else:
                return None

    def Show_Everyone(self):
        # Best, average and worst case: O(size)
        occupides_list = []
        for temp in self._table:
            if temp != None:
                occupides_list.append(temp[1])
        return occupides_list

class Person:
    def __init__(self):
        self._Name = None
        self._SSN = None
        self._Sex = None
        self._Birth = None
        self._Death = "false"

    def Update_Person_Info(self, name, ssn, sex, birth, death):
        self.Name = name
        self.SSN = ssn
        self.Sex = sex
        self.Birth = birth
        self.Death = death


class Marriage_info:
    def __init__(self):
        self.PrevMarWife = None
        self.PrevMarHus = None
        self.Wife = None
        self.Hus = None
        self.DateOfMar = "not defined"
        self.DateOfMarEnd = "not defined"


class MainNode:
    def __init__(self):
        self.PI = Person()
        self.Dad = None
        self.Mom = None
        self.Latest_Mar = None
        self.Prev_Child_Of_Mom = None
        self.Prev_Child_Of_Dad = None
        self.Last_Child = None
        self.MI = Marriage_info()


class Family_Tree:
    HT = HashTable(100)
    # best, average and worst case: O(n) cuz we have to go trough all the childrens ... it all depends on number of childrens!
    def Show_Children(self, personssn):
        templist = []
        person = self.HT.search(personssn)
        if person != None and person.PI.Sex == 'male':
            LastChild = person.Last_Child
            while LastChild != None:
                  templist.append(LastChild)
                  LastChild = LastChild.Prev_Child_Of_Dad

        elif person != None and person.PI.Sex == 'female':
            LastChild = person.Last_Child
            while LastChild != None:
                  templist.append(LastChild)
                  LastChild = LastChild.Prev_Child_Of_Mom

        return templist

    def Add_Person(self, name, ssn, sex, birth, death):
        # best and average case: O(1) || worst case: O(size) bcuz of insert function of Hash table!
        temp = MainNode()
        temp.PI.Update_Person_Info(name, ssn, sex, birth, death)
        self.HT.insert(int(temp.PI.SSN), temp)
        with open("sequence.txt", "a") as f:
            f.writelines(["@startuml\n", "[" + temp.PI.Name + "]" , "\n@enduml"])

    def Define_Wife_And_Hus(self, mal, fem, date_of_marriage):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        female = self.HT.search(fem)
        male = self.HT.search(mal)
        if female != None and male != None:
            if female.PI.Sex == 'male' and male.PI.Sex == 'male':
                print('HARAM BROTHER! GO HALAL MODE!')
            elif female.PI.Sex == 'female' and male.PI.Sex == 'female':
                print('HARAM SISTER! GO HALAL MODE!')
            else:
                if male.MI.Wife == None and female.MI.Hus == None:
                    female.MI.DateOfMar = male.MI.DateOfMar = date_of_marriage
                    male.MI.Wife = female
                    female.MI.Hus = male
                    male.MI.LatestMar = female
                    female.MI.LatestMar = male
                    with open("sequence.txt", "a") as f:
                        f.writelines(["@startuml\n", "[" + male.PI.Name + "]" + ".." + "[" + female.PI.Name + "]", "\n@enduml"])
                else:
                    print('one or both of these people are already married! they cant marry untill they divorce!')
        else:
            print("no persons exist with the given SSNs!")

    def Divorce(self, mal, fem, date_of_mar_end):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        female = self.HT.search(fem)
        male = self.HT.search(mal)
        if female != None and male != None:
            if female.MI.Hus == male:
                female.MI.Hus = male.MI.Wife = None
                male.MI.PrevMarWife = female
                female.MI.PrevMarHus = male
                female.MI.DateOfMarEnd = male.MI.DateOfMarEnd = date_of_mar_end
                with open("sequence.txt", "r") as f:
                    UMLlist = f.readlines()
                    UMLlist.remove("[" + male.PI.Name + "]" + ".." + "[" + female.PI.Name + "]" + "\n")
                    f.close()
                with open("sequence.txt", "w") as p:
                    for line in UMLlist:
                        p.writelines(line)
            else:
                print('these people are not yet married!')
        else:
            print("no persons exist with the given SSNs!")

    def Dad_And_Mom(self, personSSN, dadSSN, momSSN):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        dad = self.HT.search(dadSSN)
        mom = self.HT.search(momSSN)
        person = self.HT.search(personSSN)
        if mom != None and dad != None and person != None:
            if dad == mom.MI.Hus and mom == dad.MI.Wife:
                person.Dad = dad
                person.Mom = mom
                person.Prev_Child_Of_Dad = person.Dad.Last_Child
                person.Prev_Child_Of_Mom = person.Mom.Last_Child
                person.Mom.Last_Child = person.Dad.Last_Child = person
                if person.Prev_Child_Of_Mom == person.Prev_Child_Of_Dad and person.Prev_Child_Of_Mom != None and person.Prev_Child_Of_Dad != None:
                    with open("sequence.txt", "a") as f:
                        f.writelines(["@startuml\n", "[" + person.Prev_Child_Of_Dad.PI.Name + "]" + "->" + "[" + person.PI.Name + "]", "\n@enduml"])
                with open("sequence.txt", "a") as f:
                    f.writelines(["@startuml\n", "[" + mom.PI.Name + "]" + "--" + "[" + person.PI.Name + "]", "\n@enduml"])
                    f.writelines(["@startuml\n", "[" + dad.PI.Name + "]" + "--" + "[" + person.PI.Name + "]", "\n@enduml"])
        else:
            print("no persons exist with the given SSNs!")

    def death(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        temp = self.HT.search(personssn)
        if temp != None:
            temp.PI.Death == "true"
            if temp.PI.Sex == 'male' and temp.MI.Wife != None:
                temp.MI.Wife.MI.Hus = None
            elif temp.PI.Sex == 'female' and temp.MI.Hus != None:
                temp.MI.Hus.MI.Wife = None
        else:
            print("Person not found!")
    
    def Show_Brothers(self, personssn):
        # O(len(childrenlist1) * len(templist))
        templist = []
        flag = 1
        person = self.HT.search(personssn).Dad
        person1 = self.HT.search(personssn).Mom
        if person1 != None and person != None:
            childrenlist = self.Show_Children(person.PI.SSN)
            childrenlist1 = self.Show_Children(person1.PI.SSN)
            if childrenlist:
                for temp in childrenlist:
                    if temp.PI.SSN != personssn and temp.PI.Sex == 'male':
                        templist.append(temp)
            if childrenlist1:
                if templist:
                    for temp in childrenlist1:
                        if temp.PI.SSN != personssn and temp.PI.Sex == 'male':
                            flag = 1
                            for temp1 in templist:
                                if temp == temp1:
                                    flag = 0
                            if flag == 1:
                                templist.append(temp)
                    if not templist:
                        print('No brothers found!')
                else:
                    for temp in childrenlist1:
                        if temp.PI.SSN != personssn and temp.PI.Sex == 'male':
                            templist.append(temp)
            else:
                print("This guy is the only child!")
        return templist
        
    def Show_Sisters(self, personssn):
        # O(len(childrenlist1) * len(templist))
        templist = []
        flag = 1
        person = self.HT.search(personssn).Dad
        person1 = self.HT.search(personssn).Mom
        if person != None and person1 != None:
            childrenlist = self.Show_Children(person.PI.SSN)
            childrenlist1 = self.Show_Children(person1.PI.SSN)
            if childrenlist or childrenlist1:
                for temp in childrenlist:
                    if temp.PI.SSN != personssn and temp.PI.Sex == 'female':
                        templist.append(temp)
            if childrenlist1:
                if templist:
                    for temp in childrenlist1:
                        if temp.PI.SSN != personssn and temp.PI.Sex == 'female':
                            flag = 1
                            for temp1 in templist:
                                if temp == temp1:
                                    flag = 0
                            if flag == 1:
                                templist.append(temp)
                    if not templist:
                        print('No sisters found!')
                else:
                    for temp in childrenlist1:
                        if temp.PI.SSN != personssn and temp.PI.Sex == 'female':
                            templist.append(temp)
            else:
                print("This girl is the only child!")
        return templist

    def Show_Grandpa(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        oldlist = []
        person = self.HT.search(personssn).Dad
        person1 = self.HT.search(personssn).Mom
        if person != None and person1 != None:
            if person.Dad != None or person1.Dad != None:
                if person.Dad != None:
                    Grandpa = person.Dad
                    oldlist.append(Grandpa)
                if person1.Dad != None:
                    Grandpa = person1.Dad
                    oldlist.append(Grandpa)
            else:
                print('(Dad-side or Mom-side) GrandPa doesnt exist!')
        else:
            print("father or mother is not defined for this person yet!")
        return oldlist

    def Show_Grandma(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        oldlist = []
        person = self.HT.search(personssn).Dad
        person1 = self.HT.search(personssn).Mom
        if person != None and person1 != None:
            if person.Mom != None or person1.Mom != None:
                if person.Mom != None:
                    Grandma = person.Mom
                    oldlist.append(Grandma)
                if person1.Mom != None:
                    Grandma = person1.Mom
                    oldlist.append(Grandma)
            else:
                print('(Dad-side or Mom-side) Grandma doesnt exist!')
        else:
            print("Father or mother is not defined for this person yet!")
        return oldlist

    def Show_Khaleha(self, personssn):
        # # O(len(childrenlist1) * len(templist)) bcuz of using the Show_Sisters function!
        mom = self.HT.search(personssn).Mom
        if mom != None:
            sisterslist = self.Show_Sisters(mom.PI.SSN)
            return sisterslist
        else:
            print('Mother is not defined for this person yet!')
            return []

    def Show_Ammeha(self, personssn):
        # O(len(childrenlist1) * len(templist)) bcuz of using the Show_Sisters function!
        dad = self.HT.search(personssn).Dad
        if dad != None:
            sisterslist = self.Show_Sisters(dad.PI.SSN)
            return sisterslist
        else:
            print('Father is not defined for this person yet!')
            return []

    def Show_Amooha(self, personssn):
        # O(len(childrenlist1) * len(templist)) bcuz of using the Show_Brothers function!
        dad = self.HT.search(personssn).Dad
        if dad != None:
            brotherslist = self.Show_Brothers(dad.PI.SSN)
            return brotherslist
        else:
            print('Father is not defined for this person yet!')
            return []

    def Show_Daeeha(self, personssn):
        # O(len(childrenlist1) * len(templist)) bcuz of using the Show_Brothers function!
        mom = self.HT.search(personssn).Mom
        if mom != None:
            brotherslist = self.Show_Brothers(mom.PI.SSN)
            return brotherslist
        else:
            print('Mother is not defined for this person yet!')
            return []

    def Show_Children_Of_Amooha(self, personssn):
        # O(len(Amoohalist) * len(templist)) bcuz of 2 for loops inside each other
        temporary = []
        Amoohalist = self.Show_Amooha(personssn)
        if Amoohalist:
            for temp in Amoohalist:
                templist = self.Show_Children(temp.PI.SSN)
                for temp1 in templist:
                    temporary.append(temp1)
        return temporary

    def Show_Children_Of_Daeeha(self, personssn):
        # O(len(Dayeehalist) * len(templist)) bcuz of 2 for loops inside each other
        temporary = []
        Dayeehalist = self.Show_Daeeha(personssn)
        if Dayeehalist:
            for temp in Dayeehalist:
                templist = self.Show_Children(temp.PI.SSN)
                for temp1 in templist:
                    temporary.append(temp1)
        return temporary

    def Show_Children_Of_Khaleha(self, personssn):
        # O(len(Khalehalist) * len(templist)) bcuz of 2 for loops inside each other
        temporary = []
        Khalehalist = self.Show_Khaleha(personssn)
        if Khalehalist:
            for temp in Khalehalist:
                templist = self.Show_Children(temp.PI.SSN)
                for temp1 in templist:
                    temporary.append(temp1)
        return temporary

    def Show_Children_Of_Ammeha(self, personssn):
        # O(len(ammehalist) * len(templist)) bcuz of 2 for loops inside each other
        temporary = []
        ammehalist = self.Show_Ammeha(personssn)
        if ammehalist:
            for temp in ammehalist:
                templist = self.Show_Children(temp.PI.SSN)
                for temp1 in templist:
                    temporary.append(temp1)
        return temporary

    def Show_Mom(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        person = self.HT.search(personssn).Mom
        if person != None:
            return person
        else:
            print('No mom is defined for this person!')
            return None

    def Show_Dad(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        person = self.HT.search(personssn).Dad
        if person != None:
            return person
        print('No dad is defined for this person!')
        return None
    
    def Show_Wife(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        person = self.HT.search(personssn).MI.Wife
        if person != None:
            return person
        else:
            print("This person doesnt have a wife!")
            return None

    def Show_Husband(self, personssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        person = self.HT.search(personssn).MI.Hus
        if person != None:
            return person
        else:
            print("This person doesnt have a husband!")
            return None

    def Show_Naveh(self, personssn):
        # O(len(templist) * len(temporary)) bcuz of 2 for loops inside each other
        Naveh_List = []
        person = self.HT.search(personssn)
        if person != None:
            templist = self.Show_Children(personssn)
            if templist:
                for temp in templist:
                    temporary = self.Show_Children(temp.PI.SSN)
                    if temporary:
                        for temp1 in temporary:
                            Naveh_List.append(temp1)
        return Naveh_List


    def Initial_Define_Of_Last_Child(self, parentssn, childssn):
        # best and average case: O(1) || worst case: O(size) bcuz of search function of Hash table!
        parent = self.HT.search(parentssn)
        child = self.HT.search(childssn)
        if parent != None and child != None:
            parent.Last_Child = child



Test = Family_Tree()
#print('we have added a few persons to accelarate the proccess!')
#print('you can see everyones name and SSNs below so you know how to interact')
with open('Add.csv', mode = 'r') as file:
     csvFile = csv.reader(file)
     for lines in csvFile:
        Test.Add_Person(lines[0], lines[1], lines[2], lines[3], lines[4])
     file.close()
with open('Relations.csv', mode = 'r') as temp:
    csvFile = csv.reader(temp)
    for lines in csvFile:
        if lines[0] == '1':
            Test.Dad_And_Mom(str(lines[1]), str(lines[2]), str(lines[3]))
        if lines[0] == '2':
            Test.Define_Wife_And_Hus(str(lines[1]), str(lines[2]), str(lines[3]))
        if lines[0] == '3':
            Test.Divorce(str(lines[1]), str(lines[2]), str(lines[3]))
        if lines[0] == '4':
            Test.death(str(lines[1]))
        if lines[0] == '5':
            Test.Initial_Define_Of_Last_Child(str(lines[1]), str(lines[2]))
    file.close()
#Test.Add_Person('Hamid', '0890660727', 'male', '14/9/82', "false")
#Test.Add_Person('Nazi', '0989080899', 'female','15/2/83', "false")
#Test.Add_Person('Fatemeh', '1111111', 'female', '19/4/60', "false")
#Test.Add_Person('Mahdi', '2222222', 'male', '13/1/58', "false")
#Test.Add_Person('Vahid', '555555', 'male', '14/9/82', "false")
#Test.Define_Wife_And_Hus("2222222", '1111111', '14/4/59')
#Test.Dad_And_Mom('0890660727', '2222222', '1111111')
#Test.Dad_And_Mom('555555', '2222222', '1111111')
#Test.Define_Wife_And_Hus('0890660727', '0989080899', "15/9/1407")
#Test.Add_Person('Aida', '14567', 'female', '1/1/83', 'false')
#Test.Dad_And_Mom('14567', "2222222", '1111111')
#Test.Add_Person('homaayoon', '67892', 'female', '4/11/34', 'false')
#Test.Add_Person('zohreh', '98723', 'female', '15/6/24', 'false')
#Test.Add_Person('Asghar', '12345678', 'male', '10/8/33', 'false')
#Test.Add_Person('ghadir', '21345678', 'male', '10/8/33', 'false')
#Test.Add_Person('Najmeh', '578623', 'female', '14/5/78', 'false')
#Test.Define_Wife_And_Hus('21345678', '98723', '12/11/45')
#Test.Dad_And_Mom('578623', '21345678', '98723')
#Test.Dad_And_Mom('2222222', '21345678', '98723')
#Test.Define_Wife_And_Hus('12345678', '67892', '13/2/43')
#Test.Dad_And_Mom('1111111', '12345678', '67892')
#Test.Add_Person('Moslem', '678623678', 'male', '10/12/64', 'false')
#Test.Dad_And_Mom('678623678', '21345678', '98723')
#Test.Add_Person('Abolfazl', '7273437', 'male', '17/12/96', 'false')
#Test.Add_Person('Mojtaba', '7273438', 'male', '17/4/66', 'false')
#Test.Define_Wife_And_Hus('7273438','578623', '1/8/94')
#Test.Dad_And_Mom('7273437', '7273438', '578623')
# Create a root window

root = tk.Tk()
root.geometry('750x780')
root.resizable(False, False)
root['background'] = 'light blue'
root.title("Family Tree")
root.update()
# Create a label widget
label = tk.Label(root, text="select the SSN", bg = 'light yellow', width = 27)
items = []
# Create a variable to store the list
testlist = Test.HT.Show_Everyone()
for temp in testlist:
    items.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
var = tk.Variable(value = items)
listbox = tk.Listbox(root, listvariable=var, height=len(items), selectmode= 'EXTENDED', width = 32, bg = 'light yellow', borderwidth = 5)
listbox.pack()
button = tk.Button(root, text="press to show children!", width = 27)
# Define a function to handle the button click event
def click1():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing Children')
        templist = Test.Show_Children(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click2():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing Ammeha')
        templist = Test.Show_Ammeha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click3():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing Amooha')
        templist = Test.Show_Amooha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click4():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing Daeeha')
        templist = Test.Show_Daeeha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click5():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing Khaleha')
        templist = Test.Show_Khaleha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click6():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing children of someones Khaleha')
        templist = Test.Show_Children_Of_Khaleha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click7():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing children of Ammeha')
        templist = Test.Show_Children_Of_Ammeha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click8():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing children of Amooha')
        templist = Test.Show_Children_Of_Amooha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def click9():
    if var1.get() != 'None!':
        temp = []
        top = tk.Toplevel(root)
        top.title('Showing children of Daeeha')
        templist = Test.Show_Children_Of_Daeeha(var1.get())
        for temp1 in templist:
            temp.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        temp_var = tk.Variable(value = temp)
        tempbox = tk.Listbox(top, listvariable = temp_var, height = len(templist), selectmode = 'EXTENDED', width = 30, bg = 'light blue')
        tempbox.pack()
        buttemp = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp.pack()

def AddP_To_CSV(name, ssn, sex, birth, death):
    temp = [name, ssn, sex, birth, death]
    with open("Add.csv", 'a') as file1:
        writer_object = writer(file1)
        writer_object.writerow(temp)
        writer_object.writerow(temp)
        file1.close()
    df = pd.read_csv('Add.csv')
    df = df.iloc[:-1]
    df.to_csv('Add.csv', index=False)
def DAM_AddR_To_CSV(personssn, dadssn, momssn):
    temp = ['1', personssn, dadssn, momssn]
    with open("Relations.csv", 'a') as file2:
        writer_object = writer(file2)
        writer_object.writerow(temp)
        writer_object.writerow(temp)
        file2.close()
    df = pd.read_csv('Relations.csv')
    df = df.iloc[:-1]
    df.to_csv('Relations.csv', index=False)

def WAH_AddR_To_CSV(mal, fem, dom):
    temp = ['2', mal, fem, dom]
    with open("Relations.csv", 'a') as file3:
        writer_object = writer(file3)
        writer_object.writerow(temp)
        writer_object.writerow(temp)
        file3.close()
    df = pd.read_csv('Relations.csv')
    df = df.iloc[:-1]
    df.to_csv('Relations.csv', index=False)

def DI_AddR_To_CSV(mal, fem, dome):
    temp = ['3', mal, fem, dome]
    with open("Relations.csv", 'a') as file4:
        writer_object = writer(file4)
        writer_object.writerow(temp)
        writer_object.writerow(temp)
        file4.close()
    df = pd.read_csv('Relations.csv')
    df = df.iloc[:-1]
    df.to_csv('Relations.csv', index=False)

def DE_AddR_To_CSV(personssn):
    temp = ['4', personssn]
    with open("Relations.csv", 'a') as file5:
        writer_object = writer(file5)
        writer_object.writerow(temp)
        writer_object.writerow(temp)
        file5.close()
    df = pd.read_csv('Relations.csv')
    df = df.iloc[:-1]
    df.to_csv('Relations.csv', index=False)

def IDOLC_AddR_To_CSV(parent, child):
    temp = ['5', parent, child]
    with open("Relations.csv", 'a') as file6:
        writer_object = writer(file6)
        writer_object.writerow(temp)
        writer_object.writerow(temp)
        file6.close()
    df = pd.read_csv('Relations.csv')
    df = df.iloc[:-1]
    df.to_csv('Relations.csv', index=False)

def CRAA():
    with open('Relations.csv', 'w'):
        pass
    with open('Add.csv', 'w'):
        pass
    items.clear()
    items1.clear()
    var = tk.Variable(value = items)
    listbox.configure(listvariable = var, height=len(items))
    var1.set('None!')
    optionmenu['menu'].delete(0, 'end')
    with open("sequence.txt", "w") as f:
            f.write("""
            @startuml
       
            @enduml
            """)

def click10():
    top = tk.Toplevel(root)
    i = ['male', 'female']
    j = ['false', 'true']
    top.title('Adding a person')
    label1 = tk.Label(top, text = 'Enter the Name')
    label2 = tk.Label(top, text = 'Enter the SSN')
    label3 = tk.Label(top, text = 'Enter the Gender')
    label4 = tk.Label(top, text = 'Enter the Birth date')
    label5 = tk.Label(top, text = 'Define if this person is Dead or Not')
    inputtxt1 = tk.Entry(top, bg= 'light yellow')
    inputtxt2 = tk.Entry(top, bg= 'light blue')
    tempvar = tk.StringVar(value = i)
    tempvar.set(i[0])
    tempvar2 = tk.StringVar(value = j)
    tempvar2.set(j[0])
    inputtxt3 = tk.OptionMenu(top, tempvar, *i)
    inputtxt4 = tk.Entry(top, bg = 'light yellow')
    inputtxt5 = tk.OptionMenu(top, tempvar2, *j)
    label1.pack()
    inputtxt1.pack()
    label2.pack()
    inputtxt2.pack()
    label3.pack()
    inputtxt3.pack()
    label4.pack()
    inputtxt4.pack()
    label5.pack()
    inputtxt5.pack()
    Addbutton = tk.Button(top, text = 'Add person')
    Addbutton['command'] = lambda: [Test.Add_Person(inputtxt1.get(), inputtxt2.get(), tempvar.get(), inputtxt4.get(), tempvar2.get()), refresh(inputtxt1, inputtxt2), AddP_To_CSV(inputtxt1.get(), inputtxt2.get(), tempvar.get(), inputtxt4.get(), tempvar2.get())]
    buttemp = tk.Button(top, text = 'Close', command = top.destroy)
    Addbutton.pack()
    buttemp.pack()

def refresh(inputtxt1, inputtxt2):
    INPUT1 = inputtxt1.get()
    INPUT2 = inputtxt2.get()
    if var1.get() == 'None!':
        optionmenu['menu'].delete(0, 'end')
    items.append(f'Name: {INPUT1}  SSN: {INPUT2}')
    var = tk.Variable(value = items)
    listbox.configure(listvariable = var, height=len(items))
    items1.append(INPUT2)
    var1.initialize(value = items1[0])
    optionmenu['menu'].add_command(label = INPUT2, command = tk._setit(var1, INPUT2))

def click11():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tempvar1 = tk.StringVar()
        tempvar2 = tk.StringVar()
        tempvar1.set(items1[0])
        tempvar2.set(items1[0])
        label1 = tk.Label(top, text = 'select Dad')
        label2 = tk.Label(top, text = 'select Mom')
        optionmenu1 = tk.OptionMenu(top, tempvar1, *items1)
        optionmenu2 = tk.OptionMenu(top, tempvar2, *items1)
        buttemp1 =tk.Button(top, text = 'Close', command = top.destroy)
        buttemp = tk.Button(top, text = 'Define Dad and Mom', command = lambda: [Test.Dad_And_Mom(var1.get(), tempvar1.get(), tempvar2.get()), DAM_AddR_To_CSV(str(var1.get()), str(tempvar1.get()), str(tempvar2.get()))])
        label1.pack()
        optionmenu1.pack()
        label2.pack()
        optionmenu2.pack()
        buttemp.pack()
        buttemp1.pack()

def click12():
    if items1:
        top = tk.Toplevel(root)
        tempvar1 = tk.StringVar()
        tempvar2 = tk.StringVar()
        tempvar1.set(items1[0])
        tempvar2.set(items1[0])
        label1 = tk.Label(top, text = 'select male')
        label2 = tk.Label(top, text = 'select female')
        label3 = tk.Label(top, text = 'enter the date of marriage')
        optionmenu1 = tk.OptionMenu(top, tempvar1, *items1)
        optionmenu2 = tk.OptionMenu(top, tempvar2, *items1)
        buttemp1 = tk.Button(top, text = 'Close', command = top.destroy)
        DOM = tk.Entry(top)
        buttemp = tk.Button(top, text = 'Define Wife/Husband', command = lambda: [Test.Define_Wife_And_Hus(tempvar1.get(), tempvar2.get(), DOM.get()), WAH_AddR_To_CSV(str(tempvar1.get()), str(tempvar2.get()), str(DOM.get()))])
        label1.pack()
        optionmenu1.pack()
        label2.pack()
        optionmenu2.pack()
        label3.pack()
        DOM.pack()
        buttemp.pack()
        buttemp1.pack()

def click13():
    if items1:
        top = tk.Toplevel(root)
        tempvar1 = tk.StringVar()
        tempvar2 = tk.StringVar()
        tempvar1.set(items1[0])
        tempvar2.set(items1[0])
        label1 = tk.Label(top, text = 'select male')
        label2 = tk.Label(top, text = 'select female')
        label3 = tk.Label(top, text = 'enter the date of divorce')
        optionmenu1 = tk.OptionMenu(top, tempvar1, *items1)
        optionmenu2 = tk.OptionMenu(top, tempvar2, *items1)
        buttemp1 = tk.Button(top, text = 'Close', command = top.destroy)
        DOM = tk.Entry(top)
        buttemp = tk.Button(top, text = 'Define a Divorce', command = lambda: [Test.Divorce(tempvar1.get(), tempvar2.get(), DOM.get()), DI_AddR_To_CSV(str(tempvar1.get()), str(tempvar2.get()), str(DOM.get()))])
        label1.pack()
        optionmenu1.pack()
        label2.pack()
        optionmenu2.pack()
        label3.pack()
        DOM.pack()
        buttemp.pack()
        buttemp1.pack()

def click14():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        label1 = tk.Label(top, text = ("selected person: " + var1.get()))
        buttemp = tk.Button(top, text = 'Define death')
        buttemp['command'] = lambda: [Test.death(var1.get()), DE_AddR_To_CSV(str(var1.get()))]
        label1.pack()
        buttemp.pack()

def click15():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        tlist = Test.Show_Sisters(var1.get())
        for temp in tlist:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click16():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        tlist = Test.Show_Brothers(var1.get())
        for temp in tlist:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click17():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        tlist = Test.Show_Naveh(var1.get())
        for temp in tlist:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click18():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tempvar1 = tk.StringVar()
        tempvar1.set(items1[0])
        label1 = tk.Label(top, text = 'select child')
        optionmenu1 = tk.OptionMenu(top, tempvar1, *items1)
        buttemp1 = tk.Button(top, text = 'Close', command = top.destroy)
        buttemp = tk.Button(top, text = 'Define last child', command = lambda: [Test.Initial_Define_Of_Last_Child(var1.get(), tempvar1.get()), IDOLC_AddR_To_CSV(var1.get(), tempvar1.get())])
        label1.pack()
        optionmenu1.pack()
        buttemp.pack()
        buttemp1.pack()

def click19():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        tlist = Test.Show_Grandpa(var1.get())
        for temp in tlist:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click20():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        tlist = Test.Show_Grandma(var1.get())
        for temp in tlist:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click21():
    root.destroy()

def click22():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        temp = Test.Show_Husband(var1.get())
        if temp != None:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        temp1 = Test.Show_Wife(var1.get())
        if temp1 != None:
            tlist1.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist1), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click23():
    if var1.get() != 'None!':
        top = tk.Toplevel(root)
        tlist1 = []
        buttemp = tk.Button(top, text = 'Close')
        buttemp['command'] = top.destroy
        temp = Test.Show_Dad(var1.get())
        if temp != None:
            tlist1.append(f'Name: {temp.PI.Name}  SSN: {temp.PI.SSN}')
        temp1 = Test.Show_Mom(var1.get())
        if temp1 != None:
            tlist1.append(f'Name: {temp1.PI.Name}  SSN: {temp1.PI.SSN}')
        vartemp = tk.StringVar(value = tlist1)
        list1 = tk.Listbox(top, listvariable=vartemp, height=len(tlist1), selectmode= 'EXTENDED', width = 30, bg = 'light blue')
        list1.pack()
        buttemp.pack()

def click24():
    server.processes_file("sequence.txt")
    top = tk.Toplevel(root)
    top['background'] = 'light yellow'
    image = Image.open('sequence.png')
    image1 = ImageTk.PhotoImage(image)
    image_label = tk.Label(top,image = image1)
    image_label.image = image1
    image_label.pack()
    label1 = tk.Label(top, bg = 'light blue', width = 27, text = '-> sign means Brother/Sister!', font = 30)
    label2 = tk.Label(top, bg = 'light blue', width = 27, text = '-- means Children/Dad/Mom!', font = 30)
    label3 = tk.Label(top, bg = 'light blue', width = 27, text = '.. means Wife/Husband!', font = 30)
    buttemp = tk.Button(top, bg = 'light blue', width = 27, text = 'Close', font = 30)
    buttemp['command'] = top.destroy
    label1.pack()
    label2.pack()
    label3.pack()
    buttemp.pack()

# Bind the function to the button
button["command"] = click1
button1 = tk.Button(root, text="press to show Ammeha!", width = 27)
button1['command'] = click2
button2 = tk.Button(root, text="press to show Amooha!", width = 27)
button2['command'] = click3
button3 = tk.Button(root, text="press to show Daeeha!", width = 27)
button3['command'] = click4
button4 = tk.Button(root, text="press to show Khaleha!", width = 27)
button4['command'] = click5
button5 = tk.Button(root, text="press to show Children of khaleha!", width = 27)
button5['command'] = click6
button6 = tk.Button(root, text="press to show Children of Ammeha!", width = 27)
button6['command'] = click7
button7 = tk.Button(root, text="press to show Children of Amooha!", width = 27)
button7['command'] = click8
button8 = tk.Button(root, text="press to show Children of Daeeha!", width = 27)
button8['command'] = click9
button9 = tk.Button(root, text="press to add a person!", width = 27)
button9['command'] = click10
button10 = tk.Button(root, text="press to define Dad and Mom!", width = 27)
button10['command'] = click11
button11 = tk.Button(root, text = 'press to define Wife/Husband!', width = 27)
button11['command'] = click12
button12 = tk.Button(root, text = 'press to define a divorce!', width = 27)
button12['command'] = click13
button13 = tk.Button(root, text = 'press to define Death!', width = 27)
button13['command'] = click14
button14 = tk.Button(root, text = 'press to show sisters!', width = 27)
button14['command'] = click15
button15 = tk.Button(root, text = 'press to show brothers!', width = 27)
button15['command'] = click16
button16 = tk.Button(root, text = 'press to show naveha!', width = 27)
button16['command'] = click17
button17 = tk.Button(root, text = 'press to define last child!', width = 27)
button17['command'] = click18
button18 = tk.Button(root, text = 'press to show grandpa!', width = 27)
button18['command'] = click19
button19 = tk.Button(root, text = 'press to show grandma!', width = 27)
button19['command'] = click20
button20 = tk.Button(root, text = 'press to close the program!', width = 27)
button20['command'] = click21
button21 = tk.Button(root, text = 'press to show Husband/wife!', width = 27)
button21['command'] = click22
button22 = tk.Button(root, text = 'press to show Dad and mom!', width = 27)
button22['command'] = click23
button23 = tk.Button(root, text = 'press to show family graph!', width = 27)
button23['command'] = click24
button24 = tk.Button(root, text = 'press to clear the files(and the list)', width = 27, bg = 'pink')
button24['command'] = CRAA
# Use pack geometry manager to place the widgets
items1 = ['None!']
flag = 0
for temp in testlist:
    if flag == 0:
        items1.clear()
    items1.append(temp.PI.SSN)
    flag = 1
label.pack()
var1 = tk.StringVar(value = items1)
var1.set(items1[0])
optionmenu = tk.OptionMenu(root, var1, *items1)
optionmenu['background'] = 'light blue'
optionmenu['width'] = 25
optionmenu.pack()
button['background'] = 'light yellow'
button.pack()
button1['background'] = 'light yellow'
button1.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) - 150)
button2['background'] = 'light yellow'
button2.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) - 150)
button3['background'] = 'light blue'
button3.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) - 125)
button4['background'] = 'light yellow'
button4.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) - 100)
button5['background'] = 'light blue'
button5.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) - 125)
button6['background'] = 'light yellow'
button6.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) - 100)
button7['background'] = 'light blue'
button7.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) - 75)
button8['background'] = 'light yellow'
button8.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) - 50)
button9['background'] = 'light blue'
button9.pack()
button10['background'] = 'light yellow'
button10.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) - 50)
button11['background'] = 'light blue'
button11.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) - 75)
button12['background'] = 'light yellow'
button12.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) + 50)
button13['background'] = 'light blue'
button13.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) + 25)
button14['background'] = 'light yellow'
button14.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) + 50)
button15['background'] = 'light blue'
button15.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) + 25)
button16['background'] = 'light blue'
button16.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) - 25)
button17['background'] = 'light blue'
button17.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) - 25)
button18['background'] = 'light yellow'
button18.place(x = root.winfo_width() - (root.winfo_width() - 20), y = root.winfo_height()/2)
button19['background'] = 'light yellow'
button19.place(x = root.winfo_width() - 210, y = root.winfo_height()/2)
button20['background'] = 'light blue'
button23['background'] = 'lightyellow'
button23.pack()
button24.pack()
button20.pack()
button21['background'] = 'light blue'
button21.place(x = root.winfo_width() - 210, y = (root.winfo_height()/2) + 75 )
button22['background'] = 'light blue'
button22.place(x = root.winfo_width() - (root.winfo_width() - 20), y = (root.winfo_height()/2) + 75)
if items1[0] == 'None!':
    CRAA()
# Enter the main loop
root.mainloop()
#Choice = 26
#while Choice != 0:
#    test_list = Test.HT.Show_Everyone()
#    for temp in test_list:
#        print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#    print('press 1 to show someones childrens!')
#    print('press 2 to show someones ammeha!')
#    print('press 3 to show someones amooha!')
#    print('press 4 to show someones daeeha!')
#    print('press 5 to show someones khaleha!')
#    print('press 6 to show children of someones khaleha!')
#    print('press 7 to show children of someones ammeha!')
#    print('press 8 to show children of someones amooha!')
#    print('press 9 to show children of someones dayeeha!')
#    print('press 10 to add a person!')
#    print('press 11 to define someones dad and mom!')
#    print('press 12 to define someones husband/wife!')
#    print('press 13 to define a divorce!')
#    print('press 14 to define a death!')
#    print('press 15 to show someones sisters!')
#    print('press 16 to show someones brothers!')
#    print('press 17 to show someones naveha')
#    print('press 18 to define the last child of someone(just in case they have divorced and you havent yet added the other person)')
#    print('press 19 to show someones grandpas!')
#    print('press 20 to show someones grandmas!')
#    print('press 21 to show someones Husband!')
#    print('press 22 to show someones Wife!')
#    print('press 23 to show someones Dad and Mom!')
#    print('press 0 to quit the program!')
#    temp_temp = input("pls select the function:")
#    if len(temp_temp) != 0:
#        Choice = int(temp_temp)
#        if Choice == 1:
#            personssn = input('pls enter the person SSN to show his/her children!')
#            childrenlist = Test.Show_Children(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 2:
#            personssn = input('pls enter the person SSN to show his/her ammeha!')
#            childrenlist = Test.Show_Ammeha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 3:
#            personssn = input('pls enter the person SSN to show his/her amooha!')
#            childrenlist = Test.Show_Amooha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 4:
#            personssn = input('pls enter the person SSN to show his/her daeeha!')
#            childrenlist = Test.Show_Daeeha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 5:
#            personssn = input('pls enter the person SSN to show his/her khaleha!')
#            childrenlist = Test.Show_Khaleha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 6:
#            personssn = input('pls enter the person SSN to show his/her children of khaleha!')
#            childrenlist = Test.Show_Children_Of_Khaleha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 7:
#            personssn = input('pls enter the person SSN to show his/her children of ammeha!')
#            childrenlist = Test.Show_Children_Of_Ammeha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 8:
#            personssn = input('pls enter the person SSN to show his/her children of amooha!')
#            childrenlist = Test.Show_Children_Of_Amooha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 9:
#            personssn = input('pls enter the person SSN to show his/her children of daeeha!')
#            childrenlist = Test.Show_Children_Of_Daeeha(personssn)
#            for temp in childrenlist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 10:
#            name = input('pls enter the person Name')
#            ssn = input('pls enter the person SSN')
#            sex = input('pls enter the person Sex')
#            birth = input('pls enter the person birthdate like this: dd/mm/yy')
#            death = input('pls enter y if the person is dead and n if not')
#            if death == 'y':
#                death = 'true'
#            elif death == 'n':
#                death = 'false'
#            Test.Add_Person(name, ssn, sex, birth, death)
#        elif Choice == 11:
#            personssn = input('pls enter the person SSN!')
#            dadssn = input('pls enter the persons dad SSN')
#            momssn = input('pls enter the persons mom SSN')
#            Test.Dad_And_Mom(personssn, dadssn, momssn)
#        elif Choice == 12:
#            malessn = input('pls enter the male SSN')
#            femalessn = input('pls enter the female SSN')
#            date = input('pls enter the date as fallow: dd/mm/yy')
#            Test.Define_Wife_And_Hus(malessn, femalessn, date)
#        elif Choice == 13:
#            malessn = input('pls enter the male SSN')
#            femalessn = input('pls enter the female SSN')
#            date = input('pls enter the date as fallow: dd/mm/yy')
#            Test.Divorce(malessn, femalessn, date)
#        elif Choice == 14:
#            personssn = input('pls enter a person SSN to define his death')
#            Test.death(personssn)
#        elif Choice == 15:
#            personssn = input('pls enter a person SNN to Show his/her sisters')
#            templist = Test.Show_Sisters(personssn)
#            for temp in templist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 16:
#            personssn = input('pls enter a person SNN to Show his/her brothers')
#            templist = Test.Show_Brothers(personssn)
#            for temp in templist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 17:
#            personssn = input('pls enter a person SSN to Show his/her naveha')
#            templist = Test.Show_Naveh(personssn)
#            for temp in templist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 18:
#            parentssn = input('pls enter a person SSN to define his/her last child')
#            childssn = input('pls enter the child SSN')
#            templist = Test.Initial_Define_Of_Last_Child(parentssn, childssn)
#            for temp in templist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 19:
#            personssn = input('pls enter a person SSN to Show his/her grandpas')
#            templist = Test.Show_Grandpa(personssn)
#            for temp in templist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 20:
#            personssn = input('pls enter a person SSN to Show his/her grandmas')
#            templist = Test.Show_Grandma(personssn)
#            for temp in templist:
#                print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 21:
#            personssn = input('pls enter a person SSN to Show her husband')
#            temp = Test.Show_Husband(personssn)
#            print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 22:
#            personssn = input('pls enter a person SSN to Show his wife')
#            temp = Test.Show_Wife(personssn)
#            print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 23:
#            personssn = input('pls enter a person SSN to Show his wife')
#            temp = Test.Show_Dad(personssn)
#            print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#            temp = Test.Show_Mom(personssn)
#            print(f"Name: {temp.PI.Name}, SSN: {temp.PI.SSN}")
#        elif Choice == 0:
#            break
#        else:
#            continue