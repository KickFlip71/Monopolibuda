import json
from random import randint

if __name__ == '__main__':

    chance_names = ['DZIEKANKA', 'POWToRKA Z BAZ DANYCH', 'HURTOWNIE CO SEMESTR', 'KLIKANIE ACCESSA', 'RANDOM OCENA']

    starting_value = 150
    value_step_change = 200

    data = []
    pk = 0
    for i in range(10):
      for ii, description in enumerate(chance_names):
        entry = {}
        entry['model'] = 'game.chance'
        entry['pk'] = pk + 1
        pk = pk + 1
        value = starting_value + i*value_step_change * randint(1,4)
        negative = randint(0,1)
        if negative == 0:
            value = value * (-1)
        fields = {}
        fields['description'] = description
        fields['value'] = value
        entry['fields'] = fields
        data.append(entry)

    with open('chance.json', 'w') as outfile:
        json.dump(data, outfile)
