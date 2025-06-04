race = "Human"
heght = "1.60"
hair_length = "long, ponytail"
hair_color = "black"
eye_color = "brown"
skin_color = "light"
sex = "She"
classs = "bard"
piercing = "no piercing"
clothes = "All closed bard clothes"
tattoos = "no tatoo"
weapon = "lute"
body_type = "little fat" 
additional_features = "she is 56 years old, europoid"

if sex == "He":
    sex1 = "is Male"
elif sex == "She":
    sex1 = "is Female"
else:
    sex1 = "gender Define whatever you want"

print(f"""You are a Dungeon Master for DnD and you have to draw a new character for your new game.
    race: {race},
    height: {heght}, 
    {sex} is {sex1},
    Hair length: {hair_length},
    Hair color: {hair_color},
    has {eye_color} eyes,    
    skin color: {skin_color},    
    {sex} is {classs},
    clothes: {clothes}
    piercing: {piercing},
    tattoos: {tattoos},
    weapon: {weapon},
    body type: {body_type},
    additional features: {additional_features},
    magazine, statistics, lines pointing to clothing and gear, detailed character from a dark, high epic fantasy, lots of details, graphs --ar 9:16.""") 