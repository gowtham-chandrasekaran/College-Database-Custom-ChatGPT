import json
import openai
import db_helper
from secret_key import openai_key
openai.api_key = openai_key

def get_answer(question):
    messages = [
        {"role":"user","content":question}
    ]
    functions = [
        {
            "name":"get_marks",
            "description":"Get the GPA of a college student or aggregate GPA (such as average,min,max) for a given semester. If function returns -1 then it means that there is no record in the database",
            "parameters":{
                "type":"object",
                "properties":{
                    "student_name":{
                        "type":"string",
                        "description":"First and Last name of a student. e.g John Smith",
                    },
                    "semester":{
                        "type":"integer",
                        "description":"A number between 1 and 4 indicating the semester",
                    },
                    "operation":{
                        "type":"string",
                        "description":"If student is blank that means aggregate number such as max, min or average is being requested for an entire semester. semester must be passed in this case. If student field is blank and say they are passing 1 as a value in semester. Then operation parameter will tell if they need a maximum, minimumor an average GPA of all students in semester 1.",
                        "enum":["max","min","avg"],
                    },
                },
                "required":["semester"],
            },
        },
        {
            "name":"get_fees",
            "description":"Get the fees for an individual student or total fees for an entire semester. If function return -1 then it means that there is no record in the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "First and last Name of the student. e.g John Smith",
                    },
                    "semester": {
                        "type": "integer",
                        "description": "A number between 1 to 4 indicating the semester of a student",
                    },
                    "fees_type": {
                        "type": "string",
                        "description": "fee type such as 'paid', 'pending' or 'total'",
                        "enum": ["paid", "pending", "total"]
                    },
                },
                "required": ["semester"],
        },
    } 
]

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
    response_message = response["choices"][0]["message"]
    
    if response_message.get("function_call"):
        available_functions = {
            "get_marks":db_helper.get_marks,
            "get_fees":db_helper.get_fees
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(function_args)

        # To get LLM answer (human readable answer)

        messages.append(response_message)
        messages.append(
            {
                "role":"function",
                "name":function_name,
                "content":str(function_response),
            }
        )
        second_response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0613",
            messages=messages,
        )
        return second_response["choices"][0]["message"]["content"]
    
    else:
        
        return response_message["content"]


        



if __name__ == '__main__':
    print(get_answer("What was the average GPA in second semester?"))