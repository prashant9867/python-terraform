import re

# Function to modify a single query
def modify_query(query):
    # Remove the column name 'resolutionclosurecontrolsid'
    query = re.sub(r"resolutionclosurecontrolsid\s*,\s*", "", query, count=1)
    
    # Remove the corresponding value (assuming it's a single quoted string)
    query = re.sub(r"'[0-9]+'\s*,\s*", "", query, count=1)
    
    # Adjust the remaining query to fix any potential issues with syntax
    query = re.sub(r"\(\s*,", "(", query)  # Remove leading comma in VALUES list
    query = re.sub(r",\s*\)", ")", query)  # Remove trailing comma in VALUES list
    
    return query

# Read the input file
with open('myfileinput.txt', 'r') as file:
    queries = file.readlines()

# Modify each query
modified_queries = [modify_query(query) for query in queries]

# Write the modified queries to a new file
with open('modified_queries.txt', 'w') as file:
    file.writelines(modified_queries)

print("Queries have been modified and saved to 'modified_queries.sql'")



