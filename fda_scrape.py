import requests
import csv
from bs4 import BeautifulSoup as Soup

csv_content_length = 32750
fda_url = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm"
filename = "fda_records.csv"
with open(filename, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    # html parsing to get all CFR title options
    response = requests.get(fda_url)
    page_soup = Soup(response.text, "html.parser")
    options = page_soup.find("select")
    option = options.contents[1]
    # contains all the child pages
    part_list = []
    while option is not None:
        key = int(option.attrs['value'])
        if key != 0:
            part_list.append(key)
        if len(option.contents) > 1:
            option = option.contents[1]
        else:
            option = None

    # Iterate for each post
    for key in part_list:
        data = {"CFRPart": key, "Search": "search"}
        response = requests.post(fda_url, data)
        page_soup = Soup(response.text, "html.parser")
        column1 = "\"" + page_soup.table.tr.td.table.findAll("tr")[3].div.find("a").text + "\""
        items = page_soup.table.tr.td.table.findAll("tr")[3].findAll("td")[0].findAll("strong")
        for item in items:
            if item.a is not None:
                data = item.a['href'].split('?')[1]
                response = requests.get(fda_url, data)
                page_soup = Soup(response.text, "html.parser")
                all_rows = list(page_soup.table.tr.td.table.children)
                row_counter = 0
                while row_counter < len(all_rows):
                    if all_rows[row_counter] == '\n':
                        row_counter += 1
                        continue
                    if all_rows[row_counter].strong is not None:
                        break
                    row_counter += 1
                column2 = "\"" + all_rows[row_counter].strong.text.strip().split('--')[1] + "\""
                for row_num in range(row_counter, len(all_rows)):
                    row = all_rows[row_num]
                    if row is not None and row != '\n' and len(row.findAll("table")) >= 2:
                        table1 = row.findAll("table")[0]
                        text_arr = table1.tr.td.text.strip().split(' ')
                        column3 = "\"" + text_arr[1:][0] + "\""
                        column4 = "\"" + " ".join(text_arr[1:][1:]) + "\""
                        cntnt = " ".join(list(row.findAll("table")[1].strings)).strip().replace("\n", "")
                        column5 = "\"" + (cntnt[:csv_content_length] + '...') if len(cntnt) > csv_content_length else cntnt + "\""
                        fields = [column1, column2, column3, column4, column5]
                        csv_writer.writerow(fields)