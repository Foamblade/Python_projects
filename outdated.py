month = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

def main():
    while True:
        try:
            date1 = input("Date: ")
            date = date1.split('/')
            if int(date[0]) <= 12 and int(date[1]) <= 31:
                slash(date)
                break
        except:
            date2 = date1.split()
            if date2[0] in month and date2[1].endswith(',') and int(date2[1].replace(',','')) <= 31:
                long(date2)
                break

def slash(date):
    print(f"{int(date[2]):04d}", f"{int(date[0]):02d}", f"{int(date[1]):02d}", sep='-')

def long(date):
    date[1] == date[1].replace(',','')
    print(f"{int(date[2]):04d}", f"{month.index(date[0])+1:02d}", f"{int(date[1].replace(',','')):02d}", sep='-')

main()

