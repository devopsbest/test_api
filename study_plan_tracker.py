import requests
import json
import time
import re

host = "webus1"

url = "http://{}.englishtown.com/ecplatform/mvc/studyplan/LoadStudyPlanReport?token={}"

token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJFQyIsInN1YiI6IlN0dWR5UGxhblJlcG9ydCIsInN0dWRlbnRJZCI6IjM4MjA1Nzk0In0.BIDVvMWLLFOiKc1JGogip0qO3RE53hTs0yZaxLKNFgs"

query = requests.get(url.format(host,token))
result = json.loads(query.text)
print(result)

rex = "\/Date\(-?(\d+)\)\/"
#result["Report"]["LongestCheckInPeriod"]["StartDate"] = re.search(rex,result["Report"]["LongestCheckInPeriod"]["StartDate"]).group(1)
#print(result["Report"]["LongestCheckInPeriod"]["StartDate"])
l_start_time = re.search(rex,result["Report"]["LongestCheckInPeriod"]["StartDate"]).group(1)
l_end_time = re.search(rex,result["Report"]["LongestCheckInPeriod"]["EndDate"]).group(1)
s_start_time = re.search(rex,result["Report"]["StudyPlanStartDate"]).group(1)
s_end_time = re.search(rex,result["Report"]["StudyPlanEndDate"]).group(1)
result["Report"]["LongestCheckInPeriod"]["StartDate"]= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(l_start_time)/1000))
result["Report"]["LongestCheckInPeriod"]["EndDate"]= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(l_end_time)/1000))
result["Report"]["StudyPlanStartDate"]= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(s_start_time)/1000))
result["Report"]["StudyPlanEndDate"]= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(s_end_time)/1000))


result2= json.dumps(result, sort_keys=True,indent=2)
print(result2)
