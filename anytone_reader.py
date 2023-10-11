import csv


with open("anytone3.csv", "r",  newline='', encoding='utf-8') as a:
    reader = csv.reader(a, delimiter=',', quotechar='|')

    for row in reader:
        print(row)


#with open('anytone.csv', newline='') as csvfile:
#    reader = csv.reader(csvfile)