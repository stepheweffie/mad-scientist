css_styles = '''
        /* Import Animate.css */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');

        :root {
            --primary-color: #7dd3fc;
            --secondary-color: #67e8f9;
            --accent-color: #a7f3d0;
            --danger-color: #ef4444;
            --background-color: #ffffff;
            --surface-color: #f0f9ff;
            --surface-light: #e0f2fe;
            --text-color: #1e293b;
            --text-muted: #64748b;
            --glow-color: #38bdf8;
            --border-color: #bae6fd;
            --hover-color: #0ea5e9;
            --success-color: #10b981;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', 'Arial', sans-serif;
            background: var(--background-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            overflow-x: hidden;
        }


        /* Main Title Styling */
        h1 {
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            color: var(--glow-color);
            text-shadow: 0 0 10px var(--glow-color);
            margin-bottom: 2rem;
        }
        
        .lab-title {
            color: var(--text-color);
            font-weight: 700;
            display: inline-block;
            padding: 0 0.5rem;
        }

        .centered {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        .form-container {
            background: var(--surface-color);
            padding: 3rem;
            border-radius: 20px;
            border: 2px solid var(--border-color);
            min-width: 400px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 30px rgba(192, 132, 252, 0.1);
            cursor: default;
        }

        .avatar {
            text-align: center;
            margin: 1rem 0;
        }

        .avatar img {
            border-radius: 12px;
            border: 3px solid var(--glow-color);
            box-shadow: 0 0 15px rgba(192, 132, 252, 0.3);
            cursor: pointer;
        }


        .chat-container {
            width: 48%;
            height: 95vh;
            margin-top: 10px;
            background: var(--surface-color);
            border-radius: 12px;
            padding: 20px;
            margin-left: 10px;
            margin-right: 10px;
            position: relative;
            overflow-y: auto;
            border: 2px solid var(--border-color);
            box-shadow: 0 0 20px rgba(192, 132, 252, 0.1);
            display: flex;
            flex-direction: column;
        }

        .message {
            background: var(--surface-light);
            color: var(--text-color);
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 15px;
            border-left: 4px solid var(--glow-color);
        }


        .message.sender {
            background: var(--primary-color);
            color: var(--text-color);
            text-align: right;
            border-left: none;
            border-right: 4px solid var(--glow-color);
        }


        .message.sender .message-text {
            color: var(--text-color);
            font-weight: 500;
        }

        .message-sender {
            font-weight: bold;
            margin-bottom: 8px;
            display: block;
        }
        
        .container {
            display: flex;
            align-items: flex-start;
            max-width: 100%;
            width: 100%;
            margin: 0;
            padding: 10px;
            min-height: 100vh;
            box-sizing: border-box;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
            
        .form-container {
            width: 48%;
            display: flex;
            flex-direction: column;
            background: var(--surface-color);
            height: 95vh;
            border-radius: 12px;
            padding: 20px;
            flex: none;
            margin-left: 10px;
            margin-top: 10px;
            border: 2px solid var(--border-color);
            box-shadow: 0 0 20px rgba(192, 132, 252, 0.1);
        }

        /* Form Elements */
        .input-element {
            background: var(--surface-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            font-size: 1rem;
            color: var(--text-color);
            transition: all 0.3s ease;
            cursor: text;
        }

        .input-element:focus {
            outline: none;
            border-color: var(--glow-color);
            box-shadow: 0 0 10px rgba(192, 132, 252, 0.2);
        }

        input[type="email"] {
            width: 100%;
            margin-bottom: 1.5rem;
        }

        .custom-select {
            width: 100%;
            margin-bottom: 1rem;
            background: var(--surface-color);
            color: var(--text-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            cursor: pointer;
        }

        textarea {
            width: 100%;
            height: 150px;
            background: var(--surface-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            color: var(--text-color);
            font-family: inherit;
            resize: vertical;
            transition: all 0.3s ease;
            cursor: text;
        }

        textarea:focus {
            outline: none;
            border-color: var(--glow-color);
            box-shadow: 0 0 10px rgba(192, 132, 252, 0.2);
        }

        .message-text {
            width: 100%;
            min-height: 120px;
            background: var(--surface-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            color: var(--text-color);
            font-family: inherit;
            resize: vertical;
            cursor: text;
        }

        /* Buttons */
        .submit {
            background: var(--primary-color);
            border: 2px solid var(--primary-color);
            border-radius: 12px;
            color: var(--text-color);
            padding: 15px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            margin-top: 1.5rem;
            display: block;
            text-decoration: none;
            text-align: center;
        }

        .submit:hover {
            background: var(--secondary-color);
            border-color: var(--secondary-color);
            transform: translateY(-2px);
        }

        .submit:active {
            transform: translateY(0);
        }

        .submit:focus {
            outline: 2px solid var(--glow-color);
            outline-offset: 2px;
        }

        .avatar-button {
            max-width: 48%;
            margin: 0.5rem;
            padding: 12px 20px;
            font-size: 1rem;
            border-radius: 10px;
            display: inline-block;
            cursor: pointer;
            background: var(--surface-light);
            border: 2px solid var(--border-color);
            color: var(--text-color);
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        .avatar-button:hover {
            background: var(--hover-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(91, 33, 182, 0.3);
        }

        /* Labels and Text */
        p {
            color: var(--text-color);
            font-weight: 500;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
            cursor: default;
        }

        label {
            color: var(--text-color);
            font-weight: 500;
            margin-bottom: 0.5rem;
            display: block;
            cursor: pointer;
        }

        /* Loading Animation */
        .submit.loading {
            position: relative;
            pointer-events: none;
            cursor: wait;
            opacity: 0.7;
        }

        .submit.loading::after {
            content: '';
            position: absolute;
            top: 50%;
            right: 15px;
            width: 16px;
            height: 16px;
            margin: -8px 0 0 0;
            border: 2px solid transparent;
            border-top: 2px solid var(--text-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
                padding: 5px;
            }
            
            .form-container, .chat-container {
                width: 100%;
                height: auto;
                min-height: 50vh;
                margin: 5px 0;
            }
            
            .form-container {
                padding: 1rem;
            }

            h1 {
                font-size: 2rem;
            }

            .avatar-button {
                max-width: 100%;
                margin: 0.5rem 0;
            }
        }

'''

chat_js = '''
<script>
 
</script>
'''

