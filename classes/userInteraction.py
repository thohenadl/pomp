import numpy as np
import pandas as pd
from const import action_Dimensions

from const import TERMS_FOR_MISSING

class userInteraction:
    """
    A user Interaction (UI) is a set of context parameters, which can have two forms: 
        a) string of context-parameter values
        b) an array of context-parameter titles and context-parameter values

    Attributes
    ----------
    context_fields : str
        A string representing the context-parameter values of the interaction.
    context_Array : array
        An array representing context-parameter values in of the user interaction.
    """
    def __init__(self,context: pd.DataFrame):
        # Array with Context attributes and values
        self.context_Array = context.dropna(axis=1)
        self.drop_columns_with_TermsForMissing()
        # Place Holder
        self.context_fields_str = ""
        self.setContextString()
        # Placeholder for the Parts of manual processes dimension
        self.pompDim = ""
        self.hash = hash(self)

    def drop_columns_with_TermsForMissing(self):
        """
        Drops all columns from a Context Array DataFrame that contain any value from a provided list.
        Drop is conducted inplace, thus no return required.

        Parameters:
            self (User Interaction): The user interaction the method is called on.
        """
        for col in self.context_Array.columns:
            if any(self.context_Array[col].isin(TERMS_FOR_MISSING)):
                self.context_Array.drop(col, axis=1, inplace=True)

    def setContextString(self):
        row_str = ', '.join(str(val) for val in self.context_Array.iloc[0])
        self.context_fields_str = row_str

    def equals(self, other):
        """
        Checks whether this UserInteraction instance is equal to another instance.

        Args:
            other (UserInteraction): The other UserInteraction instance to compare against.

        Returns:
            bool: True if this instance is equal to the other instance, False otherwise.
        """
        # print("Context Fields string equals:" + str(self.context_fields_str == other.context_fields_str))
        # print("Context Array equals:" + str(np.array_equal(self.context_Array, other.context_Array)))
        return self.context_fields_str == other.context_fields_str and np.array_equal(self.context_Array, other.context_Array, equal_nan=True)

    def __eq__(self, other: object) -> bool:
        """
        Checks whether this UserInteraction instance is equal to another instance.

        Args:
            other (UserInteraction): The other UserInteraction instance to compare against.

        Returns:
            bool: True if this instance is equal to the other instance, False otherwise.
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        
        return self.context_fields_str == other.context_fields_str and np.array_equal(self.context_Array, other.context_Array)
    
    def __hash__(self):
        # As suggested in https://stackoverflow.com/questions/10254594/what-makes-a-user-defined-class-unhashable
        """
        Hash method returns the hash of the user interaction object.

        Returns:
            Hash of context_Array content
        """
        return hash(self.context_fields_str)
    
    def __iter__(self):
        # As suggested in https://stackoverflow.com/questions/5434400/python-make-class-iterable
        for each in self.__dict__.values():
            yield each

    def get_attribute(self, attr_name):
        """
        Gets the value of the specified attribute of this UserInteraction instance.

        Args:
            attr_name (str): The name of the attribute to get the value of.

        Returns:
            Any: The value of the specified attribute.
        """
        return getattr(self, attr_name)

    def set_attribute(self, attr_name: str, attr_value: any):
        """
        Sets the value of the specified attribute of this UserInteraction instance.

        Args:
            attr_name (str): The name of the attribute to set the value of.
            attr_value (Any): The value to set the attribute to.
        """
        if attr_name == "pompDim" and str(attr_value) not in action_Dimensions:
            raise ValueError(f"POMP dimension must be one of {action_Dimensions}.")
        setattr(self, attr_name, attr_value)

    def delete_attribute(self, attr_name):
        """
        Deletes the specified attribute of this UserInteraction instance.

        Args:
            attr_name (str): The name of the attribute to delete.
        """
        delattr(self, attr_name)

    def __str__(self):
        """ 
        String method to get the User Interaction element.

        Returns:
            String description
        """
        str_len = str(self.context_Array.size)
        return_str = "User Interaction with " + str_len + " context elements."
        return return_str
    
    def __repr__(self):
        """ 
        Representation method to get the User Interaction element.

        Returns:
            String description
        """
        str_len = str(self.context_Array.size)
        return_str = "User Interaction with " + str_len + " context elements."
        return return_str