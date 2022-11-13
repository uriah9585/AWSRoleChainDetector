# !/usr/bin/env python3

import boto3
import argparse
import matplotlib.pyplot as plt
import networkx


def get_chain_path(aws_roles, graph):
    roles = [role['Arn'] for role in aws_roles]
    for role in aws_roles:
        for statement in role['AssumeRolePolicyDocument']['Statement']:
            if statement['Effect'] == "Allow" and 'AWS' in statement['Principal']:
                arns = statement['Principal']['AWS']
                if not isinstance(arns, list):
                    arns = [arns]
                for arn in arns:
                    if arn in roles:
                        graph.add_edges_from([(role['Arn'], arn)])
    chain_path = list(networkx.simple_cycles(graph))
    return chain_path


def find_role_jugglling(args):
    client = boto3.client('iam', aws_access_key_id=args.accesskey, aws_secret_access_key=args.secretkey,)
    aws_roles = client.list_roles()['Roles']
    graph = networkx.DiGraph()
    chain_path = get_chain_path(aws_roles, graph)
    if args.graph:
        pos = networkx.spring_layout(graph)
        networkx.draw_networkx_nodes(graph, pos)
        networkx.draw_networkx_edges(graph, pos, edgelist=graph.edges())
        networkx.draw_networkx_labels(graph, pos)
        plt.show()

    for chain in chain_path:
        print(f'Found juggling role: {chain}')


def main():
    parser = argparse.ArgumentParser(description="Search for AWS role chain that can be used by attacker for persistance.")
    parser.add_argument('--accesskey', required=True, help='Set AWS access key')
    parser.add_argument('--secretkey', required=True, help='Set AWS secret key')
    parser.add_argument('--graph', required=False, help='Show role chain on graph', action='store_true')
    args = parser.parse_args()
    find_role_jugglling(args)


if __name__ == "__main__":
    main()
