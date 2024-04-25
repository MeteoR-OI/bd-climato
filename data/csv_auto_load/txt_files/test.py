POSTE :  97402240
DATE :  2024041814

RR1 :  0.0
QRR1 :  t
T :  24.2
QT :  t
TD :  18.2
QTD :  t
TN :  24.1
QTN :  t
HTN :  1301
QHTN :  t
TX :  25.5
QTX :  t
HTX :  1315
QHTX :  t
PSTAT :  None
QPSTAT :  None
PMER :  None
QPMER :  None
PMERMIN :  None
QPMERMIN :  None
FF :  5.6
QFF :  t
DD :  120
QDD :  t
FXI :  11.6
QFXI :  t
DXI :  120
QDXI :  t
HXI :  1323
QHXI :  t
U :  69
QU :  t
UN :  61
QUN :  t
HUN :  1340
QHUN :  t
UX :  69
QUX :  t
HUX :  1400
QHUX :  t
GLO :  257
QGLO :  t

# Field names
fieldNames = [
    "POSTE",
    "DATE",
    "RR1",
    "QRR1",
    "T",
    "QT",
    "TD",
    "QTD",
    "TN",
    "QTN",
    "HTN",
    "QHTN",
    "TX",
    "QTX",
    "HTX",
    "QHTX",
    "PSTAT",
    "QPSTAT",
    "PMER",
    "QPMER",
    "PMERMIN",
    "QPMERMIN",
    "FF",
    "QFF",
    "DD",
    "QDD",
    "FXI",
    "QFXI",
    "DXI",
    "QDXI",
    "HXI",
    "QHXI",
    "U",
    "QU",
    "UN",
    "QUN",
    "HUN",
    "QHUN",
    "UX",
    "QUX",
    "HUX",
    "QHUX",
    "GLO",
    "QGLO"
]

#  field values
fieldValues = [
    97402240,
    2024041814,
    0.0,
    "t",
    24.2,
    "t",
    18.2,
    "t",
    24.1,
    "t",
    1301,
    "t",
    25.5,
    "t",
    1315,
    "t",
    None,
    None,
    None,
    None,
    None,
    None,
    5.6,
    "t",
    120,
    "t",
    11.6,
    "t",
    120,
    "t",
    1323,
    "t",
    69,
    "t",
    61,
    "t",
    1340,
    "t",
    69,
    "t",
    1400,
    "t",
    257,
    "t"
]

i = 0
while i < len(fieldNames):
    print(fieldNames[i], ": ", fieldValues[i])
    i+=1
