import glob
import os
import collections
import lxml.etree as ET
from slugify import slugify

from freud_api_crawler.xml import XMLReader
from freud_api_crawler.freud_api_crawler import TEI_DUMMY


def make_div_list(glob_pattern):
    """defaultdict of tei:divs fetched from XML/TEI matching the past in glob pattern
    :param glob_pattern: a glob pattern to fetch XML/TEI

    :return: default dict with grouped and ordered div-items
    :rtype: defaultdict
    """

    files = glob.glob(glob_pattern)
    divs = []
    for x in files:
        doc = XMLReader(x)
        title = doc.tree.xpath(
            ".//tei:title[@type='manifestation']/text()", namespaces=doc.nsmap
        )[0]
        pub_id = f'{doc.tree.xpath(".//tei:rs[1]/@ref", namespaces=doc.nsmap)[0]}'
        pub_title = doc.tree.xpath(".//tei:rs[1]/text()", namespaces=doc.nsmap)[0]
        for div in doc.tree.xpath(".//tei:div", namespaces=doc.nsmap):
            first_page = div.xpath(".//tei:pb[@n]/@n", namespaces=doc.nsmap)[0]
            item = {
                "title": title,
                "pub_id": pub_id,
                "pub_title": pub_title,
                "first_page": first_page,
                "div": div
            }
            divs.append(item)

    sorted_list = sorted(divs, key=lambda i: (i['pub_id'], i['title']))
    d = collections.defaultdict(list)
    for x in sorted_list:
        d[x['pub_id']].append(x)
    return d


def create_united_files(glob_pattern):
    output_dir = glob_pattern.replace("*.xml", 'merged')
    try:
        os.makedirs(output_dir)
    except Exception as e:
        pass
    d = make_div_list(glob_pattern)
    xml_obj = XMLReader(TEI_DUMMY)
    for key, value in d.items():
        slug_name = slugify(f"{value[0]['pub_title']}")
        pub_id = f"{key[7:]}"
        doc = ET.parse(TEI_DUMMY)
        save_path = os.path.join(output_dir, f"{slug_name}.xml")
        root_el = doc.xpath('//tei:TEI', namespaces=xml_obj.nsmap)[0]
        root_el.attrib["{http://www.w3.org/XML/1998/namespace}base"] = f"https://whatever.com"
        root_el.attrib[
            "{http://www.w3.org/XML/1998/namespace}id"
        ] = f"manifestation__{pub_id}"
        title = doc.xpath('//tei:title[@type="manifestation"]', namespaces=xml_obj.nsmap)[0]
        t_p = doc.xpath('//tei:title[@type="publication"]', namespaces=xml_obj.nsmap)[0]
        t_p.text = f"{value[0]['pub_title']}"
        body = doc.xpath('//tei:body', namespaces=xml_obj.nsmap)[0]
        for item in value:
            body.append(item['div'])
        with open(f'{save_path}', 'wb') as f:
            f.write(ET.tostring(doc, encoding="UTF-8"))
    return (output_dir, d)
