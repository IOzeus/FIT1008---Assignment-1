
current_hp = 0.5

x = float.as_integer_ratio(current_hp)
get_name = "monster"
current_level = 1
statement = f"LV.{current_level} {get_name}, {x[0]}/{x[1]} HP"

def str():
    return statement

print(str())

