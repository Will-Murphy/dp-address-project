"""
Class represents data structure for address objects and provides methods 
for returning strings comprised of address attributes in a standardized format. 
"""
class Address ():
    def __init__(self):
        self.input_string = None
        self.line_1 = None 
        self.line_2 = None 
        self.latitude = None
        self.longitude = None 
        self.is_valid = None 
    
    def get_standardized_string(self):    
        """
        Return correctly formatted address string based on address object 
        attributes. "Standardized" formatting based on user specifications.

        useful only after address is processed and validated.
        """
        if (self.line_1 is None and self.line_2 is None) or \
           (self.is_valid is not True):
            return None      
        elif self.line_2 is None: 
            return str(self.line_1)
        elif self.line_1 is None: 
            return str(self.line_2)
        else:
            return f'{str(self.line_1)}, {str(self.line_2)}'
    
    def get_coordinates_string(self):
        """
        Return coordinate string formatted based on address object
        attributes. 
        """
        if self.latitude is None and self.longitude is None:
            return None 
        else: 
            return f'{str(self.latitude)}, {str(self.longitude)}'
    