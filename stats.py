import abc

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import SortedList, ListItem
import math

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        """
        Catch all: O(1) for all SimpleStats functions

        :attack: Attack stat of monster
        :defense: Defense stat of monster
        :speed: Speed stat of monster
        :max_hp: Max health point stat of monster
        """
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp

    def get_attack(self):
        return self.attack


    def get_defense(self):
        return self.defense
        

    def get_speed(self):
        return self.speed
    

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(self, attack_formula: ArrayR[str], defense_formula: ArrayR[str], speed_formula: ArrayR[str], max_hp_formula: ArrayR[str],) -> None:
        '''
        Cactch all: All functions in this class ComplexStats have a complexity of O(n) except the initialiser
        Also, unless specifically mentioned, complexity is for both best and worse case
        '''
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    def get_attack(self, level: int):
        return self.evaluate(self.attack_formula,level)

    def get_defense(self, level: int):
        return self.evaluate(self.defense_formula, level)

    def get_speed(self, level: int):
        return self.evaluate(self.speed_formula, level)

    def get_max_hp(self, level: int):
        return self.evaluate(self.max_hp_formula, level)
    
    def evaluate(self, expression : ArrayR[str], level: int) -> int:
        """
        :complexity: O(n) -> n = length of expression array
        Evaluates the expression given in post-fix notation

        :level: The level of the monster
        :expression: Array of the post fix notation for the expression to be calculated
        """
        
        operators = ArrayR.from_list(['power', 'sqrt', 'middle', '/', '+', '*', '-']) #If we encounter then pop and evaluate
        holder = ArrayStack(len(expression))

        for element in range (len(expression)): #O(n)

            if not (expression[element] == None):
                top_of_stack = expression[element]

                if top_of_stack in operators: # O(1)

                    if not (top_of_stack=='sqrt'): # if not square root sends it done bottom to get square rooted real quick
                        a = holder.pop()
                        b = holder.pop()
                        if top_of_stack == "middle": # if median works out median
                            sorted_list = ArraySortedList(3)
                            c = holder.pop()
                            sorted_list.add(ListItem(float(a),float(a)))
                            sorted_list.add(ListItem(float(b),float(b)))
                            sorted_list.add(ListItem(float(c),float(c)))
                            median = str(sorted_list[1].value)
                            holder.push(median)
                        elif top_of_stack=='/':
                            result = float(b) / float(a)
                            holder.push(str(result))
                        elif top_of_stack=='+':
                            result = float(a) + float(b)
                            holder.push(str(result))
                        elif top_of_stack=='*':
                            result = float(a) * float(b)
                            holder.push(str(result))
                        elif top_of_stack=='-':
                            result = float(b) - float(a)
                            holder.push(str(result))
                        elif top_of_stack == 'power':
                            power_result =  float(b) ** float(a)
                            holder.push(str(power_result))

                    elif top_of_stack == 'sqrt': #squareroot the number number push it back in
                        a = holder.pop()
                        holder.push( math.sqrt(float(a)) )

                elif top_of_stack not in operators:
                    if top_of_stack == "level":
                        holder.push(level)
                    else:
                        holder.push(top_of_stack) 

        final_value = float(holder.pop())
        return int(final_value)
    
    
    
