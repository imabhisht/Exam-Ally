import dotenv
dotenv.load_dotenv()
from flask import Flask, request, send_file
from flask_cors import CORS
# from routes import project_routes
import logging
from api.functions.copilot_gen import generate_text
import os
import random
from io import BytesIO
import pymongo

## Connect the MongoDB Database
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client["examally"]
collection = db["messages"]


def configure_logging(app):
    # Set log level
    log_level = logging.DEBUG
    app.logger.setLevel(log_level)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    app.logger.addHandler(stream_handler)

app = Flask(__name__)
configure_logging(app)
# project_routes(app)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/help')
def help():
    return 'To use write a Prompt after / in the url. Example: https://www.examally.co/WriteHelloWorldPythonProgram. The response will be the code generated.'


@app.route('/s/<string:q>')
def ai_route(q):
    ## Get Query Parameters
    # q = request.args.get('q')
    if q:
        # Modify the string to append space before every uppercase letter (except the first one)
        modified_q = ''
        for i, char in enumerate(q):
            if i > 0 and char.isupper():
                modified_q += ' ' + char
            else:
                modified_q += char
        answer = generate_text(modified_q)

        if "```python" in answer and "```" in answer:
            start = answer.index("```python")
            end = answer.index("```", start+1)
            answer = answer[start:end+3]

            ## Remove ```python and ``` from the code
            answer = answer.replace("```python", "")
            answer = answer.replace("```", "")
            
            app.logger.info(f"Prompt: {modified_q} \nCode: {answer}")
            app.logger.info("Python code found in answer. Returning python code.")
            return answer
        else:
            app.logger.info(f"Prompt: {modified_q} \nCode: {answer}")
            app.logger.info("Answer does not contain python code")
            return answer
    else:
        return 'Hello, World!'

@app.route('/puja/<string:q>', methods=['GET'])
def send_message_secure(q):
    
    print("q", q)
    print("request", os.getenv('MONGODB_URI'))

    if q:

        modified_q = ''
        for i, char in enumerate(q):
            if i > 0 and char.isupper():
                modified_q += ' ' + char
            else:
                modified_q += char

        # Save the message in the database
        # message = {"message": modified_q}
        # Insert the message in the database with _id
        if(collection.find_one({"_id": "puja"})):
            collection.update_one({"_id": "puja"}, {"$set": {"message": modified_q}})
        else:
            collection.insert_one({
                "_id": "puja",
                "message": modified_q
            })
        app.logger.info(f"Message saved: {q}")
        print("Message saved")
        return 'Message saved successfully'
    else:
        return 'Message not saved'
 
@app.route('/puja', methods=['GET'])
def get_message_secure():
    message = collection.find_one({"_id": "puja"})
    if message:
        app.logger.info(f"Message fetched: {message['message']}")
        return message['message']
    else:
        return 'Message not found'

@app.route('/save/<string:q>')
def ai_route_save(q):
    ## Get Query Parameters
    # q = request.args.get('q')
    if q:
        # Modify the string to append space before every uppercase letter (except the first one)
        modified_q = ''
        for i, char in enumerate(q):
            if i > 0 and char.isupper():
                modified_q += ' ' + char
            else:
                modified_q += char

        # Generate text
        answer = generate_text(modified_q, save=True)

        ## If answer contains ```python in start and ``` end, then only return the code
        if "```python" in answer and "```" in answer:
            start = answer.index("```python")
            end = answer.index("```", start+1)
            answer = answer[start:end+3]

            ## Remove ```python and ``` from the code
            answer = answer.replace("```python", "")
            answer = answer.replace("```", "")
            
            python_code_bytes = bytes(answer, 'utf-8')

            # Create an in-memory file-like object using BytesIO
            in_memory_file = BytesIO()
            in_memory_file.write(python_code_bytes)
            in_memory_file.seek(0)
            app.logger.info("Python code found in answer. Returning python code as a file.")
            app.logger.info(f"Prompt: {modified_q} \nCode: {answer}")
            return send_file(in_memory_file, as_attachment=True, download_name="gen_code.py", mimetype='text/plain')
        
        else:
            app.logger.info("Answer does not contain python code")
            return answer

    else:   
        return 'Hello, World!'



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

