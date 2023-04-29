class LoadKG:
    
    def __init__(self, data_path):
        
        #read in variables
        self.data_path = data_path
    
    def load_train_data(self):
    
        ####load the train, valid and test set##########
        with open (self.data_path, 'r') as f:
            
            data_ini = f.readlines()
            
            data_ = set({})
            
            for i in range(len(data_ini)):
            
                x = data_ini[i].split()
                
                x_ = tuple(x)
                
                data_.add(x_)
            
            del(data_ini)
        
        ####relation dict#################
        index = 0
        
        relation_dict = {}
        
        inverse_relation_dict = {}
        
        for key in data_:
            
            if key[1] not in relation_dict:
                
                relation_dict.update({key[1]:index})
                
                inverse_relation_dict.update({index:key[1]})
                
                index += 1
        
        #we exclude the inverse relations for counting the number of relations
        num_r = len(relation_dict)
        
        #add in the inverse relation
        for i in range(num_r):
            
            relation_ = inverse_relation_dict.get(i)
            
            iv_r_ = '_inverse' + relation_
            
            relation_dict.update({iv_r_:index})
            
            inverse_relation_dict.update({index:iv_r_})
            
            index += 1
        
        #get the id of the inverse relation
        def inverse_r(r):
            
            if r < num_r:
                
                iv_r = r + num_r
            
            else:
                
                iv_r = r - num_r
            
            return(iv_r)
        
        ####entity dict###################
        index = 0
        
        entity_dict = {}
        
        inverse_entity_dict = {}
        
        for key in data_:
            
            if key[0] not in entity_dict:
                
                entity_dict.update({key[0]:index})
                
                inverse_entity_dict.update({index:key[0]})
                
                index += 1
            
            if key[2] not in entity_dict:
                
                entity_dict.update({key[2]:index})
                
                inverse_entity_dict.update({index:key[2]})
                
                index += 1
                
        #create the set of triples using id instead of string
        data = set({})
        
        for key in data_:
            
            s = entity_dict[key[0]]
            
            r = relation_dict[key[1]]
            
            t = entity_dict[key[2]]
            
            if (s,r,t) not in data:
                
                data.add((s,r,t))
        
        one_hop = {} #one-hop neighbourhood
        
        #build the one_hop set. Only one_hop directly comes from triples
        for ele in data:
            
            s,r,t = ele[0],ele[1],ele[2]
            
            if s not in one_hop:
                
                one_hop[s] = dict()
            
            if r not in one_hop[s]:
                
                one_hop[s][r] = set()
            
            one_hop[s][r].add(t)
            
            if t not in one_hop:
                
                one_hop[t] = dict()
            
            r_inv = inverse_r(r)
            
            if r_inv not in one_hop[t]:
                
                one_hop[t][r_inv] = set()
            
            one_hop[t][r_inv].add(s)
        
        return(one_hop, data, entity_dict, inverse_entity_dict,
                     relation_dict, inverse_relation_dict)


if __name__ == "__main__":
    
    print("!!! Kill the process if you see this when running the whole model !!!")
    
    Class = LoadKG('../train.txt')

    one_hop, data, entity_dict, inverse_entity_dict, relation_dict, inverse_relation_dict = Class.load_train_data()








