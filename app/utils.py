import json

def dict_list_to_json(struct, filename):
    try:
        json_str = json.dumps(struct, ensure_ascii=False)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json_str)
        return json_str
    except (Exception) as e:
        print(f"Error: {e}")
        return None
    
def json_to_dict_list(filename):
    try:
        with open(filename, "r") as file:
            json_str = file.read()
            dict_list = json.loads(json_str)
        return dict_list
    except Exception as e:
        print(f"Error: {e}")
        return None