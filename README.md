# AWSRoleChainDetector
This tool will search in your AWS policies for any role chian that can lead to persistent access.

# Requiermnets
Install networkx and matplotlib
```
pip install networkx
pip install matplotlib
```

# Usage
```
python role_chain_detector.py --accesskey {YOUR_AWS_ACCESS_KEY} --secretkey {YOUR_AWS_SECRET_KEY}

Found juggling role: ['arn:aws:iam::855543857173:role/RoleA', 'arn:aws:iam::855543857173:role/RoleB', 'arn:aws:iam::855543857173:role/RoleC']
```

# Show Graph
Add the flag `--graph` to show the chain over graph
