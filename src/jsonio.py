import json


def write(file, data):
    assert isinstance(data, dict) or isinstance(data, list), "Input data should be of type dict or list"
    
    with open(file, "w") as fp:
        json.dump(data, fp, indent=4, sort_keys=True)
        
        
def read(file):
    try:
        with open(file, "r") as fp:
            data = json.load(fp)
            return data

    except FileNotFoundError:
        print(f"the file: '{file}' does not exist")
        return None
        
    except Exception as e:
        print(e)

def test():
    _ = read("test_none.json")
    # dict
    d = {
        "a": "AAAA",
        "bert": 1234,
        "date": "2022-04-01"
        } 
    write("test_dict.json", d)
    data_d = read("test_dict.json")
    print(data_d)
    
    # list
    l = [1,23,4] 
    write("test_list.json", l)
    data_l = read("test_list.json")
    print(data_l)
    
    # combined
    d1 = {"a": "aaa", "p": "/a/b/c", "d": "2022-04-01"}
    d2 = {"a": "bbb", "p": "/a/b/b", "d": "2022-04-02"}
    c = [d1, d2]
    write("test_combined.json", c)
    data_c = read("test_combined.json")
    print(data_c)
    
    # double dict
    d1 = {"p": "/a/b/c", "d": "2022-04-01"}
    d2 = {"p": "/a/b/b", "d": "2022-04-02"}
    dd = {"a": d1, "b": d2}
    write("test_double_dict.json", dd)
    data_dd = read("test_double_dict.json")
    print(data_dd)
    
    # tuple
    t = (1.2, 7.8) 
    write("test_tuple.json", t)

if __name__ == "__main__":
    test()