def src_ip_addresses():
   src_ip_addresses = ['10.3.3.211', '10.3.3.119', '10.3.3.14'] 
   return src_ip_addresses 

def dst_ip_addresses():
   dst_ip_addresses = ['192.168.100.2', '192.168.100.5', '192.168.100.101', '192.168.100.240', '192.168.100.202'] 
   return dst_ip_addresses 

def src_dst_passed():
   src_dst_passed = [['Администраторы Linux', [['ex1105', '172.16.200.15', 'none'], ['ex0105', '172.16.200.230', 'none'], ['ex0105', '172.16.200.128', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '443'], ['TCP', 443]], 'TCP\nHTTPS', 'Тестовый комментарий третий']] 
   return src_dst_passed 

def access_role_list():
   access_role_list = ['none_10.3.3.211_24', 'none_10.3.3.119_24', 'none_10.3.3.14_24'] 
   return access_role_list