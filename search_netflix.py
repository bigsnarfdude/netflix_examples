import netflix

api_key = "bfddvnduhs3xxyhxpf5x9sue"
api_secret="7BZZdYt4GS"

def get_answer():
    answer = raw_input("Netflix Search Term please? ")
    api = netflix.NetflixAPI(api_key, api_secret)
    result = api.get("catalog/titles/autocomplete", { "term" : answer })

    for t in result["autocomplete"]["autocomplete_item"]:
        print t["title"]["short"]

get_answer()

