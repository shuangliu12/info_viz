import json
import csv
import time
import sys



start_time = time.time()
file_name = "data/Kickstarter_2018-01-12T10_20_09_196Z"
# file_name = "data/Kickstarter_2018-01-12T10_20_09_196Z-tiny"
max_rows = 2000
shrunk_file_name = file_name + "-shrunk"
if max_rows >= 0:
  shrunk_file_name += str(max_rows) + ".csv"
columns = ["id", "pledged", "goal", "backers_count", "state", "spotlight", "staff_pick", "is_starrable", "disable_communication", "created_at", "launched_at", "state_changed_at", "deadline", ['category', 'id'], ['category', 'name'], ['creator', 'id'], ['location', 'id'], ['location', 'state'], "name", "blurb", "slug"]
columns_with_null = {}
with open(shrunk_file_name, 'wb') as out_file:
  wh = csv.writer(out_file, quoting=csv.QUOTE_NONE)
  row = []
  for column in columns:
    column_name = column
    if type(column) is list:
      column_name = '_'.join(column)
    row.append(column_name)
  wh.writerow(row)

  wr = csv.writer(out_file, quoting=csv.QUOTE_NONNUMERIC)
  with open(file_name + ".json", "r") as f:
    for cnt, line in enumerate(f):
      project = json.loads(line)
      if project['data']['country'] != 'US' or ('location' in project['data'] and project['data']['location']['country'] != 'US') or project['data']['currency'] != 'USD' or project['data']['current_currency'] != 'USD':
        continue

      if cnt == max_rows:
        break

      # if 'location' in project['data'] and project['data']['location']['state'] == 'Shanghai':
      #   print(line)

      row = []
      for column in columns:
        column_name = column
        try:
          if type(column) is list:
            column_name = '_'.join(column)
            row_data = project['data'][column[0]][column[1]]
          else:
            row_data = project['data'][column]

          if type(row_data) is unicode:
            row_data = row_data.encode('utf-8').replace("\n", "")
        except:
          columns_with_null[column_name] = columns_with_null.get(column_name, 0) + 1
          row_data = None
        row.append(row_data)
      wr.writerow(row)

print("Nulls:")
print(columns_with_null)
print("Took {} seconds".format(time.time() - start_time))
