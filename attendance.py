from datetime import datetime

def markAttendance(name):
    id=name
    dt_now = datetime.today()
    f_name = dt_now.strftime("%b-%d-%Y")
    open('Attendance/' + f_name + '.csv', 'a+')
    with open('Attendance/'+f_name+'.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if id not in nameList:
            detail = id.split('-')
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{id},{detail[0]},{dtString},{detail[1]}')