import requests


class FactService:
    """Just your basic class that can pull in data from a few api endpoints and do a basic task."""

    def get_cat(self):
        response = requests.get('https://cat-fact.herokuapp.com/facts/random')
        return response.json()['text']

    def get_buzzword(self):
        response = requests.get('https://corporatebs-generator.sameerkumar.website/')
        return response.json()['phrase']

    def get_norris(self):
        response = requests.get('https://api.chucknorris.io/jokes/random')
        return response.json()['value']

    def do_task(self, data, **kwargs):
        if "fact" not in data:
            raise Exception("No Fact Provided.")
        else:
            fact = data["fact"]

        if fact.type == "cat":
            fact.details = self.get_cat()
        elif fact.type == "norris":
            fact.details = self.get_norris()
        elif fact.type == "buzzword":
            fact.details = self.get_buzzword()
        else:
            fact.details = "unknown fact type."
        print("The fact is : " + fact.type + " --> " + fact.details)
