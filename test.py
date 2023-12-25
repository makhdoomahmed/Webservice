import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from flask import Flask, render_template, request

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

BASE_URL = 'https://mobileservicesuat.aadc.ae' # API Base end point

app = Flask(__name__) # creating Flask Object Class

@app.route('/',methods = ['GET'])
def show_indexhtml():
    return render_template('test.html') # Show the main web page of your application only in Development environment

@app.route('/send_data', methods = ['POST']) #creating POST 
def get_data_from_html():  # function which wil take the data from your application web page
        userId = request.form['userId'] # assigning web page data value into variable
        password = request.form['password'] # assigning web page data value into variable
        
        # creating query paramaters to invoke API
        query_params = {
        "UserID": userId,
        "Password": password,
        "ClientID" : "Mobile"
        }

        # Calling the API with Base URL value and other appended end point with methd name, verify false not validing SSL
        response = requests.post(f"{BASE_URL}/AADCUAT2022/LoginService.svc/ValidateUser",verify=False, json=query_params)

        if response.status_code == 200: # if web service sucessfully executed
          json_res = json.loads(response.text) # convert the response in Json dictionary

          if response.json().get('StatusCode') == '100': # Check user is authenticated by API StatusCode value
               return(f"Authorized User") 
               
          elif response.json().get('StatusCode') == '199': # Check user is not authenticated by API StatusCode value
            return(f"Un Authorized User")
            
        else:
            return(f"Technical Error") # If API not executed due to any other technical error

# Invoking the Flask web service on below host and port only for development environment
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)