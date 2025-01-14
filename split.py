import os
import re
import math

def read_file(file_path):
    """
    Reads the content of a file. Output is a list of lines.

    :param file_path: Path to the input file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content


def filter_lines(array_of_lines, skip_tags=None):
    """
    Generates array without empty fields and specified tags.

    :param array_of_lines: List of lines to filter.
    :param skip_tags: List of tags to skip.
    """

    # Create regex for skipping specified tags
    if skip_tags:
        skip_pattern = re.compile(r"<\s*({})\s*>.*?</\s*\1\s*>".format("|".join(skip_tags)))
    else:
        skip_pattern = None
        
    # Filter and clean lines in one step
    filtered_lines = [
        re.sub(r"&lt;.*?&gt;", "", line)  # Clean HTML-like tags
        for line in array_of_lines
        if not (
            re.match(r"<(\w+)>\s*</\1>", line.strip()) or  # Skip empty fields
            (skip_pattern and skip_pattern.match(line.strip()))  # Skip lines matching the skip pattern
        )
    ]

    return filtered_lines


def write_out(filtered_lines, output_dir, output_filename, max_lines=250000, total_parts=1):
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

    for i, line in enumerate(filtered_lines):
        chunk.append(line)  # Add the line to the current chunk
        if len(chunk) >= max_lines or i == len(filtered_lines) - 1:
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
        print(f"XML file successfully written to {os.path.join(output_dir, f'{output_filename}.xml')}.")
    else:
        print(f"XML file successfully split into {chunk_index - 1} parts.")


def process_xml(file_path, output_dir, output_filename, max_lines=250000, skip_tags=None, split=False):
    """
    Removes empty fields and specified tags from an XML file and writes the output to a new file.

    :param file_path: Path to the input XML file.
    :param output_dir: Directory to store the split files.
    :param output_filename: Base name of the output file(s).
    :param max_lines: Maximum number of lines per split file.
    :param skip_tags: List of tags to skip.
    :param split: Whether to split the file into multiple parts.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    array_of_lines = read_file(file_path)
    filtered_lines = filter_lines(array_of_lines, skip_tags)

    # Determine total parts after filtering
    total_lines = len(filtered_lines)
    total_parts = math.ceil(total_lines / max_lines)
    write_out(filtered_lines, output_dir, output_filename, max_lines, total_parts if split else 1)


skip_tags=["image", "id" ,"created", "updated", "hidden","position", "column", "map_id", "enable_proxy"]
# split_large_xml('../wordpress_unc_oct_2024.xml', './xml/wordpress', 'wordpress_export')
process_xml('../unprocessed_files/libguides-241008.xml', 
                './xml/libguides', 
                'libguides_export', 
                skip_tags=skip_tags,
                split=True)
