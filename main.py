import requests
import json
import base64
import click

class UserInfo(object):
    def __init__(self, gh_auth):
        response = requests.get('https://api.github.com/user', headers=gh_auth.auth_header)
        v = json.loads(response.text)
        self.login = v['login']
        
    
class Gists(list):
    def __init__(self, gh_auth):
        response = requests.get('https://api.github.com/gists', headers=gh_auth.auth_header)
        v = json.loads(response.text)
        self.extend(v)
        
class Repos(object):
    def __init__(self, gh_auth):
        self.gh_auth = gh_auth
        
    def create(self, repo_name):
        response = requests.post('https://api.github.com/user/repos', data=json.dumps({'name': repo_name}), headers=self.gh_auth.auth_header)
        v = json.loads(response.text)
        print(response.text)
        return 'Repo {0} created, add a remote for {1}'.format(v['full_name'], v['ssh_url'])
    
class GHAuth(object):
    def __init__(self):
        f = open('auth', 'r')
        lines = f.readlines()
        gh_access_token = lines[0].strip()
        self.auth_header = {'Authorization': b'Basic ' + base64.b64encode(bytes(gh_access_token, 'UTF-8'))} 
        
class GithubClient(object):
    def __init__(self):
        self.gh_auth = GHAuth()
        
    def run_cmd(self, cmd, subcmd, param):
        if cmd == 'userinfo':
            print(UserInfo(self.gh_auth).login)
        elif cmd == 'listgist':
            print('\n'.join([gist['description'] for gist in Gists(self.gh_auth)]))
        elif cmd == 'repos':
            repos = Repos(self.gh_auth)
            if subcmd == 'create':
                print(repos.create(param))
    
@click.command()
@click.argument('cmd')
@click.argument('subcmd')
@click.argument('param')
def app(cmd, subcmd, param):
    gh_client = GithubClient()
    gh_client.run_cmd(cmd, subcmd, param)
    
if __name__ == '__main__':
    app()