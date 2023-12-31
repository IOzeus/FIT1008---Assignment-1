from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import SortedList, ListItem

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto() 
        '''In TeamMode.FRONT, when a monster is added to a team, it is always added to the front of the team array[0]. 
        Note that this means it is this monster that will be next retrieved from the team again.'''
        BACK = auto()
        '''In TeamMode.BACK, when a monster is added to a team, it is always added to the back of the team. 
        Note that this means this monster will be the last to be retrieved from the team.'''
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):
        
        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:

        '''
        :complexity: Best case: O(n) 
        Worse Case: O(nlog(n)) (Specifically when team is Optimse Mode)
        -> n = length of monsters in team array

        Catch all: Please note complexity is for best case and worse case if not specificied for each, and also constant if not noted at all (this is for all functions in this module) 
        also note, not all line by line complexity is noted; the catch all is only for whole functions as this complexity analysis is only done to determine
        and show the whole functions complexity
        '''
        self.length = 0
        self.ascending = False
        self.team_mode = team_mode #team mode selected: Front Back or Optimise
        
        if self.team_mode == self.TeamMode.OPTIMISE:
            self.clone_team = ArraySortedList(self.TEAM_LIMIT)
        else:
            self.clone_team = CircularQueue(self.TEAM_LIMIT)

        if self.team_mode == self.TeamMode.FRONT:
            self.team = ArrayStack(self.TEAM_LIMIT) #just make it the max size because they might wanna change it
        elif self.team_mode == self.TeamMode.BACK:
            self.team = CircularQueue(self.TEAM_LIMIT) 
        elif self.team_mode == self.TeamMode.OPTIMISE:
            self.team = ArraySortedList(self.TEAM_LIMIT)
            self.sort_mode = kwargs.get('sort_key') #returns what value player chose to sort monsters with in array
        else:
            raise ValueError(f"team_mode {team_mode} not supported.")

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)  #Best case: O(n) Worse case: O(nlog(n)) 
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs) #same as above
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs) #save as abover
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
        
    def __len__(self):
        return self.length

    def __sorting_key(self, monster: MonsterBase, sort_mode: SortMode): #MAKE function for if sort_mode return mosnter hp or attack or etc
        '''
        quick helper method for getting the monsters stat we're sorting the monsters in the array by
        
        :complexity: O(1)
        
        :monster: monster object/value to sort
        :sort_mode: sorting mode you want to sort the monster by in array'''
        if self.sort_mode == self.SortMode.HP:
            return monster.get_hp()
        elif self.sort_mode == self.SortMode.ATTACK:
            return monster.get_attack()
        elif self.sort_mode == self.SortMode.DEFENSE:
            return monster.get_defense()
        elif self.sort_mode == self.SortMode.SPEED:
            return monster.get_speed()
        elif self.sort_mode == self.SortMode.LEVEL:
            return monster.get_level()

    def add_to_team(self, monster: MonsterBase):
        ''':monster: monster object to add to team
        Adds desired monster class to team ADT
        
        :complextiy: Best case: O(1) 
        Worse case:  O(log(n)) (Specifically when team is Optimse Mode)
        -> n = length of monster in team array
        '''
        self.length = self.length + 1
        if not self.team.is_full():
        #For Front team mode added to front of team, FILO
            if self.team_mode == self.TeamMode.FRONT: # if team mode is 'front' adds monster to array[0]
                self.team.push(monster) #add monster to top of stack
            #For Back team mode added to the back of the team, FIFO
            if self.team_mode == self.TeamMode.BACK: #if team mode is 'back' adds monster to array[-1]
                self.team.append(monster) #add monster to back of queue
            #For Optimised team mode (sorted in picked order of the monster stat chosen: largest - lowest)
            if self.team_mode == self.TeamMode.OPTIMISE:
                if self.ascending: #for if its ascending don't multiply the key by -1 (incase user adds monster to team directly using function)
                    if monster.get_hp()>0:
                        monster = ListItem(monster, self.__sorting_key(monster, self.sort_mode))
                        self.team.add(monster)
                else:
                    # if monster.
                    monster = ListItem(monster, (-1)*self.__sorting_key(monster, self.sort_mode)) #create key and value of the chosen monster class key to sort it sort_key i.e hp,attack etc, value is the monster
                    self.team.add(monster) #adds monster according to order it should be in
        else:
            Exception("Team is full can't add monsters")

    def __initial_team (self, monster: MonsterBase):
        '''Helper function to just run on initialisation to clone the orginal team
        
        :complextiy: Best case O(1) 
        Worse case: O(log(n)) (Specifically when team is Optimse Mode)
        -> n = length of monsters in team array 
        '''
        if self.team_mode == self.TeamMode.OPTIMISE:
            monster = ListItem(monster, (-1)*self.__sorting_key(monster, self.sort_mode))
            self.clone_team.add(monster)
        
        else:
            self.clone_team.append(monster) #add monsters to clone team

    def retrieve_from_team(self) -> MonsterBase:
        '''
        Retrieves a monster from the team, changes depending on team mode of team
        In a battle, monsters will be retrieved from the team and used in battle. 
        If a monster is swapped out, then it is added back into the team.
        
        :complexity: O(1)'''
        self.length = self.length - 1

        #Retrives monster from front array[0] then deletes it from array
        if self.team_mode == self.TeamMode.FRONT:
            return self.team.pop()
        
        #Retrives monster from back array[-1] then deletes it from array
        elif self.team_mode == self.TeamMode.BACK:
            return self.team.serve()
        
        #Retrives monster from back array[-1] then deletes it from array
        elif self.team_mode == self.TeamMode.OPTIMISE:

            return self.team.delete_at_index(0).value

    def special(self) -> None:
        '''
        :complexity: Best case: O(n) 
        Worse case: O(nlog(n)) (Specifically when team is Optimse Mode)
        -> n = length of monsters in team array

        Does a special rearrangement of current team line up depending on team mode of team

        For TeamMode.FRONT:When team.special is used, the first 3 monsters at the front are reversed 
        (Up to the current capacity of the team) i.e array index 0,1,2 elements are reversed so these elements from these
         index end up in this order 2,1,0 therefor saying array[0]=array[2], array[1]=array[1], array[2]=array[0]'''
        
        '''For TeamMode.BACK: When team.special is used, the first half of the team is swapped with the second half 
        (in an odd team size, the middle monster is in the bottom half), and the original second half of the team is reversed.'''

        '''For TeamMode.OPTIMISE: For example, if the initial stat was HP, then monsters would be inserted so that they are sorted by HP descending.
        In the case of a draw in the statistic selected, you can order the monsters in either order. It does not matter.
        When team.special is used, the sorting order toggles from descending to ascending (or vice-versa if used again).
        '''
        #reverse organisations of monsters in team for team_mode Front
        
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            temp = CircularQueue(len(self.team)) 
            '''it doesn't override the team objects because I'm not playing with objects but resetting the assignment of the variable with name 'temp' whole variable'''

            for _ in range(min(3,len(self.team))):
                temp.append(self.team.pop())
            
            for _ in range(len(temp)):
                self.team.push(temp.serve())

        #for team_mode back
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            
            #find sizes of the halfs
            size_firstHalf = len(self.team)//2 #floor division
            size_lastHalf= len(self.team) - size_firstHalf 

            #create temp arrays of both halfs
            firstTeam_adt = CircularQueue(size_firstHalf)
            lastTeam_adt = ArrayStack(size_lastHalf) #second half array
            
            for _ in range(size_firstHalf): #take the front half from original array and move them to first team array (keeping the order)
                firstTeam_adt.append(self.team.serve())

            for _ in range(size_lastHalf): #take the last half from original array and move them to last (second) half team array (keeping the order)
                lastTeam_adt.push(self.team.serve())

            for _ in range(size_lastHalf): #take the second half and put it back into team array reversed
                self.team.append(lastTeam_adt.pop())

            for _ in range(size_firstHalf): #take the first half and put it back into team array keeping its order
                self.team.append(firstTeam_adt.serve())
  
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            
            temp = ArraySortedList(len(self.team))
            self.ascending = not self.ascending

            for _ in range(len(self.team)): #n 
                temp.add(self.team.delete_at_index(0))#log(n)

                monster_inListobject = temp.delete_at_index(0)
                monster_inListobject.key = monster_inListobject.key*-1
                self.team.add(monster_inListobject)#log(n)


        

    def regenerate_team(self) -> None:
        '''
        Puts team line up back to how it was upon it's first creation

        :complexity: Best Case: n+m (depends which one is larger dominates) 
        Worse Case: mlog(m) (specifically when team Optimise mode)
        -> n = length of monsters in team array 
        -> m = length of monsters in cloned team array
          '''
        for _ in range(len(self.team)): # n just removes all monster objects in current team array
            if self.team_mode == self.TeamMode.FRONT:
                self.team.pop()

            elif self.team_mode == self.TeamMode.BACK:
                self.team.serve()

            elif self.team_mode == self.TeamMode.OPTIMISE:
                self.team.delete_at_index(0)

        for i in range(len(self.clone_team)):  # m adds all monsters put in clone array at initialisation into the now empty team array
            
            if self.team_mode == self.TeamMode.FRONT:
                self.team.push(self.clone_team.serve())

            elif self.team_mode == self.TeamMode.BACK:
                self.team.append(self.clone_team.serve())

            elif self.team_mode == self.TeamMode.OPTIMISE:
                self.team.add(self.clone_team.__getitem__(i)) #O(logm) 
                

    def select_randomly(self):

        ''' 
        Selects the size of the team and the monsters in the time randomly for you
        
        :complexity: Best case: O(n) 
        Worse case: O(nlog(n)) (Specifically when team is Optimse Mode)
        -> n = length of monsters in team array
        '''
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size): #n
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]()) #log(n)
                        self.__initial_team(monsters[x]()) #log(n)
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        '''
        Select the monsters you want in your team by picking from the list of spawnable mosnters

        :complexity: Best case: O(n) 
        Worse case: nlog(n) (Specifically when team is Optimse Mode)

        -> n = team size picked by the user i.e amount of monsters they want in the time
        '''

        #pick team size if wrong input pull exception then continue
        while True:
            try:
                team_size = int(input('How many monsters are there?: '))

                
            except ValueError: #Try again... Return to the start of the loop
                print("Invalid input, needs to be an integer. Reinput size.\n")
                continue
            else:
                if (team_size<1) or (team_size>6):
                    print("Invalid input, team size needs to be between or including sizes 1 to 6. Reinput size.\n")
                    continue
                break

        print("Spawnable monsters are: \n")
        monster_list = get_all_monsters()
        for i, cls_monster in enumerate(monster_list, start = 1): #print spawnable monster classes with corresponding index (i)
                    if cls_monster.can_be_spawned():
                         print(f"{i}: {cls_monster.get_name()}\n")
                    else:
                        continue

        for _ in range(team_size): # iterate as many as team size, choose monsters you want in team
                
                chosen_monster = int(input('Which monster are you spawning? (select integer): '))

                while not monster_list[chosen_monster-1].can_be_spawned(): #if selected monster isn't spawnable get them to select again (iterates until spawnable monster)
                    print ("You can't spawn that monster\n")
                    chosen_monster = int(input('Which monster are you spawning? (select integer): '))

                self.add_to_team(monster_list[chosen_monster-1]()) #add chosen monster to team
                self.__initial_team(monster_list[chosen_monster-1]()) #log(N)
                
                print(f"You added {monster_list[chosen_monster-1].get_name()} to the team. Here's your line up right now: {print(self.team)} ") #show them the team now
    
    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None, **kwargs):
        """
        Generates a team based on a list of already provided monster classes/objects.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]

        :complexity: Best case: O(n) 
        Worse case: O(nlog(n)) (Specifically when team is Optimse Mode)
        -> n = Number of monsters provided in array
        """
        if len(provided_monsters) < 6 and len(provided_monsters) > 0 : #Check no. of monsters added are below 6 and above 0
            for monster in provided_monsters: #loop through provided monsters
                
                if self.team.is_full():
                    raise Exception(f"Team is Full: {monster.get_name()} couldn't be added to the team because team is now full")
                elif monster.can_be_spawned():
                    self.add_to_team(monster()) #add each monster into array (according to team_mode which is builtin to add_to_team)
                    self.__initial_team(monster())
        else: #if length of monsters provided were bigger than 6 or less than 1 then Exception
            return ValueError("Too many monsters or a monster cannot be spawned")
            # raise Exception('Either you have too many monsters - you can only have a max of 6 in a team or,\nYou have no monsters or,\n team is full')

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    print("\nARE YOU WORKING\n")
    '''team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )'''
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
    )
    print("\nARE YOU WORKING\n")
    team.select_manually()
    #while len(team):
        #print(team.retrieve_from_team())
    
