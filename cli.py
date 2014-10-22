import click

@click.command()
@click.argument('cmd')
def hello(cmd):
    print('Hello {0}!'.format(cmd))
    
if __name__ == '__main__':
    hello()