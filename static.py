css_styles = '''

        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;           
        }

        .centered {
            position: absolute; /* Position absolutely */
            top: 50%; /* Position the top edge of the element in the middle of the container */
            left: 50%; /* Position the left edge of the element in the middle of the container */
            transform: translate(-50%, -50%); /* Offset the element by half its width and height */
        }

        .avatar {
            padding-left: 18%;

        }

        .chat-container {
            align-items: flex-start; /* Align items to the start of the flex container */
            width: 100%;
            max-width: 800px;
            height: calc(100vh - 40px); /* Adjust height based on your UI */
            margin-top: 10px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 10px;
            margin-left: 25px;
            margin-right: 10px;
            position: relative;
            overflow-y: auto;
            margin-bottom: 10px; /* Space before the chat input */
            box-shadow: 
            -8px -8px 12px 0 rgba(0, 0, 0, 0.3),
            12px 12px 16px rgba(255, 255, 255, 0.25);
        }

        .message {
            background-color: #f9f9f9;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 6px;
        }

        .message.sender {
            background-color: #e6f7ff;
            text-align: right;            
        }

        .message.sender .message-text {
            color: #007bff;
        }

        .message.sender .message-sender {
            font-weight: bold;
        }
        
        .container {
            display: flex; /* Use flexbox layout */
            align-items: flex-start; /* Align items to the start of the flex container */
            max-width: 100%; /* Maximum width of the container */
            width: 100%;
            margin: auto; /* Center the container */
            position: absolute;
            left: 0;
            box-shadow: 
            12px 12px 16px 0 rgba(0, 0, 0, 0.25),
            -8px -8px 12px 0 rgba(255, 255, 255, 0.3);
            }
            
        .form-container {
            width: 99%;
            display: flex;
            flex-direction: column;
            background-color: #f0f0f0;
            height: 95vh; /* Make the chat container take up the full viewport height */
            border-radius: 8px;
            justify-content: space-between;
            flex: 1; /* Take up the other half of the container space */
            margin-left: 10px; /* Add some space between the form and the chat container */
            margin-top: 10px;
        }

        .chat-input {
            margin-top: 30px;
            margin-bottom: 0px;
        }

        .submit {
            background: linear-gradient(-45deg, rgba(0,0,0,0.1), rgba(200,200,200,0.05));
            border-radius: 8px;
            background-color: #f9f9f9;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border: none;
            width: 101%;
            margin-top: 10px;
        }

        #messageInput {
            width: 97%; /* Take up the full width of the form container */
            border: none;
        }
        
        .custom-select {
            padding: 5px 4px 5px 4px; /* Adjust padding to your preference */
        }
            
        textarea {
            height: 30vh;
            border-radius: 10px;
            border: none;
            padding: 8px;
            box-shadow: 
            -8px -8px 12px 0 rgba(0, 0, 0, 0.3),
            12px 12px 16px rgba(255, 255, 255, 0.25);
            
        }
        
        select {
            border-radius: 10px;
            border: none;
            padding: 8px;
        }
        
        .input-element {
            box-shadow:
            -8px 8px 12px 0 rgba(0, 0, 0, 0.3),
            12px -12px 16px rgba(255, 255, 255, 0.25);
        }

        .avatar-button {
            max-width: 49%;
            margin-bottom: 8px;
        }
                
        .chat-button {
            margin-right: 0px;
        }

        .message-datetime {
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }

'''

chat_js = '''
<script>
 
</script>
'''

