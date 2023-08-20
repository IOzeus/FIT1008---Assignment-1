from __future__ import annotations
import abc

from stats import Stats
''' This is how to commment everything
what the function does
complexity of overall function 
'''

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        :self.max_hp: Max hp of monster (retrived from stats.py)
        """

        #Stats of monster retrieved from stats.py
        stats = self.get_simple_stats() #just naming a variable i.e self.stats to equal the function get_simple_stats() (which gets all the stats somehow from the stats file) so that I can access this function easier just by writing stats.whatever
        self.__max_hp = stats.get_max_hp()
        self.__defense = stats.get_defense()
        self.__dmg = stats.get_attack()
        self.__speed = stats.get_speed()

        #Inputted values
        self.__init_level = level
        self.__current_level = level
        self.__current_hp = self.get_max_hp()
        self.__is_alive = True
        self.__eff_dmg = None
        

    def get_level(self):
        """The current level of this monster instance"""
        return self.__current_level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        # if other monsters hp<=0 (hp is less than or equal to 0) i.e the variable 'other' obj hp stat is hp<=0 
        # then if this is the case level up (update current_level using current_level+=current_level)
        #return current_level
        old_max_hp = self.get_max_hp()
        self.__current_level += 1
        self.set_hp( self.get_max_hp() - (old_max_hp - self.get_hp()) )
        return self.__current_level

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.__current_hp
        
    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        if val < 0:
            raise ValueError("HP cannot be negative")

        if val > self.__max_hp: 
            hp_increase = val - self.__max_hp
            self.__current_hp = self.__max_hp
            self.__max_hp = val  # Update max HP

        else:
            self.__current_hp = val
        
    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.__dmg

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.__defense

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.__speed

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.__max_hp


    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        if (self.__current_hp <= 0):
            self.__is_alive = False
        else:
            self.__is_alive = True

        return self.__is_alive

        

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP

        raise NotImplementedError

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        if self.get_evolution() == None:
            return False
        
        if (self.__current_level > self.__init_level):
            return True
        
        else:
            return False
    


    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        
        if (self.ready_to_evolve()):
            #if (self.__current_level > self.__init_level):
            evolved_cls = self.get_evolution()
            evolved_monster_obj = evolved_cls.__new__(evolved_cls)
            evolved_monster_obj.__init__(True,self.__current_level)
            #val = evolved_monster_obj.__max_hp - self.__max_hp
             
            hp_increase = evolved_monster_obj.get_max_hp() - self.__max_hp
            new_current_hp = self.__current_hp + hp_increase
            evolved_monster_obj.set_hp(new_current_hp)
            return evolved_monster_obj
        else:
            pass
    
    def __str__(self) -> str:
            return f"LV.{self.get_level()} {self.get_name()}, {self.get_hp()}/{self.get_max_hp()} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
