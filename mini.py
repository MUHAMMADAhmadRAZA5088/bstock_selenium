import requests

url = "https://manifest-prod.bstock.com/downloads/get?site=amz&sku=AMZ_OV_20250623_010&file_type=csv"
url = "https://manifest-prod.bstock.com/downloads/get?site=amz&amp;sku=AMZ_OV_20250623_010&amp;file_type=csv"

response = requests.get(url)

if response.status_code == 200:
    csv_data = response.text
    print(csv_data)  # CSV content print karega
else:
    print(f"Failed to fetch CSV. Status code: {response.status_code}")