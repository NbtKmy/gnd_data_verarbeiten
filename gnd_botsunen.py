# -*- coding: utf-8 -*-
import pandas as pd
import gzip
import json
import argparse


parser = argparse.ArgumentParser('GND parser')
parser.add_argument('-i', '--input', help='input file name (without .txt.gz)', type=str, required=True)
parser.add_argument('-o', '--output', help='output file name (without .csv)', type=str, required=True)




def createCsvFile(inputFileName, outputFileName):

    with gzip.open(inputFileName, mode='rt', encoding='utf-8') as f:
        data = f.read()

    persons = data.split('\n')

    '''
    dateOfBirth[0] -> die Daten ist als List geschrieben wie ["1852"]. Hier wird das erst genannte Datum genommen.
    id -> "https://d-nb.info/gnd/13226854X" als URL 
    preferredName -> ist in der Form "Weber, Max" eingetragen.
    biographicalOrHistoricalInformation[0] -> als Liste eingetragen. Es wird hier nur der erste Eintrag mitgenommen, wenn vorhanden 
    '''

    
    array_dob = [] # dob = date of birth
    array_ident = []
    array_name = []
    array_bio = []


    for x in persons:

        # Das letzte Objekt der Liste "persons" ist leer. Deshalb wird das leere Objekt übersprungen
        if len(x) == 0:
            continue
        
        # x wird zuerst als Dict-Objekt gelesen
        x = json.loads(x)

        dob = x['dateOfBirth'][0]
        ident = x['id']

        if 'biographicalOrHistoricalInformation' in x:
            bio = x['biographicalOrHistoricalInformation'][0]
        else:
            bio = None

        n = x['preferredName']
        comma_index = n.find(',')
        if comma_index == -1:
            name = n
        else:
            Nachname = n[:comma_index]
            Vorname = n[comma_index+2:]
            name = Vorname + ' ' + Nachname

        array_dob.append(dob)
        array_ident.append(ident)
        array_bio.append(bio)
        array_name.append(name)

    ser_dob = pd.Series(array_dob, name='date of birth')
    ser_ident = pd.Series(array_ident, name='id')
    ser_bio = pd.Series(array_bio, name='biographical information')
    ser_name = pd.Series(array_name, name='name')

    res = pd.concat([ser_name, ser_dob, ser_bio, ser_ident], axis=1)
    res.to_csv(outputFileName)
    

if __name__ =='__main__' :
    args = parser.parse_args()

    input = args.input
    inputFileName = input + '.txt.gz'
    
    output = args.output
    outputFileName = output + '.csv'

    createCsvFile(inputFileName, outputFileName)
