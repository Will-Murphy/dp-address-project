class AddressService (): 
    """ 
    Abstract Class to standardize third party service specific 
    implementation of the dp-address-project specifications. 
    
    If a method is not provided by a particular service implmentation 
    and is called the method will raise an error.
    """

    def load_config(self, config_file, usage):
        """Resonsible for loading configs & setting up client"""
        raise NotImplementedError(f'{type(self).__name__} ' \
                                   'has not implemented this method')

    def send_request(self, params:dict,  data):
        """Responsible for sending request to service"""
        raise NotImplementedError(f'{type(self).__name__} ' \
                                   'has not implemented this method')

    def validate(self, params:dict, data ):
        """ 
        Reponsible for validating input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input 
        and multiple for batch input.
        """
        raise NotImplementedError(f'{type(self).__name__} ' \
                                   'has not implemented this method')
    
    def forward_geocode(self, params:dict, data):
        """ 
        Reponsible for forward geocoding input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input 
        and multiple for batch input.
        """
        raise NotImplementedError(f'{type(self).__name__} ' \
                                   'has not implemented this method')

    def reverse_geocode(self, params:dict, data):
        """ 
        Reponsible for reverse geocoding input addresses in stream or batch form.
        
        returns a list containing a single Address object for stream input 
        and multiple for batch input.
        """
        raise NotImplementedError(f'{type(self).__name__} ' \
                                   'has not implemented this method')
    