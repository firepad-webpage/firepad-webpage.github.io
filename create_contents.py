import pandas as pd
from bs4 import BeautifulSoup
import os

# Load CSV
df = pd.read_csv("original_abstract.csv")  # change this to your CSV path

# HTML template
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <p>{abstract}</p>
</body>
</html>"""

# Generate HTML files
for _, row in df.iterrows():
    filename = row['filename']
    abstract = row['abstract']
    filled_html = base_html.format(abstract=abstract)
    
    with open(f"./abstract/{filename}", "w", encoding="utf-8") as f:
        f.write(filled_html)

input_dir = "content"    
output_dir = "original_content"   
os.makedirs(output_dir, exist_ok=True)

# Process each file
for idx, (_, row) in enumerate(df.iterrows(), start=4):
    input_filename = f"content{idx}.html"
    output_filename = f"content{idx+100}.html"
    new_abstract = row['abstract']

    input_path = os.path.join(input_dir, input_filename)
    output_path = os.path.join(output_dir, output_filename)

    with open(input_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find the <h2>Original Abstract</h2> tag and the next <p>
    header = soup.find("h2", string="Original Abstract")
    if header:
        next_p = header.find_next_sibling("p")
        if next_p:
            next_p.string = new_abstract

    # Write to new file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
