import requests
import json
import sys


def get_api_data(url):
    data = requests.get(url)
    if data.status_code != 200:
        print(f'Request to url {url} failed.')
        sys.exit()
    return json.loads(data.text)

def put_new_person():
    url = "http://127.0.0.1:5000/v2/create"

    name = input('What is your name? ')

    created_person = {"id": 0,
                      "posted_by": 0,
                      "likes": 0,
                      "dislikes": 0,
                      "first_name": name,
                      "last_name": "Andersson",
                      "age": 34}




def main():
    name = input('What is your name? ')
    age_url = 'https://api.agify.io?name=' + name
    gender_url = 'https://api.genderize.io?name=' + name
    nation_url = 'https://api.nationalize.io?name=' + name
    age = get_api_data(age_url)['age']
    gender = get_api_data(gender_url)['gender']
    nation = get_api_data(nation_url)['country'][0]['country_id']

    country_url = 'https://restcountries.com/v3.1/alpha/' + nation.lower()

    country_info = get_api_data(country_url)
    country = country_info[0]['name']['common']

    print(f'Hello {name}. My guess is that you are {gender} and {age} years old. I think you are from {country}.')


if __name__ == '__main__':
    main()