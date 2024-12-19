import os
import re

def reformat_lrc(input_file, output_file):
    """
    Reformats .lrc file to have the first timestamp in [time] and subsequent timestamps in <time>.

    Args:
        input_file (str): Path to the input .lrc file.
        output_file (str): Path to save the reformatted lyrics.
    """
    # Read the input .lrc file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    reformatted_lines = []

    # Process each line
    for line in lines:
        # Match all timestamps and lyrics in the line
        matches = re.findall(r"(\[\d{2}:\d{2}\.\d{3}\])([^\[\]]+)", line)
        
        if matches:
            reformatted_line = ""
            for idx, (timestamp, word) in enumerate(matches):
                # First timestamp uses []
                if idx == 0:
                    reformatted_line += f"{timestamp}{word.strip()} "
                else:
                    # Subsequent timestamps use <>
                    reformatted_line += f"<{timestamp[1:-1]}>{word.strip()} "
            reformatted_lines.append(reformatted_line.strip())

    # Write the reformatted lines to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        for line in reformatted_lines:
            f.write(line + "\n")

if __name__ == "__main__":
    # Example file paths
    base_dir = os.getcwd()
    input_file = os.path.join(base_dir, "Justin Bieber - Sorry.lrc")  # Path to the input .lrc file
    output_file = os.path.join(base_dir, "Justin Bieber - Sorry_reformatted.lrc")  # Path to save the reformatted .lrc file

    # Reformat the .lrc file
    reformat_lrc(input_file, output_file)

    print(f"Reformatted lyrics saved to: {output_file}")
