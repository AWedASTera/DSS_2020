import json
import os
import requests
import urllib.request

def get_image_description(url):
    res = ''
    # get and save image by url
    urllib.request.urlretrieve(url, "blah/img.jpg")

    # start network
    os.system(' python3 tools/eval.py --model model.pth --infos_path infos.pkl --image_folder blah --num_images -1 --device cpu --language_eval 0')

    #
    with open('vis/vis.json') as json_file:
        data = json.load(json_file)
        res = data[0]["caption"]
    # del
    os.system('del eval_results/.saved_pred_fc_test.pth')
    os.system('del blah/img.jpg')

    return res


if __name__ == "__main__":
    dfdata = []
    with open("data_file.json", "r") as read_file:
        dfdata = json.load(read_file)
    if dfdata is not None:
        while not analyze_done:
            try:
                print("Waining for ai analyze")
                for post in dfdata:
                    for photo in dfdata["photos"]:
                        photo["description"] = ai_analyze(photo["url"])
                analyze_done = True
            except Exception:
                print("Something went wrong!")
        print("Analyzed")
    else:
        print("Something went wrong!")
    with open("data_file.json", "w") as write_file:
        json.dump(dfdata, write_file)