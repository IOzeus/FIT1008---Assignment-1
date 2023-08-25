from __future__ import annotations

from enum import auto
from typing import Optional

from base_enum import BaseEnum

from data_structures.referential_array import ArrayR

class Element(BaseEnum):
    """
    Element Class to store all different elements as constants, and associate indicies with them.

    Example:
    ```
    print(Element.FIRE.value)         # 1
    print(Element.GRASS.value)        # 3

    print(Element.from_string("Ice")) # Element.ICE
    ```
    """

    FIRE = auto()
    WATER = auto()
    GRASS = auto()
    BUG = auto()
    DRAGON = auto()
    ELECTRIC = auto()
    FIGHTING = auto()
    FLYING = auto()
    GHOST = auto()
    GROUND = auto()
    ICE = auto()
    NORMAL = auto()
    POISON = auto()
    PSYCHIC = auto()
    ROCK = auto()
    FAIRY = auto()
    DARK = auto()
    STEEL = auto()

    '''Class method from_string takes a string as input and returns an instance of the 
Element class based on a case-insensitive comparison of the input string with the names of the elements.'''
    @classmethod
    def from_string(cls, string: str) -> Element:
        for elem in Element:
            if elem.name.lower() == string.lower():
                return elem
        raise ValueError(f"Unexpected string {string}")

class EffectivenessCalculator:
    """
    Helper class for calculating the element effectiveness for two elements.

    This class follows the singleton pattern.

    Usage:
        EffectivenessCalculator.get_effectiveness(elem1, elem2)
    """

    instance: Optional[EffectivenessCalculator] = None

    def __init__(self, element_names: ArrayR[str], effectiveness_values: ArrayR[float]) -> None:
        """

        :complexity: O(1)
        Initialise the Effectiveness Calculator.

        The first parameter is an ArrayR of size n containing all element_names.
        The second parameter is an ArrayR of size n*n, containing all effectiveness values.
            The first n values in the array is the effectiveness of the first element
            against all other elements, in the same order as element_names.
            The next n values is the same, but the effectiveness of the second element, and so on.

        Example:
        element_names - ['Fire', 'Water', 'Grass']
        effectivness_values: [0.5, 0.5, 2, 2, 0.5, 0.5, 0.5, 2, 0.5]
        Fire is half effective to Fire and Water, and double effective to Grass [0.5, 0.5, 2]
        Water is double effective to Fire, and half effective to Water and Grass [2, 0.5, 0.5]
        Grass is half effective to Fire and Grass, and double effective to Water [0.5, 2, 0.5]

        :element_names: ArrayR of size n containing all element_names
        :effectiveness_values: ArrayR of size n*n, containing all effectiveness values
        """
        self.elements = element_names
        self.effectiveness = effectiveness_values

    @classmethod
    def get_effectiveness(cls, type1: Element, type2: Element) -> float:
        """
        :complexity: O(n) -> n = length of elements array 
        :type1: Element of monster attacking
        :type2: Element of monster attacked

        Returns the effectiveness of elem1 attacking elem2.

        Example: EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER) == 0.5
        """

        elements = cls.instance.elements # assign elements array to elements variable from singleton instance
        effectiveness = cls.instance.effectiveness # assign effectivenesss array to elements variable from singleton instance

        type1 = type1.name.lower() #turn first element string to lower case
        type2 = type2.name.lower() #turn second element string to lower case
        elements_lowercase_array = ArrayR.from_list([elem.lower() for elem in elements]) # O(n)Create array of element headers all in lowercase

        if type1 in elements_lowercase_array: #O(n) check if the first element exists in the new lowercase array ex. water == water? 
                index_type1 = elements_lowercase_array.index(type1) #get index value of the first element

                if type2 in elements_lowercase_array: #O(n) check if the second element exists in the new lowercase array ex. water == water?
                    index_type2 = elements_lowercase_array.index(type2) #get index value of the second element

        else: #raise Exception if first element or second element is not found
            raise Exception("Please enter valid Elements")

        index = index_type1 * len(elements) + index_type2 #calculate index where the corresponding effectiveness value is

        effectiveness_value = effectiveness[index] #get the value from the effectiveness_value array which contains all effectiveness values

        return effectiveness_value

        # for element in elements_lowercase_array:
        #     if type1 == element.lower():
        #         index_type1 = elements.index(type1)

        #     if type2 == element.lower():
        #         index_type2 = elements.index(type2)

    @classmethod
    def from_csv(cls, csv_file: str) -> EffectivenessCalculator:
        # NOTE: This is a terrible way to open csv files, if writing your own code use the `csv` module.
        # This is done this way to facilitate the second half of the task, the __init__ definition.
        with open(csv_file, "r") as file:
            header, rest = file.read().strip().split("\n", maxsplit=1)
            header = header.split(",")
            rest = rest.replace("\n", ",").split(",")
            a_header = ArrayR(len(header))
            a_all = ArrayR(len(rest))
            for i in range(len(header)):
                a_header[i] = header[i]
            for i in range(len(rest)):
                a_all[i] = float(rest[i])
            return EffectivenessCalculator(a_header, a_all)

    @classmethod
    def make_singleton(cls):
        cls.instance = EffectivenessCalculator.from_csv("type_effectiveness.csv")

EffectivenessCalculator.make_singleton()


if __name__ == "__main__":
    print(EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER))
    print(EffectivenessCalculator.instance.elements)
    print(EffectivenessCalculator.instance.effectiveness)
