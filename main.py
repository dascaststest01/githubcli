import requests
import json
import base64
import click

gh_access_token = ''

def create_auth_header():
    global gh_access_token
    headers = {'Authorization': b'Basic ' + base64.b64encode(bytes(gh_access_token, 'UTF-8'))}
    return headers
    

    
def ghapi_gist():
    response = requests.get('https://api.github.com/gists', headers=create_auth_header())
    return response.text
    
    
def get_user_gists():
    v = json.loads(ghapi_gist())
    return '\n'.join([gist['description'] for gist in v])
    
    
class UserInfo(object):
    def __init__(self, gh_auth):
        response = requests.get('https://api.github.com/user', headers=gh_auth.auth_header)
        print(gh_auth.auth_header)
        v = json.loads(response.text)
        self.login = v['login']
        
    
class Gists(object):
    def __init__(self):
        pass
    
class GHAuth(object):
    def __init__(self):
        f = open('auth', 'r')
        lines = f.readlines()
        gh_access_token = lines[0].strip()
        self.auth_header = {'Authorization': b'Basic ' + base64.b64encode(bytes(gh_access_token, 'UTF-8'))} 
        
class GithubClient(object):
    def __init__(self):
        self.gh_auth = GHAuth()
        
    def run_cmd(self, cmd):
        if cmd == 'userinfo':
            print(UserInfo(self.gh_auth).login)
        elif cmd == 'listgist':
            print('\n'.join([gist['description'] for gist in Gists(self.gh_auth)]))
    
@click.command()
@click.argument('cmd')
def app(cmd):
    gh_client = GithubClient()
    gh_client.run_cmd(cmd)
    
if __name__ == '__main__':
    app()