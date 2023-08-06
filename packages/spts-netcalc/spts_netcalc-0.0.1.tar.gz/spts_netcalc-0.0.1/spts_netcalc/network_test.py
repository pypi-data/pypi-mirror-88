import unittest
from network import Network

class TestNetwork(unittest.TestCase):
    
    def test_calculate_net_address(self):
        self.assertEqual(Network.calculate_net_address('177.16.174.1', '255.255.255.252'), '177.16.174.0')
        self.assertEqual(Network.calculate_net_address('10.213.37.2', '255.255.224.0'), '10.213.32.0')
        self.assertEqual(Network.calculate_net_address('172.17.221.102', '255.255.255.248'), '172.17.221.96')
        self.assertEqual(Network.calculate_net_address('172.26.0.15', '255.255.255.128'), '172.26.0.0')
        self.assertEqual(Network.calculate_net_address('10.11.143.96', '255.255.255.192'), '10.11.143.64')
        self.assertEqual(Network.calculate_net_address('192.168.78.138', '255.255.255.192'), '192.168.78.128')
        
        
    def test_calculate_net_broadcast(self):
        self.assertEqual(Network.calculate_net_broadcast('177.16.174.1', '255.255.255.252'), '177.16.174.3')
        self.assertEqual(Network.calculate_net_broadcast('10.213.37.2', '255.255.224.0'), '10.213.63.255')
        self.assertEqual(Network.calculate_net_broadcast('172.17.221.102', '255.255.255.248'), '172.17.221.103')
        self.assertEqual(Network.calculate_net_broadcast('172.26.0.15', '255.255.255.128'), '172.26.0.127')
        self.assertEqual(Network.calculate_net_broadcast('10.11.143.96', '255.255.255.192'), '10.11.143.127')
        self.assertEqual(Network.calculate_net_broadcast('192.168.78.138', '255.255.255.192'), '192.168.78.191')
        
        
    def test_calculate_host_addresses(self):
        self.assertEqual(Network.calculate_host_addresses('177.16.174.0', '255.255.255.252')[0], '177.16.174.1')
        self.assertEqual(Network.calculate_host_addresses('177.16.174.0', '255.255.255.252')[-1], '177.16.174.2')
        self.assertEqual(Network.calculate_host_addresses('10.213.32.0', '255.255.224.0')[0], '10.213.32.1')
        self.assertEqual(Network.calculate_host_addresses('10.213.32.0', '255.255.224.0')[-1], '10.213.63.254')
        self.assertEqual(Network.calculate_host_addresses('172.17.221.96', '255.255.255.248')[0], '172.17.221.97')
        self.assertEqual(Network.calculate_host_addresses('172.17.221.96', '255.255.255.248')[-1], '172.17.221.102')
        self.assertEqual(Network.calculate_host_addresses('172.26.0.0', '255.255.255.128')[0], '172.26.0.1')
        self.assertEqual(Network.calculate_host_addresses('172.26.0.0', '255.255.255.128')[-1], '172.26.0.126')
        self.assertEqual(Network.calculate_host_addresses('10.11.143.64', '255.255.255.192')[0], '10.11.143.65')
        self.assertEqual(Network.calculate_host_addresses('10.11.143.64', '255.255.255.192')[-1], '10.11.143.126')
        self.assertEqual(Network.calculate_host_addresses('192.168.78.128', '255.255.255.192')[0], '192.168.78.129')
        self.assertEqual(Network.calculate_host_addresses('192.168.78.128', '255.255.255.192')[-1], '192.168.78.190')
        
        
    def test_calculate_class(self):
        self.assertEqual(Network.calculate_class('177.16.174.1'), 'B')
        self.assertEqual(Network.calculate_class('10.213.37.2'), 'A')
        self.assertEqual(Network.calculate_class('192.240.1.2'), 'C')
        self.assertEqual(Network.calculate_class('225.245.1.9'), 'D (multicast)')
        self.assertEqual(Network.calculate_class('242.7.93.124'), 'E (reserved)')
        
        
    def test_calculate_cidr_mask(self):
        self.assertEqual(Network.calculate_cidr_mask('224.0.0.0'), 3)
        self.assertEqual(Network.calculate_cidr_mask('255.240.0.0'), 12)
        self.assertEqual(Network.calculate_cidr_mask('255.255.224.0'), 19)
        self.assertEqual(Network.calculate_cidr_mask('255.255.255.192'), 26)
        self.assertEqual(Network.calculate_cidr_mask('255.255.255.252'), 30)
        
    def test_calculate_dot_decimal_mask(self):
        self.assertEqual(Network.calculate_dot_decimal_mask(1), '128.0.0.0')
        self.assertEqual(Network.calculate_dot_decimal_mask(11), '255.224.0.0')
        self.assertEqual(Network.calculate_dot_decimal_mask(17), '255.255.128.0')
        self.assertEqual(Network.calculate_dot_decimal_mask(29), '255.255.255.248')
        self.assertEqual(Network.calculate_dot_decimal_mask(31), '255.255.255.254')
        
        
    def test_calculate_wildcard_mask(self):
        self.assertEqual(Network.calculate_wildcard_mask('255.255.255.252'), '0.0.0.3')
        self.assertEqual(Network.calculate_wildcard_mask('128.0.0.0'), '127.255.255.255')
        self.assertEqual(Network.calculate_wildcard_mask('255.224.0.0'), '0.31.255.255')
        self.assertEqual(Network.calculate_wildcard_mask('255.255.128.0'), '0.0.127.255')
        self.assertEqual(Network.calculate_wildcard_mask('255.255.255.248'), '0.0.0.7')
        self.assertEqual(Network.calculate_wildcard_mask('255.255.255.254'), '0.0.0.1')
        
    def test_is_mask_valid(self):
        self.assertTrue(Network.is_mask_valid('255.255.255.252'))
        self.assertTrue(Network.is_mask_valid('128.0.0.0'))
        self.assertTrue(Network.is_mask_valid('255.224.0.0'))
        self.assertTrue(Network.is_mask_valid('255.255.128.0'))
        self.assertFalse(Network.is_mask_valid('255.255.230.252'))
        self.assertFalse(Network.is_mask_valid('12.0.0.0'))
        self.assertFalse(Network.is_mask_valid('255.242.0.0'))
        self.assertFalse(Network.is_mask_valid('251.255.255.252'))
        self.assertFalse(Network.is_mask_valid('251.25.5.255.252'))
        self.assertFalse(Network.is_mask_valid('251.255.255'))
        
        
    def test_is_address_valid(self):
        self.assertTrue(Network.is_address_valid('177.16.174.1'))
        self.assertTrue(Network.is_address_valid('10.36.13.159'))
        self.assertTrue(Network.is_address_valid('226.1.123.2'))
        self.assertTrue(Network.is_address_valid('192.168.13.2'))
        self.assertFalse(Network.is_address_valid('177.260.174.1'))
        self.assertFalse(Network.is_address_valid('300.16.174.1'))
        self.assertFalse(Network.is_address_valid('-1.16.174.1'))
        self.assertFalse(Network.is_address_valid('177.16.174.319'))
        self.assertFalse(Network.is_address_valid('1.16.1.74.1'))
        self.assertFalse(Network.is_address_valid('177.16.174'))
        
        
    def test_convert_to_int(self):
        self.assertEqual(Network.convert_to_int('177.16.174.1'), 2970660353)
        self.assertEqual(Network.convert_to_int('10.213.37.2'), 181740802)
        self.assertEqual(Network.convert_to_int('172.17.221.102'), 2886851942)
        self.assertEqual(Network.convert_to_int('172.26.0.15'), 2887385103)
        self.assertEqual(Network.convert_to_int('10.11.143.96'), 168529760)
        self.assertEqual(Network.convert_to_int('192.168.78.138'), 3232255626)
                        
    def test_convert_to_string(self):
        self.assertEqual(Network.convert_to_string(2970660353), '177.16.174.1')
        self.assertEqual(Network.convert_to_string(181740802), '10.213.37.2')
        self.assertEqual(Network.convert_to_string(2886851942), '172.17.221.102')
        self.assertEqual(Network.convert_to_string(2887385103), '172.26.0.15')
        self.assertEqual(Network.convert_to_string(168529760), '10.11.143.96')
        self.assertEqual(Network.convert_to_string(3232255626), '192.168.78.138')
        
    def test_split_to_octets(self):
        self.assertEqual(Network.split_to_octets('177.16.174.1'), [177, 16, 174, 1])
        self.assertEqual(Network.split_to_octets('10.213.37.2'), [10, 213, 37, 2])
        self.assertEqual(Network.split_to_octets('172.17.221.102'), [172, 17, 221, 102])
        self.assertEqual(Network.split_to_octets('172.26.0.15'), [172, 26, 0, 15])
        self.assertEqual(Network.split_to_octets('10.11.143.96'), [10, 11, 143, 96])
        self.assertEqual(Network.split_to_octets('192.168.78.138'), [192, 168, 78, 138])
        
        
if __name__ == '__main__':
    unittest.main()

     