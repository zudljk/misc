#!/usr/bin/env python3

from relatorio.templates.opendocument import Template
import sys
import os
from datetime import date


def usage():
    print("Usage:")
    print(sys.argv[0] + " contractnumber...")
    print("""Revocate premium rise for MLP contract

Options:
-h, --help\tShow help
""")


contracts = sys.argv[1:]

if len(contracts) < 1:
    usage()
    sys.exit(1)

contractData = {
    '02': 'MLP bestpartner topinvest fondsgebundene Lebensversicherung',
    '04': 'MLP topinvest fondsgebundene Lebensversicherung',
    '07': 'MLP topinvest fondsgebundene Lebensversicherung',
    '08': 'MLP Titan Fondspolice',
    '09': 'MLP Tital Basisrente',
}

templateData = {
    'date': date.today().strftime("%d.%m.%Y"),
    'contracts': []
}

outputFile = "mlp-erhoehung-widerspruch_"+date.today().strftime("%Y%m")

for contract in contracts:
    c = {'key': contract, 'name': contractData[contract]}
    templateData['contracts'].append(c)
    outputFile = outputFile + "_" + contract

outputFile += ".odt"

basic = Template(source='', filepath=os.environ['HOME'] +
                                     '/Documents/Dropbox/Org/versicherung/mlp-erhoehung-widerspruch-template.odt')
basic_generated = basic.generate(o=templateData).render()

open(outputFile, 'wb').write(basic_generated.getvalue())

os.system("")