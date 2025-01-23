import xml.etree.ElementTree as ET

def parse_xspf(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Define the namespace dictionary
    ns = {'xspf': 'http://xspf.org/ns/0/', 'vlc': 'http://www.videolan.org/vlc/playlist/ns/0/'}
    
    playlist_items = []

    # Iterate through each track in the trackList and extract relevant information
    for track in root.find('xspf:trackList', ns):
        location = track.find('xspf:location', ns).text

        playlist_item = ET.Element("PlaylistItem")
        path_elem = ET.SubElement(playlist_item, "Path")
        path_elem.text = location
        
        playlist_items.append(playlist_item)

    return playlist_items

def generate_xml(output_path, playlist_items):
    root_element = ET.Element("Item")

    # Add static elements inside the Item element
    added = ET.SubElement(root_element, "Added")
    lock_data = ET.SubElement(root_element, "LockData")
    local_title = ET.SubElement(root_element, "LocalTitle")
    running_time = ET.SubElement(root_element, "RunningTime")
    owner_user_id = ET.SubElement(root_element, "OwnerUserId")
    
    # Add empty elements
    added.text = ""
    lock_data.text = ""
    local_title.text = ""
    running_time.text = ""
    owner_user_id.text = ""

    shares = ET.SubElement(root_element, "Shares")
    playlist_media_type = ET.SubElement(root_element, "PlaylistMediaType")
    playlist_media_type.text = "Audio"

    # Create PlaylistItems element and append PlaylistItem elements
    playlist_items_elem = ET.SubElement(root_element, "PlaylistItems")
    
    for item in playlist_items:
        playlist_items_elem.append(item)
    
    tree = ET.ElementTree(root_element)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

def main():
    input_file = 'input.xspf'  # Path to the XSPF file
    output_file = 'output.xml'  # Desired path for the output XML file

    playlist_items = parse_xspf(input_file)
    
    generate_xml(output_file, playlist_items)

if __name__ == "__main__":
    main()
