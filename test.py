import numpy as np


# Convert contract details into dictionary
{key: getattr(cds[0].contract, key) for key in Contract.defaults}

# Convert more contract details into dictionary and get company name
{key: getattr(cds[0], key) for key in ContractDetails.defaults}['longName']
