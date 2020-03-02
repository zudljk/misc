#!/usr/bin/env python3

from os import path
from os import system
from os import environ
from os import remove
import sys
from datetime import date

from relatorio.templates.opendocument import Template


libreOfficePath = path.join("/", "Applications", "LibreOffice.app", "Contents", "MacOS", "soffice")
documents = path.join(environ['HOME'], "Documents", "Dropbox")
outputDir = path.join(documents, "Inbox", "PDF", "4 - manuell prüfen")
contracts = sys.argv[1:]

if len(contracts) < 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage:")
    print(sys.argv[0] + " contractnumber...")
    print("""Revocate premium rise for MLP contract

Options:
-h, --help\tShow help
""")
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

outputFile = "MLP"

for contract in contracts:
    c = {'key': contract, 'name': contractData[contract]}
    templateData['contracts'].append(c)
    outputFile = outputFile + "_" + contract

outputFile = outputFile+"_"+date.today().strftime("%Y%m%d")+"_ErhoehungWiderspruch"

basic = Template(source='', filepath=path.join(documents, 'Org', 'versicherung', 'mlp-erhoehung-widerspruch-template.odt'))
basic_generated = basic.generate(o=templateData).render()

open(outputFile+".odt", 'wb').write(basic_generated.getvalue())

system(libreOfficePath + ' --convert-to pdf --outdir "'+outputDir+'" '+outputFile+'.odt')

remove(outputFile+".odt")

system('open "'+path.join(outputDir, outputFile+'.pdf')+'"')
system("open https://web.de")
