import requests
import json
import urllib.parse as ul


def get_response(url):
    username = 'eserfeliz'
    personal_token = 'b550bde24f05577b125088c861e42647ff2137f0'
    return requests.get(url, auth=(username, personal_token))


def get_json(url):
    return json.loads(get_response(url).text)


valid_url_prefix = 'api.github.com/orgs/BoomTownROI'
initial_url = 'https://' + valid_url_prefix

urls = {}        # Initialize dict of urls
id_results = []  # Initialize list of id_results

num_public_repos = 0
length_of_repo_list = 0
created_dt = ''
updated_dt = ''

# Collect top level organizational details via API
org_tld = get_json(initial_url)

# Separate organizational top level details into key/value pairs
for org_tld_k, org_tld_v in org_tld.items():
    # Check URLs in top level details to flag URLs to be followed
    if valid_url_prefix in str(org_tld_v) and org_tld_k != 'url':
        urls.update({org_tld_k: org_tld_v})
    # Get number of public repos for verification
    if 'public_repos' in org_tld_k:
        num_public_repos = org_tld['public_repos']
    if 'created_at' in org_tld_k:
        created_dt = org_tld['created_at']
    if 'updated_at' in org_tld_k:
        updated_dt = org_tld['updated_at']

# For each required BoomTown URL in top level details, generate a new request
# Consider each resource only returns 30 objects in the default query
# URLs returning status codes of 200 should display id key/value pairs in its response
# Status codes not equal to 200 should indicate which type of failure occurred

for url_value in urls.values():
    id_results = get_json(url_value)

    response = get_response(url_value)
    if response.status_code == 200:
        link = response.headers.get('link', None)
        links = link.split(',')
        url = ''

        # Github will respond with links to the next and last pages of information. These can be utilized for traversal
        # rather than building the query manually. If there are multiple pages, continue traversing until "next" no
        # longer appears in the response header.

        while 'next' in response.links.keys():
            for data in links:
                if 'rel="next"' in data:
                    url = link[link.find("<") + 1:link.find(">")]

            response = get_response(url)
            id_results.extend(json.loads(response.text))
            link = response.headers.get('link', None)

        for item in id_results:
            if 'type' not in item:  # if result is a repo item
                length_of_repo_list = len(id_results)
                try:
                    print("Repo id: {}\nRepo name: {}\n".format(item['id'], item['name']))
                except KeyError:
                    pass
            else:
                try:
                    print("Event id: {}\nEvent type: {}".format(item['id'], item['type']))
                    actor = item['actor']
                    print("Authenticated user: {}\n".format(actor['login']))
                    repo = item['repo']
                    print("Repo id (nested): {}\nRepo name: {}".format(repo['id'], repo['name']))
                except TypeError:
                    pass
    else:
        print('Request to ' + ul.unquote(str(response.url)) + ' failed with a status code of ' +
              str(response.status_code))

created_updated_validation = True if updated_dt >= created_dt else False
num_public_repos_validation = True if num_public_repos == length_of_repo_list else False

print('\nVerification:\n')
print('The date the organization was updated (' + updated_dt + ') is ' +
      ('the same or later' if created_updated_validation else 'earlier')
      + ' than the date the organization was created (' + created_dt + ')'
      + (' - PASS' if created_updated_validation else ' - FAIL') + '\n')
print('The number of public repos reported via the top level organizational details (' + str(num_public_repos) + ') is '
      + ('equal to' if num_public_repos_validation else 'not equal to') + ' the length of the repo list (' +
      str(length_of_repo_list) + ')' + (' - PASS' if num_public_repos_validation else ' - FAIL'))
