from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR

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

        self.team_mode = team_mode #team mode selected: Front Back or Optimise
        self.sort_mode = kwargs.get('sort_mode') #returns what value player chose to sort monsters with in array
        self.team = ArrayR(6) 
        '''create default array, although is there a better way? also am I 
        creating too many arrays at difference spots in the code'''

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
        
    def add_to_team(self, monster: MonsterBase):

        #For Front team mode added to front of team, FILO
        from data_structures.stack_adt import ArrayStack
        if self.team_mode == self.TeamMode.FRONT: # if team mode is 'front' retrieves monster from array[0]
            self.team = ArrayStack() # insert ArrayR into ArrayStack ADT so it gets it properties
            self.team.push(monster) #add monster to top of stack
            '''is this right? should i be inputting into stack self.team.team_size or nothing?'''

        #For Back team mode added to the back of the team, FIFO
        from data_structures.queue_adt import CircularQueue
        if self.team_mode == self.TeamMode.BACK: #if team mode is 'back' retrieves monster from array[-1]
            self.team = CircularQueue() # insert base ArrayR into CircularQueue ADT so it gets it properties
            self.team.append(monster) #add monster to back of queue
            '''is this right? should i be inputting into CircularQueue self.team.team_size or nothing?'''

        #For Optimised team mode (sorted in picked order of the stat chosen: largest - lowest)
        from data_structures.array_sorted_list import ArraySortedList
        from data_structures.sorted_list_adt import SortedList, ListItem
        if self.team_mode == self.TeamMode.OPTIMISE:
            monster = ListItem(monster, self.sort_mode) #create key and value of the chosen monster class key to sort it sort_mode i.e hp,attack etc, value is the monster
            self.team = ArraySortedList(self.team) # insert base ArrayR into Arraysortedlist ADT so it gets it properties
            self.team.add(monster) #adds monster according to order it should be in
            '''is this right? should I be inputting into Arraysortlist self.team.team_size or nothing?'''

    def retrieve_from_team(self) -> MonsterBase:
        '''In a battle, monsters will be retrieved from the team and used in battle. 
        If a monster is swapped out, then it is added back into the team.'''

        #Retrives monster from front array[0] then deletes it from array
        if self.team_mode == self.TeamMode.FRONT:
            return self.team.pop()
        
        #Retrives monster from back array[-1] then deletes it from array
        if self.team_mode == self.TeamMode.BACK:
            return self.team.serve()
        
        if self.team_mode == self.TeamMode.OPTIMISE:
            return self.team.__getitem__(0) 
        '''gets item from from (IDK IF THIS IS CORRECT DOUBLE CHECK)'''

    def special(self) -> None:
        '''For TeamMode.FRONT:When team.special is used, the first 3 monsters at the front are reversed 
        (Up to the current capacity of the team) i.e array index 0,1,2 elements are reversed so these elements from these
         index end up in this order 2,1,0 therefor saying array[0]=array[2], array[1]=array[1], array[2]=array[0]'''
        
        '''For TeamMode.BACK: When team.special is used, the first half of the team is swapped with the second half 
        (in an odd team size, the middle monster is in the bottom half), and the original second half of the team is reversed.'''

        '''For TeamMode.OPTIMISE: For example, if the initial stat was HP, then monsters would be inserted so that they are sorted by HP descending.
        In the case of a draw in the statistic selected, you can order the monsters in either order. It does not matter.
        When team.special is used, the sorting order toggles from descending to ascending (or vice-versa if used again).'''
        pass
        #raise NotImplementedError

    def regenerate_team(self) -> None:
        pass
        #raise NotImplementedError

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        #pick team size if wrong input pull exception then continue
        while True:
            try:
                team_size = int(input('How many monsters are there?: '))
                self.team = ArrayR(team_size)
                
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
        for i, cls_monster in enumerate(monster_list, start= 1): #print spawnable monster classes with corresponding index (i)
                    if cls_monster.can_be_spawned():
                         print(f"{i}: {cls_monster.get_name()}\n")
                    else:
                        continue

        for j in range(team_size): # iterate as many as team size, choose monsters you want in team
                
                chosen_monster = int(input('Which monster are you spawning? (select integer): '))

                while not monster_list[chosen_monster-1].can_be_spawned(): #if selected monster isn't spawnable get them to select again (iterates until spawnable monster)
                    print ("You can't spawn that monster\n")
                    chosen_monster = int(input('Which monster are you spawning? (select integer): '))

                self.add_to_team(monster_list[chosen_monster-1]) #add chosen monster to team

                print(f"You added {monster_list[chosen_monster-1].get_name()} to the team. Here's your line up right now: {print(self)} ") #show them the team now
        return team
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        pass
        #raise NotImplementedError

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
    
