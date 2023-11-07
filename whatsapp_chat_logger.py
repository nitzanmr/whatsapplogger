import pandas as pd
import re
import argparse


def getDatapoint(line):
    pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\] (.*?): (.*)'
    match = re.match(pattern, line)
    # print(match)
    if match:
        date_time, author, message = match.groups()
        return date_time, author, message
    else:
        pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\] (.*?): (.*?): (.*?)>'
        match = re.search(pattern, line)
        if match:
            date_time, author, not_important, message = match.groups()
            # print(message)
            return date_time, author, message
        return None, None, line


def is_image(content, photos_folder):
    # Check if the content contains the word "attached" (case-insensitive)
    if ".jpg" in content.lower() or ".pdf" in content.lower() or ".opus" in content.lower():
        file_placement = photos_folder + "\\"+content
        file_placement = file_placement.replace('\\', '/')
        # print(file_placement.replace('\\', '/'))
        file_url = f"file:///{file_placement}"
        return file_url  # You can add image detection logic here. For example, check if the content is a URL to an image.
    return None
    
    
def main(input_file, output_file, photos_folder):
    data = []
    with open(input_file, encoding="utf-8") as fp:
        fp.readline()
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()

            # Define a regular expression pattern to match the time format without leading zero
            pattern = r'(\d{2}/\d{2}/\d{4},) (\d{1}:\d{2}:\d{2})'

            # Use re.sub() to add a leading zero to the hour if it's a single digit
            line = re.sub(pattern, r'\1 0\2', line)

            date_time, author, message = getDatapoint(line)
            
            # Check if the message is an image; if it is, skip this row
            returned_messege = is_image(message, photos_folder)
            link = ""
            if returned_messege is not None:
                link = returned_messege
                data.append([date_time, author, message, link])
            else:
                data.append([date_time, author, message, link])


    df = pd.DataFrame(data, columns=["Date/Time", 'Author', "Message", "LINK"])

    df[['Date', 'Time']] = df['Date/Time'].str.split(', ', expand=True)
    df = df[['Date', 'Time', 'Author', 'Message', 'LINK']]

    df.to_excel(output_file, index=False)
    print(f"Data written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input chat text file")
    parser.add_argument("output_file", help="Output CSV file")
    parser.add_argument("photos_folder", help=" photos_folder")

    args = parser.parse_args()
    print(main(args.input_file, args.output_file, args.photos_folder))
    # print(re.search("[Date, Time] Author: ‎<attached: Filename>"))
