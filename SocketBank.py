#!/usr/bin/env python

def boss(q_to_bank, q_back_bank):
    
    # SOCKETBANK [[[name], [client_socket], [process_id]], [...]]
    SOCKETBANK = []
    
    while True:
        
        if not q_to_bank.empty():
            
            data = q_to_bank.get()
            
            if data[0][0] == 'UPDATE':
                
                # message send to staff [[command], [name], [client_socket], [process_id]]
                new_message = []
                
                new_message.append(data[1])
                
                new_message.append(data[2])
                
                new_message.append(data[3])
                
                SOCKETBANK.append(new_message)
                
            if data[0][0] == 'GET ALL THE ONLINE USERS':
                # message like [['GET ALL THE ONLINE USERS'], [process_id]]
                
                back_all = []
                
                back_all.append(['ALL'])
                
                back_all.append(data[1])
                
                name_list = []
                
                for lines in SOCKETBANK:
                    
                    name_list.append(lines[0])
                    
                back_all.append(name_list)
                
                # back message [[ALL], [process_id], [name_list]]
                q_back_bank.put(back_all)
                
            if data[0][0] == 'GET FRIEND':
                
                # message like [['GET FRIEND'], [process_id], [friend_list]]
                want_name_list = data[2][0]
                    
                want_list = []
                
                want_list.append(['RETURN QUERY RESULT'])
                
                want_list.append(data[1])
                
                # SOCKETBANK [[[name], [client_socket], [process_id]], [...]]
                for want_name in want_name_list:
                    
                    for lines_name in SOCKETBANK:
                        
                        if want_name == lines_name[0][0]:
                            
                            small_list = []
                            
                            small_list.append(want_name)
                            
                            small_list.append(lines_name[1])
                            
                        want_list.append(lines_name[1])
                            
                # back message [[RETURN QUERY RESULT], [process_id], [[name, socket]]]
                q_back_bank.put(want_list)
