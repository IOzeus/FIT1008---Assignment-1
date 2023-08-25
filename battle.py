from __future__ import annotations
from enum import auto
from typing import Optional
from monster_base import MonsterBase
from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:

        '''
        :complexity: O(1)
        Catch all: Please note complexity is for best case and worse case if not specificied for each, and also constant if not noted at all (this is for all functions in this module)
        also note, not all line by line complexity is not noted; the catch all is only for whole functions as this complexity analysis is only done to determine
        and show the whole functions complexity
        '''
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        :complexity: Best case: O(n)
        Worse case: O(nlog(n)^2)
        -> n = length of monsters in team array (specifically when team Optimise mode)

        Process a single turn of the battle:
        * process' actions chosen by each team
        * levels and evolves monsters
        * removes fainted monsters and retrieve new ones.
        * returns the battle result if completed.
        """

        '''SWAP LOGIC---------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        if self.team1.choose_action(self.out1, self.out2) == self.Action.SWAP: # Swaps the monster on field with the one retrieve from the team (for team1)
            monster_onField = self.out1 # store monster currently on field
            self.out1 = self.team1.retrieve_from_team() # then asssign self.out1 - i.e the monster you want to bring on field - to .retrieve_from...() i.e monster from team
            self.team1.add_to_team(monster_onField) #store the monster that was on the field back in the team
        
        elif self.team2.choose_action(self.out2, self.out1) == self.Action.SWAP:
            monster_onField = self.out2
            self.out2 = self.team2.retrieve_from_team()
            self.team2.add_to_team(monster_onField) #worse: logn
        '''---------------------------------------------------------------------------------------------------------------------------------------------------------------'''

        '''SPECIAL LOGIC---------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        if self.team1.choose_action(self.out1, self.out2) == self.Action.SPECIAL:
            self.team1.special() #Best case: O(n) Worse case: O(nlog(n)^2)
        elif self.team2.choose_action(self.out2, self.out1) == self.Action.SPECIAL: #same as above but for team2  
            self.team2.special()
        '''---------------------------------------------------------------------------------------------------------------------------------------------------------------'''
            
        '''---------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        monster1_dead: bool = False #monsters always alive when starting
        monster2_dead: bool = False    

        '''BOTH TEAMS SELECTED TO ATTACK ON THE SAME PROCESS TURN---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        if (self.team1.choose_action(self.out1, self.out2) == self.Action.ATTACK) and (self.team2.choose_action(self.out2, self.out1) == self.Action.ATTACK): #if both teams attack at same time 

            '''FIRST MONSTER SPEED STAT IS BIGGER########################################################################################################################################################################'''
            if (self.out1.get_speed() > self.out2.get_speed()): # if first monster speed faster than second then the first monster attacks first

                self.out1.attack(self.out2) #if so run attack i.e compute damage
                monster2_dead = self.__after_attack_logics(self.out1, self.out2, self.team1, self.team2, 2) #check if the monster has been killed (Boolean) 

                #It the attacked monster (monster2) died then it can attack back 
                if not monster2_dead: # if the second monster is not dead - i.e monster2_dead=false (not false == true) -  then the second monster can attack the first

                    self.out2.attack(self.out1) #same as above
                    monster1_dead = self.__after_attack_logics(self.out2, self.out1, self.team2, self.team1, 1) #same as above
                
                '''SECOND MONSTER SPEED STAT IS BIGGER###################################################################################################################'''
            elif (self.out2.get_speed() > self.out1.get_speed()): # if second monster speed is bigger than first monster the second attacks first
                self.out2.attack(self.out1)
                monster1_dead = self.__after_attack_logics(self.out2, self.out1, self.team2, self.team1, 1)
                
                if not monster1_dead:

                    self.out1.attack(self.out2)
                    monster2_dead = self.__after_attack_logics(self.out1, self.out2, self.team1, self.team2, 2) 
                '''###############################################################################################################################################################################################################'''
                
                '''DRAW IN ATTACKING SPEEDS LOGIC##########################################################################################################################################'''
            elif (self.out2.get_speed() == self.out1.get_speed()): #If attack speeds equal
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)

                #We save the monster so we can check process the attack on the monster that been attacked instead of the present monster alive
                monster1 = self.out1
                monster2 = self.out2
                monster1_dead = self.__after_attack_logics(monster2, monster1, self.team2, self.team1, 1)
                monster2_dead = self.__after_attack_logics(monster1, monster2, self.team1, self.team2, 2)
            '''#################################################################################################################################################################'''


            '''TEAM 1 PICKS ATTACK ONLY (OTHER TEAM MUST'VE PICKED SOMETHING ELSE TO NOT HIT CONDITION ABOVE)##########################################################################################################################################'''
        elif self.team1.choose_action(self.out1, self.out2) == self.Action.ATTACK:
            self.out1.attack(self.out2)
            monster2_dead = self.__after_attack_logics( self.out1, self.out2, self.team1, self.team2, 2)
            '''##########################################################################################################################################'''
            
            '''TEAM 2 PICKS ATTACK ONLY (OTHER TEAM MUST'VE PICKED SOMETHING ELSE TO NOT HIT CONDITION ABOVE)#####################################################################'''
        elif self.team2.choose_action(self.out2, self.out1) == self.Action.ATTACK:
            self.out2.attack(self.out1)
            monster1_dead = self.__after_attack_logics(self.out2, self.out1, self.team2, self.team1, 1)
            '''##########################################################################################################################################'''
        '''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        
        '''BOTH ALIVE LOGIC-----------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        if not monster1_dead and not monster2_dead: #subtract 1 hp from both monsters if they both survive
            self.out2.set_hp(self.out2.get_hp() - 1)
            self.out1.set_hp(self.out1.get_hp() - 1)

            monster1 = self.out1
            monster2 = self.out2
            self.__after_attack_logics(monster1, monster2, self.team1, self.team2, 2)
            self.__after_attack_logics( monster2, monster1, self.team2, self.team1, 1)

        if self.result: #if result has been assigned a value other than None then the function will return the result
            return self.result
        
    def __after_attack_logics(self, attacking_monster: MonsterBase, attacked_monster: MonsterBase, attacking_team: MonsterTeam, attacked_team: MonsterTeam, ref_num: int):
        """

        :complexity: O(1)

        Does the functionality that happens after a monster has attacked: RETURNS True if attacked monster died

        It sets self.result

        It handles attacking at same time logic

        It handles dying monster (replaces it with alive one from team, if team isn't all dead)

        :attacking_monster: The monster that attacked
        :attacked_monster: The monster that was attacked
        :attacking_team: The team of the monster that was attacking
        :attacked_team: The team of the monster that was attacked
        :ref_num: The reference number of the team that was attacked 
        """

        '''ATTACKED MONSTER DIED LOGIC---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        if (attacked_monster.get_hp()) <= 0: #if attacked monster died

            if (ref_num==1): #team is the first team: team1
                    self.out1 = attacked_team.retrieve_from_team() #replace dead monster with the next monster from the team    
            else:
                    self.out2 = attacked_team.retrieve_from_team() #same as above but grabs it from the 2nd monsters team - as the team variable that should be inputted should be of the attacked monsters team (i.e the one that just died)
            '''------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

            '''ATTACKING MONSTER STILL ALIVE LOGIC------------------------------------------------------------------------------------------------------------------------------------------------------------'''
            if (attacking_monster.get_hp()>0): #if attacking monster is alive
                
                attacking_monster.level_up() #level that boy up
                if (attacking_monster.ready_to_evolve()): #if its ready to evolve 

                    '''EVOLVE LOGIC-------------------------------------------------'''
                    if (ref_num==1):
                        self.out2 = attacking_monster.evolve() #evolve the attacking monster because he killed the other and leveled up and assign it to the monster currently out
                        #if team that was attacked is team1 level up the attacking team's monster

                    elif (ref_num==2): 
                        self.out1 = attacking_monster.evolve()   #if team that was attacked is team2 level up the attacking team's monster
                    '''-------------------------------------------------------------'''
            '''------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

            '''RESULT LOGIC-----------------------------------------------------------------------------------------------------------------------------'''
            if ((attacked_team.team.is_empty()) and (attacking_team.team.is_empty()) and (attacking_monster.get_hp()<=0) and (attacked_monster.get_hp()<=0)): # if the last two monsters attacked at the same time and killed each other at same time it's a draw)
                self.result = self.Result.DRAW # draw the result

            elif (attacked_team.team.is_empty()) and (attacked_monster.get_hp()<=0) and (ref_num==1) : #if attacked team is empty and their last monster on field just died
                    self.result = self.Result.TEAM2 # team2 wins
            
            elif (attacked_team.team.is_empty()) and (attacked_monster.get_hp()<=0) and (ref_num==2) :
                    self.result = self.Result.TEAM1

            return True #Returns True implying monster attacked died, this then is used to stop other monster from attacking (used in process_turn())
        '''-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
        return False #returns false if the initial condition (the attacked monster didn't die hp<=0) i.e false for it didn't die
    

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        self.result = None
        
        while self.result is None:
            self.result = self.process_turn()
        
        if self.result == Battle.Result.DRAW:
            print(f'Its a {self.result}!')

        else:
            print(f'Congrats {self.result} you won!')
        # Add any postgame logic here.
        return self.result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
