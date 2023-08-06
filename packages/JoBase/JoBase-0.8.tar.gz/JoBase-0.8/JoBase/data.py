import arcade

class Sound:
    def __init__(sound, name: str = 'collect.wav'):
        sound.name = name
        sound.sound = arcade.load_sound(name)
        
    def play(sound):
        arcade.play_sound(sound.sound)
        
    def loop(sound):
        pass

def Write(name: str, *words):
    file = open(str(name), 'w')
    
    for word in words:
        file.write(str(word) + '\n')
        
    file.close()
    
def Read(name: str):
    file = open(str(name), 'r')
    
    read = file.readlines()
    file_list = []
    
    for element in read:
        element = element.strip()
        
        if element.replace('.', '', 1).isdigit():
            element = eval(element)
            
        file_list.append(element)
        
    file.close()
    
    return file_list