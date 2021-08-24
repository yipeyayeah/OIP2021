import requests
r = requests.get('curl --silent --request POST --url https://app.slickk.ai/api/project/undesirable-care --header \'Accept: */*\' --header 'Accept-Language: en-US,en;q=0.5' --header 'Connection: keep-alive'     --header 'Content-Type: multipart/form-data'     --form 'projectId=dfbb7979-773f-4b4e-b8b9-64331d6fd477'   --form data=@/home/pi/Desktop/camera.jpg   ')
r.json()