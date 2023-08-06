# cfcli getfacts --format yaml
# cfcli deletefact --id asdasdas --format jsonll

import argparse
import sys
import requests

class Cfcli(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='CLI to query catfacts API',
            usage='''cf <command> [<args>]

The most commonly used cf commands are:
  getfacts     Get cat facts from the API
  deletefact   Delete a cat fact 
''')

        parser.add_argument('command', help='Subcommand to run')

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def getfacts(self):
        parser = argparse.ArgumentParser(description='Get cat facts')

        # prefixing the argument with -- means it's optional
        parser.add_argument('--format')
        parser.add_argument('--firstname')
        parser.add_argument('--lastname')
        parser.add_argument('--id')
        
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print('Displaying cat facts in {} format'.format(args.format))
        print("=======================================================")
        
         # Create a params dict to hold query parameters
        params = {}
        params['firstname'] = args.firstname
        params['lastname'] = args.lastname
        params['id'] = args.id
        print("params is",params)

        # contruct the payload dict 
        payload = {k: v for k, v in params.items() if v is not None}
        print("payload is",payload)

        URL = 'http://127.0.0.1:5000/api/v1/catfacts'
        response = requests.get(URL, params=payload)
        if response.status_code == 200:
            print(response.json())
        
        if response.status_code == 404:
            print("No catfact found matching criteria")

    def deletefact(self):
        parser = argparse.ArgumentParser(description='Delete cat fact')

        parser.add_argument('--id', required=True)
        args = parser.parse_args(sys.argv[2:])
        print('Attempting to delete catfact with id: {}'.format(args.id))

        # check if catfact exists, If yes? then delete, else tell end user that you cant find
        URL = 'http://127.0.0.1:5000/api/v1/catfacts'
        response = requests.delete(URL, params={"id": args.id})
        if response.status_code == 202:
            print("Catfact ID {} successfully deleted".format(args.id))
        
        if response.status_code == 404:
            print("Catfact ID {} not found".format(args.id))
        

if __name__ == '__main__':
    Cfcli()