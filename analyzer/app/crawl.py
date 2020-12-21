from elasticsearch import Elasticsearch
import json
from datetime import datetime

host = 'host.docker.internal'
port = 9200
index = "wall_posts"
client = Elasticsearch([{'host': host, 'port': port}])
elastic_done = False
dfdata = []


def collect_prepare_data(client, index_):
	global elastic_done
	print("Waiting for Elastic to init")
	while not elastic_done:
		try:
			info = json.dumps(client.info(), indent=4)
			print("Elasticsearch client info():", info)
			elastic_done = True
		except ConnectionError as err:
			print ("\nElasticsearch info() ERROR:", err)
			print ("\nThe client host:", host, "is invalid or cluster is not running")
			client = None
	dfdata = None
	if client != None:
		print("Waiting for Elastic to load data")
		elastic_done = True
		number_rows = 0
		while number_rows == 0:
			try:
				resp = client.search(
					index = index_,
					params = {"size" : 0}
				)
				number_rows = int(resp["hits"]["total"]["value"])
			except Exception:
				continue
		if number_rows != 0:
			resp = client.search(
				index = index_,
				params = {"size" : number_rows}
			)
			dfdata = []
			for el in resp['hits']['hits']:
				geo = ""
				photos=[]
				if "attachments" in el["_source"]:
					for a in el["_source"]["attachments"]:
						if "photo" in a:
							photo={"url": a["photo"]["sizes"][2]["url"], "description": ""} # [2] means p as format of vk's image (max_side = 200px)
							photos.append(photo)
				dfdata.append({"timestamp": datetime.fromtimestamp(el["_source"]["date"]).strftime("%d-%m-%Y (%H:%M:%S)"), "text": el["_source"]["text"], "photos": photos, "toponymes": [], "geo": geo}) 
	return dfdata




if __name__ == "__main__":
    data = collect_prepare_data(client, index)
    with open("data_file.json", "w") as write_file:
        json.dump(data[0:9], write_file)