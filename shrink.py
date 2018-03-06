import json
import csv
import time
import sys
import random
random.seed(5)


start_time = time.time()
file_name = "Kickstarter_2018-01-12T10_20_09_196Z"
# file_name = "Kickstarter_2018-01-12T10_20_09_196Z-tiny"
# number of rows to be output
number_of_rows = -1

shrunk_file_name = file_name
if number_of_rows >= 0:
  shrunk_file_name += "-" + str(number_of_rows)
shrunk_file_name += ".csv"
columns = ["id", "pledged", "goal", "backers_count", "state", "spotlight", "staff_pick", "is_starrable", "disable_communication", "created_at", "launched_at", "state_changed_at", "deadline", "launched_to_deadline_days", ['category', 'id'], ['category', 'name'], ['creator', 'id'], ['location', 'id'], ['location', 'state'], "name", "blurb", "slug"]
columns_with_null = {}
with open("data/processed/" + shrunk_file_name, 'wb') as out_file:
  wh = csv.writer(out_file, quoting=csv.QUOTE_NONE)
  row = []
  for column in columns:
    column_name = column
    if type(column) is list:
      column_name = '_'.join(column)
    row.append(column_name)
  wh.writerow(row)

  wr = csv.writer(out_file, quoting=csv.QUOTE_NONNUMERIC)
  with open("data/original/" + file_name + ".json", "r") as f:
    projects = []
    for cnt, line in enumerate(f):
      project = json.loads(line)
      if project['data']['country'] != 'US' or ('location' in project['data'] and project['data']['location']['country'] != 'US') or project['data']['currency'] != 'USD' or project['data']['current_currency'] != 'USD' or project['data']['state'] not in ['failed', 'successful']:
        continue
      projects.append(project)


    if number_of_rows > 0 and number_of_rows < len(projects):
      indexes = random.sample(range(0, len(projects)), number_of_rows)
      projects_to_use = []
      for index in indexes:
        projects_to_use.append(projects[index])
    else:
      projects_to_use = projects
      

    for project in projects_to_use:
      row = []
      for column in columns:
        column_name = column
        try:
          if type(column) is list:
            column_name = '_'.join(column)
            row_data = project['data'][column[0]][column[1]]
          elif column_name == 'launched_to_deadline_days':
            row_data = (project['data']['deadline'] - project['data']['launched_at']) / 86400.0
          else:
            row_data = project['data'][column]

          if type(row_data) is unicode:
            row_data = row_data.encode('utf-8').replace("\n", "").replace("\r", "")
        except:
          columns_with_null[column_name] = columns_with_null.get(column_name, 0) + 1
          row_data = None
        row.append(row_data)
      wr.writerow(row)

print("Nulls:")
print(columns_with_null)
print("Took {} seconds".format(time.time() - start_time))
