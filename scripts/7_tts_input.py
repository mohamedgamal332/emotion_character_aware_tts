import os
from transformers import pipeline
import json


speakers = {'M': ['9017', '6097', '6671', '6670', '1018', '101', '1025', '1027', '1028', '1034', '1040', '1046', '1049', '1058', '1065', '107', '1081', '1085', '1094', '1096', '1097', '1107', '1110', '1112', '1121', '1132', '1160', '1161', '1165', '1175', '1179', '1182', '1184', '1187', '118', '119', '1200', '1222', '1225', '1226', '122', '1230', '1235', '1239', '1258', '1260', '1261', '1265', '1271', '1274', '127', '1280', '1283', '128', '1311', '1313', '1323', '1331', '1334', '1336', '133', '1341', '1347', '1349', '1353', '1355', '1365', '1367', '1374', '1379', '1384', '1387', '1392', '1403', '1430', '1444', '1445', '1455', '1469', '147', '1485', '1487', '1492', '1494', '1495', '1505', '1513', '152', '1535', '1536', '153', '154', '1552', '1556', '1559', '1571', '1572', '1594', '1595', '159', '1601', '1603', '1607', '1614', '1618', '161', '1621', '1624', '1639', '163', '1643', '1645', '1646', '1647', '167', '1685', '168', '1699', '1708', '1743', '1746', '1748', '1769', '176', '1772', '1777', '1780', '1789', '1795', '1801', '1811', '1815', '1826', '1828', '1844', '1846', '1849', '1867', '1868', '1870', '1874', '1878', '1903', '1913', '1924', '1938', '1943', '196', '1985', '1987', '1989', '2001', '2002', '2003', '2012', '2013', '201', '2021'], 
            'F': ['8051', '11614', '9136', '11697', '92', '12787', '1006', '1012', '102', '103', '104', '1050', '1051', '1052', '1061', '1066', '1069', '1079', '1084', '1088', '1092', '1093', '1098', '110', '1116', '111', '1124', '112', '1152', '1154', '1166', '1168', '1171', '1183', '1195', '1224', '123', '1246', '1250', '1252', '1259', '125', '1263', '1266', '126', '1291', '1296', '1298', '1335', '1342', '1343', '1363', '1370', '1373', '1414', '1417', '1421', '1422', '1425', '1447', '1448', '1460', '1463', '1474', '1498', '1502', '1509', '150', '151', '1544', '1545', '1547', '1553', '1563', '1564', '1566', '1569', '1578', '1579', '1593', '1633', '1636', '1641', '1648', '1653', '1664', '1665', '1668', '1674', '1679', '1680', '1681', '1690', '1691', '1693', '1695', '1696', '16', '1704', '1705', '1710', '1714', '1717', '1721', '1726', '1731', '1733', '1736', '1737', '173', '1750', '1754', '1756', '1757', '175', '1760', '1765', '1767', '1773', '1779', '177', '1784', '1804', '1809', '1813', '1819', '1825', '1841', '1851', '1859', '1863', '1885', '188', '1898', '1901', '1920', '1923', '1926', '1931', '1944', '1963', '1968', '1970', '1974', '1977', '198', '1992', '199', '19', '2004', '2007', '200', '2010', '2026']}


with open(r"..\temp\character-attribution.json", 'r') as file:
    sentences = json.load(file)

with open(r"..\temp\gender.json", 'r') as file:
    characters = json.load(file)

characters_to_speakers = {}
for i in characters:
    if i[0] not in characters_to_speakers.keys():
        id_list = speakers.get(i[1])
        for id in id_list:
            if id not in characters_to_speakers.values():
                characters_to_speakers[i[0].lower()] = id
                break
        else:
            characters_to_speakers[i[0].lower()] = id_list[-1]


classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

labeled_sentences = []
for i in sentences:
    sentiment_output = classifier(i[0])
    score = [label['score'] for emotion in sentiment_output for label in emotion]
    labels = [label['label'] for emotion in sentiment_output for label in emotion]
    
    labeled_sentences.append([i, labels[score.index(max(score))]])

final_list = []
for i in range(len(labeled_sentences)):
   final_list.append([(labeled_sentences[i][0][0], characters_to_speakers[labeled_sentences[i][0][1].lower()]), labeled_sentences[i][1]])

print(final_list)
def save_data_to_json(data, filename):
  """Saves the given data to a JSON file.

  Args:
      data (list): The data to write.
      filename (str): The name of the JSON file.
  """
  try:
    with open(filename, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data successfully written to {filename}")
  except Exception as e:
    print(f"Error saving data to JSON: {e}")

output_filename = os.path.join("..", "temp", "tts_input.json")
save_data_to_json(final_list, output_filename)