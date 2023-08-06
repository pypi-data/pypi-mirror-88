class Network:
    """ Class to calculate all parameters of a network given an address and network mask
        Variables:
            net_address: str, the network address
            mask: str, network mask
            broadcast: str, network broadcast address
            host_addresses: list, a list of all addresses on the network that can be assigned to a hosts
            host_number: int, the number of host address available given a network address and mask
            net_class: str, the class of the network
            cidr_mask: int, the network mask in CIDR format
            wildcard_mask: str, the equivalent wildcard of the network mask
        Methods:
            calculate_net_address(): calculates the network address based on any address and mask given
            calculate_net_broadcast(): calculates the network broadcast address based on any address and mask given
            calculate_host_addresses(): returns all addresses of a network given the network address and a mask
            calculate_class(): returns the class of the network
            calculate_cidr_mask(): calculates the network mask in CIDR format given a dot-decimal format mask
            calculate_dot_decimal_mask(): returns the network mask in dot-decimal format given a CIDR mask
            calculate_wildcard_mask(): returns the wildcard equivalent of the network mask
            is_mask_valid(): verifies if the given network mask is valid
            is_address_valid(): verifies if the network address is valid
            convert_to_int(): converts a network address or mask in an int number
            convert_to_string(): converts a netwirk address or mask from it to dot-decimal string format 
            split_to_octets(): split a network address or mask in dot-decimal format in a list of octets in int format
            
    """
    
    def __init__(self, address, mask):
        """ Contructor of Network class
            Stores data of the network
            Arguments:
                address: str, any IPv4 address in a valid format
                mask: str, an IPv4 network mask in a valid format
            Return:
                None
        """
        self.net_address = self.calculate_net_address(address, mask)
        self.mask = mask
        self.broadcast = self.calculate_net_broadcast(address, mask)
        self.host_addresses = self.calculate_host_addresses(self.net_address, mask)
        self.host_number = len(self.host_addresses)
        self.net_class = self.calculate_class(address)
        self.cidr_mask = self.calculate_cidr_mask(mask)
        self.wildcard_mask = self.calculate_wildcard_mask(mask)
        

    def __repr__(self):
        """ Return a printable representation of the Network object
            Arguments:
                None
            Return:
                str, a printable representation of the Network object
        """
        return (f"Network address: {self.net_address}\n" + 
                f"Subnet mask: {self.mask}\n" +
                f"Broadcast address: {self.broadcast}\n" + 
                f"Host addresses: {self.host_addresses[0]} to {self.host_addresses[-1]}\n" +
                f"Number of hosts: {self.host_number}\n" +
                f"Wildcard mask: {self.wildcard_mask}\n" +
                f"CIDR mask: {self.cidr_mask}\n" +
                f"Network class: {self.net_class}")
        
    
    @classmethod
    def calculate_net_address(cls, address, mask):
        """ Calculate the network address, or the first address of the network
            Arguments:
                address: str, any address of the network
                mask: str, the network mask
            Returns:
                str, the network address
        """
        if not cls.is_mask_valid(mask):
            raise Exception("Mask is not valid")
        
        if not cls.is_address_valid(address):
            raise Exception("Address is not valid")
        
        return cls.convert_to_string(cls.convert_to_int(address) & cls.convert_to_int(mask))
        
    
    @classmethod
    def calculate_net_broadcast(cls, address, mask):
        """ Calculate the broadcast address of the network
            Arguments:
                address: str, any address of the network
                mask: str, the network mask
            Return:
                str, the broadcast address of the network
        """
        if not cls.is_mask_valid(mask):
            raise Exception("Mask is not valid")
        
        if not cls.is_address_valid(address):
            raise Exception("Address is not valid")
            
        return cls.convert_to_string(cls.convert_to_int(address) | cls.convert_to_int(cls.calculate_wildcard_mask(mask)))
        
    
    @classmethod
    def calculate_host_addresses(cls, net_address, mask):
        """ Calculate a list of all host address available on a given network
            Arguments:
                net_address: str, the network address
                mask: str, the network mask
            Return:
                list, containing all of the hosts address on the network
        """
        if not cls.calculate_net_address(net_address, mask) == net_address:
            raise Exception("Not a valid network address")
            
        hosts_list = []
        broadcast_address = cls.convert_to_int(cls.calculate_net_broadcast(net_address, mask))
        
        for address in range(cls.convert_to_int(net_address) + 1, broadcast_address):
            hosts_list.append(cls.convert_to_string(address))
            
        return hosts_list
    
    
    @classmethod
    def calculate_class(cls, address):
        """ Calculate the class of the network
            Arguments:
                address: str, the address for which we will calculate the class
            Return:
                str, the class of the network address
        """
        if not cls.is_address_valid(address):
            raise Exception("Address is not valid")
            
        int_address = cls.convert_to_int(address)
        
        if ((int_address >> 31) == 0b0):
            return 'A'
        
        if ((int_address >> 30) == 0b10):
            return 'B'
        
        if ((int_address >> 29) == 0b110):
            return 'C'
        
        if ((int_address >> 28) == 0b1110):
            return 'D (multicast)'
        
        if ((int_address >> 28) == 0b1111):
            return 'E (reserved)'
        
        return 'Failed to calculate class'
    
    
    @classmethod
    def calculate_cidr_mask(cls, mask):
        """ Return the network mask in CIDR format
            Arguments:
                mask: str, the network mask in octets format
            Return:
                int, the network mask in CIDR format
        """
        if not cls.is_mask_valid(mask):
            raise Exception("Mask is not valid")
            
        int_mask = cls.convert_to_int(mask)
        bits = 0
        for i in range(32):
            if int_mask & 0b1 == 0:
                bits += 1
                int_mask = int_mask >> 1
            else:
                break
                
        return 32 - bits
        
        
    @classmethod
    def calculate_dot_decimal_mask(cls, mask):
        """ Calculate the mask in dot-decimal format given a cidr mask
            Arguments:
                mask: int, the mask in cidr format
            Returns:
                str, the mask in dot-decimal format
        """
        int_mask = int(mask)
        
        if int_mask > 32 or int_mask < 0:
            raise Exception("Invalid mask")
        
        bin_mask = (0xffffffff << (32 - int_mask)) & 0xffffffff
        return f"{bin_mask >> 24}.{(bin_mask >> 16) & 0xff}.{(bin_mask >> 8) & 0xff}.{bin_mask & 0xff}"
        
        
    @classmethod
    def calculate_wildcard_mask(cls, mask):
        """ Calculate the equivalent wildcard of the network mask
            Arguments:
                mask: str, the network mask
            Return:
                str, the equivalent wildcard of the network mask
        """
        if not cls.is_mask_valid(mask):
            raise Exception("Mask is not valid")
          
        return cls.convert_to_string(cls.convert_to_int(mask) ^ 0xFFFFFFFF)
    
    
    @classmethod
    def is_mask_valid(cls, mask):
        """ Check if the mask is a valid network mask, i.e, all 1s on the left and all 0s on the right side
            Arguments:
                mask: str, the network mask
            Return:
                bool, the mask is valid or not
        """
        if not cls.is_address_valid(mask):
            return False
        
        int_mask = cls.convert_to_int(mask)
                
        last_is_one = False
        for i in range(32):
            if int_mask & 0b1 == 0 and last_is_one:
                return False
            if int_mask & 0b1 == 1:
                last_is_one = True
        
            int_mask = int_mask >> 1
            
        return True
    
    
    @classmethod
    def is_address_valid(cls, address):
        """ Check if a given network address is a valid IPv4 address, i.e., if it has for octets between 0 and 255
            Arguments:
                address: str, an IPv4 address
            Return:
                bool, is the address valid or not
        """
        octet_list = cls.split_to_octets(address)
        
        if len(octet_list) != 4:
            return False
        if any(octet < 0 or octet > 255 for octet in octet_list):
            return False
        
        return True
    
    
    @classmethod    
    def convert_to_int(cls, address):
        """ Convert a given IP address or network mask to an int
            Arguments:
                address: str, an IP address or network mask
            Return:
                int, the IP address in and int format
        """
        # This method converts the IP address to in the following way:
        # octet0 * (256 ** 3) +
        # octet1 * (256 ** 2) +
        # octet2 * (256 ** 1) +
        # octet3 * (256 ** 0)
        
        octet_list = cls.split_to_octets(address)
        return sum(j * (256 ** i) for i, j in enumerate(reversed(octet_list)))
    
    
    @classmethod
    def convert_to_string(cls, address):
        """ Convert a given IP address or network mask in int format back to a string
            Arguments:
                address: int, the IP address or network mask in int format
            Return:
                str, the IP address in a.b.c.d format
        """
        ip = ''
        for i in range(4):
            ip = str((address >> i * 8) & 0xff) + ip
            if i < 3:
                ip = '.' + ip
        return ip
        
        
    @classmethod
    def split_to_octets(cls, address):
        """ Split a given address or network mask to octets
            Arguments:
                address: str, the IP address or network mask
            Return:
                list of all octets in the address or network mask
        """
        return [int(octet) for octet in address.split('.')]