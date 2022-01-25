import pandas as pd
import sys

n = len(sys.argv)
if n != 2:
    print('Input the xls or xlsx filename as the only command line argument')
    sys.exit()

filename = sys.argv[1]

df = pd.read_excel(filename)
del df['player_id']
del df['session_start_at']
del df['session_end_at']
del df['buy_in']
del df['buy_out']
del df['stack']

#sorting and handling duplicates in list
records = df.to_records(index=False)
result = list(records)
list = []
for i in range(0,len(result)-1):
    if i not in list:
        for j in range(i+1,len(result)):
            if result[i][0] == result[j][0]:
                result[i][1] = result[i][1] + result[j][1]
                list.append(j)
list.sort(reverse=True)
print(list)
print(result)
for i in list:
    print(i)
    result.pop(i)

result.sort(key=lambda tup: tup[1])

#splitting lists into who is up money and who is down money
index = 0
owed = 0
for index, tuple in enumerate(result):
    if tuple[1]>0:
        break
    owed = owed - tuple[1]
    index = index + 1

losers = result[:index]
winners = result[index:]

print('losers')
print(losers)
print('winners')
print(winners)

lenw = len(winners)-1
lenl = len(losers)

for i in range(0,lenl):
    debt = losers[i][1]
    while debt != 0:
        if -1*debt > winners[lenw][1]:
            print(losers[i][0], 'pays', winners[lenw][0], '$', winners[lenw][1])
            debt = debt + winners[lenw][1]
            lenw = lenw - 1
        elif -1*debt == winners[lenw][1]:
            print(losers[i][0], 'pays', winners[lenw][0], '$', -1*debt)
            debt = 0
            lenw = lenw - 1
        else:
            print(losers[i][0], 'pays', winners[lenw][0], '$', -1*debt)
            winners[lenw][1] = winners[lenw][1] + debt
            debt = 0
