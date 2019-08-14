code_rule = ('base64', 'strict')
def encode_dict(data_dict):
    data_encoded = str(data_dict).encode(code_rule[0], code_rule[1])
    return data_encoded

def decode_dict(data_encoded):
    data_dict = pickle.loads(b64_color.decode('base64', 'strict'))
    data_dict = 




    


