import requests

# 1. Define the URL
url = "http://127.0.0.1:8000/upload"

# 2. Pick a PDF file (Make sure this file exists in your folder!)
files = {'file': open('pdfs/sample_pdf_1.pdf', 'rb')} 

print("Attempting to upload...")

try:
    # 3. Send the request
    response = requests.post(url, files=files)
    
    # 4. Print the result
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)