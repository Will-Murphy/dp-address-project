class Address ():
    """Class represents data structure for address objects"""
    def __init__(self):
        self.input_string = None
        self.line_1 = None 
        self.line_2 = None 
        self.latitude = None
        self.longitude = None 
        self.is_valid = None 
    
    def get_formatted_address_string(self):
        if self.line_1 is None and self.line_2 is None:
            return None 
        elif self.line_2 is None: 
            return str(self.line_1)
        elif self.line_1 is None: 
            return str(self.line_2)
        else:
            return f'{str(self.line_1)}, {str(self.line_2)}'