class Settings:
    """
    The Settings class offer a convenient method to child class to attribute
    values from a dictionary to the class variables for which name and key match
    """

    def setProperties(self, settings: dict):
        """
        set variable value with dictionary value if the key is the same than the variable name
        ---
        Parameters:
        -settings: dictionary with keys possible equivalent to variable names 
        and values = values to set in variables
        """
        if not settings:
            return
        for key in settings:
            if hasattr(self, key):
                setattr(self, key, settings[key])
