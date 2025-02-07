import requests
TOKEN = "7547168681:AAFOMetVjyTejjOEjKfVMRBv0EJ68nJ6Sb0"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
print(requests.get(url).json())
