from callAPIs import downloadFile, getRequestIDforExport, getRequestIDforImport, getStatus, getToken, listPublicTasks
from time import sleep

url = 'http://10.226.107.101/'
publicTasks = []
requestIDsforExport = []
requestIDsforImport = []
status_downloadIDs = []
filepath = 'C:/Users/Administrator/Downloads/test.zip'

token = getToken(url)

# export
publicTasks = listPublicTasks(url, token)
print(publicTasks)
for task in publicTasks:
    requestIDsforExport.append(getRequestIDforExport(url, token, task['id'], task['taskname']))
for id in requestIDsforExport:
    sleep(3)
    status_downloadIDs.append(getStatus(url, token, id['requestId']))
for e in status_downloadIDs:
    print(e['status'])
    print(e['downloadFileId'])
    downloadFile(url, token, e['downloadFileId'])

# import
requestIDsforImport.append(getRequestIDforImport(url, token, filepath))
print(requestIDsforImport)
for id in requestIDsforImport:
    sleep(3)
    print(getStatus(url, token, id['requestId']))
