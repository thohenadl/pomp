import numpy as np

class UserInteraction:
    """
    A user Interaction (UI) is a set of context parameters, which can have two forms: 
        a) string of context-parameter values
        b) an array of context-parameter titles and context-parameter values

    Attributes
    ----------
    context_fields : str
        A string representing the context-parameter values of the interaction.
    data : list
        A list representing context-parameter values in of the user interaction.
    """
    def __init__(self):
        self.contextFields = ""
        self.array = []

    def equals(self, other):
        """
        Checks whether this UserInteraction instance is equal to another instance.

        Args:
            other (UserInteraction): The other UserInteraction instance to compare against.

        Returns:
            bool: True if this instance is equal to the other instance, False otherwise.
        """
        return self.context_fields == other.context_fields and np.array_equal(self.array, other.array)

    def get_attribute(self, attr_name):
        """
        Gets the value of the specified attribute of this UserInteraction instance.

        Args:
            attr_name (str): The name of the attribute to get the value of.

        Returns:
            Any: The value of the specified attribute.
        """
        return getattr(self, attr_name)

    def set_attribute(self, attr_name, attr_value):
        """
        Sets the value of the specified attribute of this UserInteraction instance.

        Args:
            attr_name (str): The name of the attribute to set the value of.
            attr_value (Any): The value to set the attribute to.
        """
        setattr(self, attr_name, attr_value)

    def delete_attribute(self, attr_name):
        """
        Deletes the specified attribute of this UserInteraction instance.

        Args:
            attr_name (str): The name of the attribute to delete.
        """
        delattr(self, attr_name)
