import os
import re
import json


def read_file(file_path):
    """
    Reads the content of a file. Output is a list of lines.

    :param file_path: Path to the input file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content


def select_items(array_of_lines):
     # Create regex for skipping specified tags
    i = 0
    all_items = []  
    while i < len(array_of_lines):
        if '<item>' in array_of_lines[i]:
            # Skip the <item> tag
            i += 1
            items = []
            while not '</item>' in array_of_lines[i]:
                items.append(array_of_lines[i])
                i += 1
        elif '</item>' in array_of_lines[i]:
            # Only add items that are pages
            all_items.append(items)
            i += 1
        else:
            i += 1
            print("Skipping line #: ", i)
    return all_items

def filer_items(all_items):
    indexes = []
    for i in range(len(all_items)):
        for line in all_items[i]:
            if "<wp:post_type><![CDATA[page]]></wp:post_type>" in line:
                i+=1
                indexes.append(i)
                break
    print("Indexes: ", indexes)
    filtered_items = [all_items[i] for i in indexes]
    # write_out(filtered_items, '../processed_files', 'filtered_items', max_lines=250000, total_parts=1)
    return filtered_items

import re

def items_to_json(filtered_items, included_tags):
    json_items = []

    # Compile regex for extracting tag content
    tag_pattern = re.compile(r"<\s*({})\s*>(.*?)</\s*\1\s*>".format("|".join(included_tags)))

    for item in filtered_items:
        json_item = {}
        for line in item:
            # Match line against the pattern
            match = tag_pattern.search(line)
            if match:
                tag = match.group(1)  
                content = match.group(2) 
                json_item[tag] = content 
        if json_item:  
            json_items.append(json_item)

    write_out(json_items, '../processed_files', 'json_items', max_lines=250000, total_parts=1)
    return json_items


def write_out(lines_array, output_dir, output_filename, max_lines=250000, total_parts=1):
    """
    Writes out the filtered lines to a file or splits them into parts.

    :param filtered_lines: List of filtered lines.
    :param output_dir: Directory to store the output files.
    :param name: Base name of the output file(s).
    :param max_lines: Maximum number of lines per split file.
    :param total_parts: Total number of parts (set to 1 for a single file).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chunk = []
    chunk_index = 1

    for i, line in enumerate(lines_array):
        chunk.append(','.join(line))  # Add the line to the current chunk
        if len(chunk) >= max_lines or i == len(lines_array) - 1:
            # Determine the output file path
            chunk_file_path = (
                os.path.join(output_dir, f"{output_filename}.xml") 
                if total_parts == 1 
                else os.path.join(output_dir, f"{output_filename}_part_{chunk_index}.xml")
            )
            # Write the chunk to the file
            with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
                if total_parts > 1:
                    chunk_file.write(f"<!-- Part {chunk_index} of {total_parts} -->\n")
                chunk_file.writelines(chunk)
            chunk_index += 1
            chunk = []  # Reset the chunk after writing

    if total_parts == 1:
        print(f"File successfully written to {os.path.join(output_dir, f'{output_filename}.xml')}.")
    else:
        print(f"File successfully split into {chunk_index - 1} parts.")

include_tags = ['title','link','content:encoded','excerpt:encoded','wp:post_type']
selected_items = select_items(read_file('../unprocessed_files/wordpress_unc_oct_2024.xml'))
filtered_items = filer_items(selected_items)
json_items = items_to_json(filtered_items, include_tags)
# Save to a JSON file
output_file = "../processed_files/output.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_items, f, indent=4, ensure_ascii=False)
print(f"JSON data saved to {output_file}.")
