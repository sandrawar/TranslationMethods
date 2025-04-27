import xml.etree.ElementTree as ET

# Load the .tmx file
tree = ET.parse('eng-pol_corpus.tmx')
root = tree.getroot()

# Register the 'xml' namespace
namespace = {'xml': 'http://www.w3.org/XML/1998/namespace'}

# Open output files
source_file = open('train.en', 'w', encoding='utf-8')
target_file = open('train.pl', 'w', encoding='utf-8')

# Extract source and target texts
for tu in root.findall('.//tu'):
    source = tu.find("./tuv[@xml:lang='en']/seg", namespaces=namespace).text
    target = tu.find("./tuv[@xml:lang='pl']/seg", namespaces=namespace).text
    if source and target:
        source_file.write(source.strip() + '\n')
        target_file.write(target.strip() + '\n')

# Close files
source_file.close()
target_file.close()

print("TMX file successfully converted to train.en and train.pl!")
