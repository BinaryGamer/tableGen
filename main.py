from flask import Flask, request, jsonify
import requests
app = Flask('app')

database = 'https://store.ncss.cloud/mel-group3-studybot-planner'

def get_data():
  return requests.get(database)

@app.route('/', methods=["POST"])
def table():
  data = request.get_json()
  author = data['author']
  storage = get_data().json()
  timetableData = storage[author]
  timebounds = timetableData['study']
  timePerDay = int((timebounds[1] - timebounds[0])/100)
  print(timePerDay, 'per day.')
  print(timebounds)
  time = 0
  for subject in timetableData['subjects']:
    time += int(timetableData['subjects'][subject])
  if timetableData['weekends'] == True:
    studyPerWeek = timePerDay*7
  else:   
    studyPerWeek = timePerDay*5
  print(studyPerWeek, 'per week of study time.')
  print(time, 'of studying to do.')
  if studyPerWeek < time:
    print('Impossible.')
    return jsonify({'text':'not enough time in your study week! Please take this seriously.','author':'Timetabler'})
  else:
    print("fantastic.")
  if timetableData['weekends'] == True:
    sched = {'Sun':{},'Mon':{},'Tue':{},'Wed':{},'Thu':{},'Fri':{},'Sat':{}}
  else:   
    sched = {'Mon':{},'Tue':{},'Wed':{},'Thu':{},'Fri':{}}
  subjectData = timetableData['subjects']
  for subject in subjectData:
    if subjectData[subject] > 0:
      for day in sched:       
        if subjectData[subject] > 0:
          if subject not in day:
            sched[day][subject] = 1
            subjectData[subject] -=1
          else:
            sched[day][subject] += 1
            subjectData[subject] -=1
  print(sched)




  message = {
      "author": "Timetabler",
      'text':f'cool, {author}'
    }
  return jsonify(message)

app.run(host='0.0.0.0', port=8080, debug=True)