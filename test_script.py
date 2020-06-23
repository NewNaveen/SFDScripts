import re
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

with open("../regex/output.txt", 'r') as f:
    data = f.read()
    regex = re.findall(r'\d*\.\d*\.\d*\.\d*', data)
    del regex[0]
    print(regex)
