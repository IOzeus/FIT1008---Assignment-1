from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import SortedList, ListItem

from elements import Element

from data_structures.referential_array import ArrayR

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        '''
        Catch all: Please note complexity is for best case and worse case if not specificied for each, and also constant if not noted at all (this is for all functions in this module)
        also note, not all line by line complexity is noted; the catch all is only for whole functions as this complexity analysis is only done to determine
        and show the whole functions complexity
        '''
        self.battle = battle or Battle(verbosity=0)
        self.teamPlayer = None
        self.all_enemy_teams = None

    def set_my_team(self, team: MonsterTeam) -> None:
        ''':complexity: O(n)'''
        self.teamPlayer = team
        self.teamPlayer.lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES) #create new variable to team array called live and give it a number

    def generate_teams(self, n: int) -> None:
        '''
        Generates random enemy teams
        :complexity: O(n) -> n = amount of enemy teams to generate
        '''

        self.encountered_elements = CircularQueue(MonsterTeam.TEAM_LIMIT*n+1) #set encountered element size to max size of teams* amount of enemy teams +1 (player team)

        self.all_enemy_teams = CircularQueue(n) 
        for _ in range(n):
            add_enemy_team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
            add_enemy_team.lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.all_enemy_teams.append(add_enemy_team)


    def battles_remaining(self) -> bool:
        '''
        checks if theres still battles to be fought
        :complexity: O(n) -> n = length of all_enemy_teams i.e how many enemy teams there are
        '''
        more_battles = False

        for _ in range(len(self.all_enemy_teams)):
            check_enemy_team = self.all_enemy_teams.serve()
            if check_enemy_team.lives > 0 :
                more_battles = True
                # break
            self.all_enemy_teams.append(check_enemy_team) # add em back

        if self.teamPlayer.lives <= 0:
            more_battles = False

        return more_battles

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """
        Initiates the next battle against the next team that has more than 0 lives

        :complexity: O(n) -> Amount of enemy teams created
        """

        for _ in range(len(self.all_enemy_teams)):
            team_toFight = self.all_enemy_teams.serve()
            self.all_enemy_teams.append(team_toFight)
            if team_toFight.lives>0:
                break
        
        result_of_battle = Battle().battle(team_toFight, self.teamPlayer,)

        if (result_of_battle == Battle.Result.TEAM1): # if team1 wins i.e enemy - the players loses a life
            self.teamPlayer.lives = self.teamPlayer.lives - 1

        elif (result_of_battle == Battle.Result.TEAM2): ## if team2 wins i.e player - the enemy team loses a life
            team_toFight.lives = team_toFight.lives - 1

        elif (result_of_battle == Battle.Result.DRAW): #both lose a life
            team_toFight.lives = team_toFight.lives - 1
            self.teamPlayer.lives = self.teamPlayer.lives - 1
        
        self.__store_encountered_elements(team_toFight)
        self.teamPlayer.regenerate_team()
        team_toFight.regenerate_team() #reset them back to og team so they can fight next time
        
        return (result, self.teamPlayer.team, team_toFight.team, self.teamPlayer.lives, team_toFight.lives)

    def __store_encountered_elements(self, team : MonsterTeam):
        """
        adds monster elements to a list that stores previously encountered monsters

        :complexity: O(n) -> n = length of team inputted
        :team: team you want to check elements of monsters for and add to list of encountered_elements
        """
        for _ in range(len(team.team)):
            monster = team.retrieve_from_team() #get monster
            monster_element = Element.from_string(monster.get_element()) # get element
            self.encountered_elements.append(monster_element.value)# add monster element to encountered elements array
            team.add_to_team(monster) #(O(1) as its always a Queue so append is constant add) add monster back to team

    def out_of_meta(self) -> ArrayR[Element]:
        pass

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)
