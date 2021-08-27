import os 
import json
import re
from pathlib import Path

file_paths = [os.path.join(Path().absolute(), 'camera.jpg')]

#project_id = 'dfbb7979-773f-4b4e-b8b9-64331d6fd477'
project_id = '53910905-2afc-430d-8f8e-e491ed97b4e8'
code = """curl --silent --request POST \
--url https://app.slickk.ai/api/project/entryPoint \
--header 'Accept: */*' \
--header 'Accept-Language: en-US,en;q=0.5' \
--header 'Connection: keep-alive' \
--header 'Content-Type: multipart/form-data' \
--form "projectId={1}" \
{0}""".format(''.join(["--form data=@{0}".format(path) for path in file_paths]),project_id)

#execute code
results = os.popen(code).read()
#print(results)
#above return string, include progress, so remove
results = re.sub(r'{"progress":\d+,"max":\d+}',"", results)
#process using json library and load into program
results = json.loads(results)
#print text of the result
print([result["text"] for result in results])
