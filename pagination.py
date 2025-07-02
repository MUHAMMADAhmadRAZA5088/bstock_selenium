import requests
import json
urls = []

for page in range(0, 1600, 160):
  url = f"https://search.bstock.com/v1/all-listings/listings?sortBy=endTime&sortOrder=asc&offset={page}&limit=160"

  payload = {}
  headers = {

  }

  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)

  if data['listings'] == []:
      break
  for url in data['listings']:
        # if  'amazon/' in url['auctionUrl'] or 'bestbuy' in url['auctionUrl'] or 'walkeredison' in url['auctionUrl']:
        if '/buy/' not in url['auctionUrl'] and 'mobilecarrier' not in url['auctionUrl'] and 'supplystoreeurope' not in url['auctionUrl']:
            
            urls.append({"name" : url['auctionUrl'].split('.com/')[1].split('/auction')[0] ,"url":url['auctionUrl']})

sorted_data = sorted(urls, key=lambda x: x['name'])

# Print sorted result
for item in sorted_data:
    print(item)

import pdb;pdb.set_trace()
with open("output.json", "w") as f:
    json.dump(sorted_data, f, indent=4)  # indent se pretty format milta hai
