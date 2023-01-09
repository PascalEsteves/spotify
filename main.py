import json
import pandas as pd
from connection import CONECTION


def main():

    file = open('config.json','utf-8')
    config = json.load(file)

    connection = CONECTION(config)

