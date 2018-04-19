import json

if __name__ == '__main__':

    building_names = ['B5', 'B4', 'E5', 'E1', 'C16', 'C1', 'C5', 'C7', 'D1', 'D2', 'C4', 'C3', 'C8', 'C13', 'A2', 'A1']

    starting_building_price = 500
    building_price_step_change = 500

    deposit_rates = 0.5

    starting_apartment_price = 500
    apartment_price_step_change = 250
    hotel_to_apartment_ratio_cost = 5

    data = []
    for i, name in enumerate(building_names):
        entry = {}
        entry['model'] = 'game.charge'
        entry['pk'] = i + 1
        cost = starting_building_price + (int(i / 2) * building_price_step_change)
        fields = {}
        fields['zero_apartments'] = int(cost * 0.1)
        fields['one_apartments'] = int(cost * 0.5)
        fields['two_apartments'] = int(cost * 1.5)
        fields['three_apartments'] = int(cost * 3)
        fields['four_apartments'] = int(cost * 3.5)
        fields['five_apartments'] = int(cost * 4)
        entry['fields'] = fields
        data.append(entry)

        apartment_cost = starting_apartment_price + (int(i / 2) * apartment_price_step_change)
        entry = {}
        entry['model'] = 'game.card'
        entry['pk'] = i + 1
        fields = {}
        fields['name'] = name
        fields['cost'] = cost
        fields['apartment_cost'] = apartment_cost
        fields['hotel_cost'] = int(hotel_to_apartment_ratio_cost * apartment_cost)
        fields['deposit_value'] = int(deposit_rates * cost)
        fields['charge'] = i + 1
        fields['group_number'] = int(i / 2)
        fields['position'] = i + 1 + int(i / 2)
        entry['fields'] = fields
        data.append(entry)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
