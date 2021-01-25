# scraping from coingecko.com. Called every ~1 minute to update metrics
# does nothing except to regularly update a csv file

import time
import random









time.sleep(random.randrange(45,70))


# writing to csv:
import csv

csvFile = open('test.csv', 'w+')    # will create if not existing already
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow( (i, i+2, i*2))
finally:
    csvFile.close()
