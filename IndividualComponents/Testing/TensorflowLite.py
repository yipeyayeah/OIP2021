import os, time, cv2, json, re
from pathlib import Path

directory = r'/home/pi/Desktop/OIP2021/IndividualComponents/Testing/TestImages'


def sendToAPI():
    start_time=time.time()
    for filename in os.listdir(directory):
        
        if filename.endswith(".jpg"):
            file_paths = [os.path.join(directory, filename)]
            print(filename)
            project_id = '53910905-2afc-430d-8f8e-e491ed97b4e8' #object detection (clean, dirty, empty)
            code = """curl --silent --request POST \
            --url https://app.slickk.ai/api/project/entryPoint \
            --header 'Accept: */*' \
            --header 'Accept-Language: en-US,en;q=0.5' \
            --header 'Connection: keep-alive' \
            --header 'Content-Type: multipart/form-data' \
            --form "projectId={1}" \
            {0}""".format(''.join(["--form data=@{0}".format(path) for path in file_paths]), project_id)

                # execute code
            results = os.popen(code).read()
                # above return string, include progress, so remove
            results = re.sub(r'{"progress":\d+,"max":\d+}', "", results)
                # process using json library and load into program
            results = json.loads(results)
                # print text of the result
            print('Result from slickk.ai API: '+ str(results[0]["text"])+'\n')
           
        else:
            continue
    
    

    print("--------Execution time: %s seconds--------" %(time.time()-start_time))  
        



def main():
    
    sendToAPI()

main()
