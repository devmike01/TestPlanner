import os
from tablib import Dataset

from gemini import AjalaAi

dataset = Dataset()

dataset.headers = ['Category', 'Subcategory', 'Field Name', 'Validity', 'Input', 'Expected Output', 'Description']


# Function to generate a unique identifier for each row
def generate_row_identifier(row):
    return f"{row['Category']}_{row['Subcategory']}_{row['Field Name']}"


# Set of existing row identifiers to prevent duplicates
existing_row_ids = set()

# Check if the Excel file already exists
file_name = 'test_case_table.xlsx'
if os.path.exists(file_name):
    # If the file exists, load the existing dataset and add identifiers for existing rows
    with open(file_name, 'rb') as f:
        existing_data = Dataset().load(f.read())
        for row in existing_data.dict:
            existing_row_ids.add(generate_row_identifier(row))  # Add existing rows' identifiers


def json_xls(raw_json):
    for category in raw_json['categories']:
        for subcategory in category['subcategories']:
            for field in subcategory['fields']:
                test_row = {
                    'Category': category['name'],
                    'Subcategory': subcategory['name'],
                    'Field Name': field['field_name'],
                    'Validity': field['validity'],
                    'Input': field['input'],
                    'Expected Output': field['expected_output'],
                    'Description': field['description']
                }

                row_id = generate_row_identifier(test_row)

                if row_id not in existing_row_ids:
                    dataset.append([
                        test_row['Category'],
                        test_row['Subcategory'],
                        test_row['Field Name'],
                        test_row['Validity'],
                        test_row['Input'],
                        test_row['Expected Output'],
                        test_row['Description']
                    ])
                    existing_row_ids.add(row_id)


file_path = "/Users/admin/Desktop/Fitfocus"
file_list = os.listdir(file_path)
app_views = {}
views_logic = {}
for f_name in file_list:
    if "." not in f_name and "venv" not in f_name:
        app_folder = os.listdir(f"{file_path}/{f_name}")
        if "views.py" in app_folder:
            for view_py in app_folder:
                app_views[f_name] = f"{file_path}/{f_name}/{view_py}"
for app, file_path in app_views.items():
    file = open(os.path.join(file_path), 'r')
    read_file = file.read()
    if views_logic.get(app):
        views_logic[app].append(read_file)
        views_logic[app] = views_logic.get(app)
    else:
        views_logic[app] = [read_file]

for app, view_py_codes in views_logic.items():
    print('------ Grab a cup of coffee. Ajala is writing your test plans -------')
    ajala_response = AjalaAi().write_test_sheet(view_py_codes)
    print('>>>>', f'Writing {app} to excel', '<<<<')
    json_xls(ajala_response)

# Export the dataset to an Excel file (.xlsx)
with open(file_name, 'wb') as f:
    f.write(dataset.export('xlsx', column_width='adaptive'))
    print('------ Ajala Ai is done!! -------')
