import os
import csv
import xml.etree.ElementTree as ET

csv_content_length = 32750


def get_text(section):
    text = section.text + " " if section.text else ""
    for child in list(section):
        if not list(child):
            if child.tag == 'DefinedTermFr':
                text += ""
            else:
                text += child.text + " " if child.text else ""
        else:
            text += get_text(child)

    return text


def generate():
    xml_filename = 'canada.xml'
    xml_file = os.path.join(xml_filename)
    root = ET.parse(xml_file).getroot()
    body = root.find('Body')

    column1 = ""
    column2 = ""
    column3 = ""
    column4 = ""
    column5 = ""

    filename = "canada_records.csv"
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for child in list(body):
            if child.tag == 'Heading':
                # Heading
                heading_level = int(child.get('level'))
                if child.find('TitleText') is None:
                    continue

                if child.find('TitleText').text:
                    title_text = child.find('TitleText').text
                else:
                    title_text = ""

                if heading_level == 1:
                    column1 = "\"" + title_text + "\""
                    column2 = ""
                    column3 = ""
                    column4 = ""
                elif heading_level == 2:
                    column2 = "\"" + title_text + "\""
                    column3 = ""
                    column4 = ""
                elif heading_level == 3:
                    column3 = "\"" + title_text + "\""
                    column4 = ""
                elif heading_level == 4:
                    column4 = "\"" + title_text + "\""
            else:
                # Section
                column6 = ""
                for sub_section in list(child):
                    if sub_section.tag == 'Label':
                        column5 = "\"" + sub_section.text + "\""
                    elif sub_section.tag == 'HistoricalNote':
                        continue
                    else:
                        column6 += get_text(sub_section)
                column6 = "\"" + (column6[:csv_content_length] + '...') if len(column6) > csv_content_length else column6 + "\""
                fields = [column1, column2, column3, column4, column5, column6]
                csv_writer.writerow(fields)


generate()