# linkace_csv_to_linkwarden_json

Simple python script to convert a [LinkAce](https://www.linkace.org/) [(GitHub)](https://github.com/Kovah/LinkAce/) csv export file into a json file to import with [Linkwarden](https://linkwarden.app/) [(GitHub)](https://github.com/linkwarden/linkwarden)

## Description

The script reads all lines from the csv file using the basic csv python library. They are then converted into the respective dataclasses for the Linkwarden json format.
Using the basic json library, these are then dumped into a json file ready for import to Linkwarden.  
Basic data needs to be provided in a file, the default is 'user_inputs.txt'. Minimal data is at least name and username. More can be provided as seen in the default file. Line can be commented with #.  
The datastructure is slightly different between the two application formats. Mainly, in LinkAce links can be part of multiple lists, but in Linkwarden the can only be part of one collection. Furthermore in LinkAce there is no need for a link to be part of a list, but in Linkwarden every link needs to be part of a collection.  
This leads to some loss of information if links are associated with multiple list in LinkAce. The script will convert all lists into collection but links will only be added to the last collection they are associated with (they could possibly be added to all collections instead, but that results in a lot of duplicate links).  
But tags work just the same in both applications, so no issues there.

## Getting Started

### Dependencies

* Python with csv, json, string, dataclass and datetime libraries
* Version 3.12.0 has all of them built in

### Installing

* Clone the git repository or download converter.py and user_inputs.txt

### Executing program

* In LinkAce use the 'Export to CSV' tool (Click the username on the top right > Export > Export to CSV)
* Copy your LinkAce_export.csv file to the same folder as the script or change 'linkaceFilename' in the script to your file path
* Change data in the user_inputs file
* Run the script
* File named backup.json is created
* Import backup.json into Linkwarden (Settings > Import From > From Linkwarden)

## Authors

Paul Wilk  
[Mail](mailto:opensource@wilkmail.de)

## Version History

* 1.0
    * Initial Release