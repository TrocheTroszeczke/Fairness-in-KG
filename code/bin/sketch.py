'''
# mode == True for training, False for Testing
# define multi-layer bidirectional dynamic lstm
def stacked_bidirectional_BasicLSTM(inputs):
    # TODO: add time_major parameter, and using batch_size = tf.shape(inputs)[0], and more assert
    _inputs = inputs
    if len(_inputs.get_shape().as_list()) != 3:
    	raise ValueError("Inputs must be dim 3")

    output_first_layer = None
    for layer in range(num_layers):
        with tf.variable_scope(None, default_name="bidirectional-rnn"):
            rnn_cell_fw = rnn.LSTMCell(num_hidden, use_peepholes=True, initializer= tf.initializers.random_uniform(-init_scale, init_scale), forget_bias=1.0)#fw
            rnn_cell_bw = rnn.LSTMCell(num_hidden, use_peepholes=True, initializer= tf.initializers.random_uniform(-init_scale, init_scale), forget_bias=1.0)#fw
            
            rnn_cell_fw = tf.nn.rnn_cell.DropoutWrapper(rnn_cell_fw, output_keep_prob=keep_prob)
            rnn_cell_bw = tf.nn.rnn_cell.DropoutWrapper(rnn_cell_bw, output_keep_prob=keep_prob)

            output, state = tf.nn.bidirectional_dynamic_rnn(rnn_cell_fw, rnn_cell_bw, _inputs, dtype=tf.float32)
            if layer == 0:            
                output_first_layer = tf.concat(output, 2) 
                _inputs = output_first_layer
            else:
                _inputs = tf.concat(output, 2)
    return output_first_layer, _inputs
'''

'''

for i in range(1, length_bd+1):
    
    res[i] = set()

#build the input and output set for dynamic programming
in_set = self.one_hop[s]
ot_set = dict()

#start the DP process
for i in range(1, length_bd+1):
    
    #to speed up, we record all the end entities of all rels,
    #then build the dict with entities to be key and rels be value
    t_p_rel_dict = dict() #t_p for t prime: t'
    
    for rel in in_set:
        
        for t_p in in_set[rel]: #t_p for t prime: t'
        
            if t_p not in t_p_rel_dict:
                
                t_p_rel_dict[t_p] = {rel}
                
            else:
                
                t_p_rel_dict[t_p].add(rel)
        
    #add to result
    if t in t_p_rel_dict:
        
        for rel_ele in t_p_rel_dict[t]:
            
            res[i].add(rel_ele)
        
    #build output for next round
    for t_p in t_p_rel_dict:
        
        temp = self.one_hop[t_p]
        
        holder = list()
        
        for rel_ele in t_p_rel_dict[t_p]:
            
            if type(rel_ele) == type(1):
                
                temp_l = list()
                temp_l.append(rel_ele)
                
                holder.append(temp_l)
            
            elif type(rel_ele) == type((1,2,3)):
                
                holder.append(list(rel_ele))
                
            else:
                
                raise TypeError("!!! path type is not correct !!!")
                
        for rel_2 in temp:
            
            for rel_ele in holder:
                
                rel_ele.append(rel_2)
                
                new_path = tuple(rel_ele)

                if new_path not in ot_set:
                
                    ot_set[new_path] = set()
                
                for t_dp in temp[rel_2]: #t_dp is for t double prime: t''
                    
                    ot_set[new_path].add(t_dp)

    #complete the DP process
    in_set = ot_set
    ot_set = dict()

'''