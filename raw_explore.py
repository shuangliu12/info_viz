import json
import time

start_time = time.time()
file_name = "data/Kickstarter_2018-01-12T10_20_09_196Z.json"
# file_name = "data/Kickstarter_2018-01-12T10_20_09_196Z-tiny.json"

country_count = {}
currency_count = {}
current_currency_count = {}
state_count = {}
photo_count = {}
is_registered_count = 0
with open(file_name, "r") as f:
  
  for cnt, line in enumerate(f):
    project = json.loads(line)

    # if project['data']['staff_pick']:
    #   print(cnt)
    #   print(project['data']['state'])
    #   print(project['data']['urls']['web']['project'])
    #   break

    country = project['data']['country']
    currency = project['data']['currency']
    current_currency = project['data']['current_currency']
    state = project['data']['state']
    num_photos = len(project['data']['photo'])
    is_registered = project['data']['creator']['is_registered']

    country_count[country] = country_count.get(country, 0) + 1
    currency_count[currency] = currency_count.get(currency, 0) + 1
    current_currency_count[current_currency] = current_currency_count.get(current_currency, 0) + 1
    if country == 'US' and currency == 'USD' and current_currency == 'USD':
      state_count[state] = state_count.get(state, 0) + 1
    photo_count[num_photos] = photo_count.get(num_photos, 0) + 1
    if is_registered:
      is_registered_count += 1
    # print(state, project['data']['pledged'], project['data']['goal'])



def print_dict(count_dict, column):
  print(column)
  keys = sorted(count_dict.keys())
  for key in keys:
    print(key, count_dict[key])
  print('')

print_dict(country_count, 'country')
print_dict(currency_count, 'currency')
print_dict(current_currency_count, 'current_currency')
print_dict(state_count, 'state')
print_dict(photo_count, 'num_photos')
print("creator_is_registered {}".format(is_registered_count))




print("Took {} seconds".format(time.time() - start_time))