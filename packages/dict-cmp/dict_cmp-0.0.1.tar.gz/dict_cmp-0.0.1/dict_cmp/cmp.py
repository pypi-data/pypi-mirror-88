
def cmp_dict(src_data,dst_data):   
    assert type(src_data) == type(dst_data),"type: '{}' != '{}'".format(type(src_data), type(dst_data))
    if isinstance(src_data,dict):
        for key in src_data:                
            assert dst_data.has_key(key)    
            cmp_dict(src_data[key],dst_data[key])    
    elif isinstance(src_data,list):                      
        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
            cmp_dict(src_list, dst_list)
    else:
        assert src_data == dst_data,"value '{}' != '{}'".format(src_data, dst_data)
