# standard package imports
import re
# installed Modules
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

def getPageRes(url):
    return get(url)

def getSoup(res):
    return BeautifulSoup(res.text, 'html.parser')


url1 = "https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000J5DM"

soup = getSoup(getPageRes(url1))

table = soup.find_all('table', class_="overviewKeyStatsTable")[0]

raw_data = table.find_all('td', class_="line text")

# for raw in raw_data:
#     print(raw.text)


def getRelData(raw, soup):
    data = {
        "fund_name": soup.find('h1').text,
        "nav": raw[0].text,
        "fund_size_mil": raw[-4].text,
        "ongoing_charge": raw[-1].text,
    }
    return data

def extractData(url):
    soup = getSoup(getPageRes(url))

    table = soup.find_all('table', class_="overviewKeyStatsTable")[0]
    raw_data = table.find_all('td', class_="line text")

    for data in raw_data:
        print(data.text)

    data = getRelData(raw_data, soup)
    data['url'] = url

    return data

# print(extractData(url1))

##### get URLS for next steps
nav_anchors = soup.find('div', class_="layout_left_col").find_all('a')

# Performance:
performance_url = nav_anchors[4]['href']
# Risk&Rating:
risk_rating_url = nav_anchors[5]['href']
# format from rel urls to full
print(performance_url, risk_rating_url)


######### Scrape quarterly returns

url2 = "https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000J5DM&tab=1"
soup = getSoup(getPageRes(url2))

q_table = soup.find('table', class_="returnsQuarterlyTable")
q_rows = q_table.find_all('tr')
td_per_row = [row.find_all('td') for row in q_rows]

# [expression for member in iterable]

# extract table header & date
header = td_per_row[0][0].text
date = td_per_row[0][1].text
# print("header", header)
# print("date", date)

raw_headings = q_table.find_all('td', class_="heading")[1:]
clean_headigs = [ raw_heading.text for raw_heading in raw_headings ]

# Get all the years that data is available
year_indexes = q_table.find_all('td', class_="col1 label")
clean_years_indexes = [ year_index.text for year_index in year_indexes ]
# print(clean_years_indexes)

# Q1s
q1s = q_table.find_all('td', class_="col2 value number")
clean_q1s = [ q.text for q in q1s ]
# print(clean_q1s)

# Q2s
q2s = q_table.find_all('td', class_="col3 value number")
clean_q2s = [ q.text for q in q2s ]
# print(clean_q2s)

# Q3s
q3s = q_table.find_all('td', class_="col4 value number")
clean_q3s = [ q.text for q in q3s ]
# print(clean_q3s)

# Q4s
q4s = q_table.find_all('td', class_="col5 value number")
clean_q4s = [ q.text for q in q4s ]
# print(clean_q4s)

qs = [clean_q1s, clean_q2s, clean_q3s, clean_q4s]
# setup df
df = pd.DataFrame(index=clean_years_indexes, columns=['q1','q2','q3','q4'])
# populate with data
df.q1, df.q2, df.q3, df.q4 = clean_q1s, clean_q2s, clean_q3s, clean_q4s

# print(df)

""" END OF PERFORMANCE; START OF RISK & RATING """

snapshot_url = "https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000J5DM&tab=2"
soup = getSoup(getPageRes(snapshot_url))

modern_portfolio_stats = soup.find('table', class_="ratingMptStatsTable").find_all('td', class_="value number")
clean_stats = list(map(lambda x: x.text, modern_portfolio_stats))
# print(clean_stats)

# Get the cleaned (relevant beta and alpha)
std_index_3rd_year_beta = clean_stats[0]
std_index_3rd_year_alpha = clean_stats[2]
# print("3rd_y b", std_index_3rd_year_beta)
# print("3rd_y a", std_index_3rd_year_alpha)

# GET SHARPE RATIO 
sharpe = soup.find_all('table', class_="ratingRiskTable")[1].find('td', class_="value number").text
# print(sharpe)

""" END OF RISK & RATING """

"""
True dataflow

FOR RESULT_PAGE IN PAGINATED+FILTERED RESULTS:

    => Select target fund from list from paginated list https://www.morningstar.co.uk/uk/fundscreener/default.aspx?fbclid=IwAR1K8uh6n3uf_xfPmAWYvgbgfhmSeJmpvMECi1lNOYB_9wOEKfh2ssuSoAQ#?filtersSelectedValue=%7B%22categoryId%22:%7B%22id%22:%22EUCA000550%22%7D,%22fundSize%22:%7B%22id%22:%22:BTW:1000000000:10000000000%22%7D,%22geoRegion%22:%7B%22id%22:%22RE_UnitedKingdom%22%7D,%22globalCategoryId%22:%7B%22id%22:%22$GC$UKEQLC%22%7D,%22managementStyle%22:%7B%22id%22:%22true%22%7D,%22totalReturnTimeFrame%22:%7B%22id%22:%22GBRReturnM60%22%7D,%22investmentObjective%22:%7B%22id%22:%22Growth:EQ:1%22%7D%7D&sortField=legalName&sortOrder=asc

    => Go to target URL via click

    => While on landing target page, extract Key stats (Name, NAV, Fund Size [mil], Ongoing Change)

    => Navigate to "performance" and extract quarterly returns

    => Navigate to "risk & rating" and extract modern portfolio stats including 3-yr Sharpe Ratio

    => Compose extracted data object and write to csv





"""