import csv
import json
import string
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime, timezone

def read_user_inputs(file_path):
     with open(file_path, 'r') as input_file:
          user_inputs = {}
          for line in input_file:
               if line.startswith('#'):
                    continue
               else:
                    key, value = line.translate({ord(c): None for c in string.whitespace}).split(':', 1)
                    if value.lower() == 'true':
                         value = True
                    elif value.lower() == 'false':
                         value = False
                    user_inputs[key.lower()] = value
     return user_inputs

user_inputs_file_path = 'user_inputs.txt'
user_inputs = read_user_inputs(user_inputs_file_path)

print(f'Data from input file {user_inputs_file_path}:')

nameInput = user_inputs.get('name', '')
print(f'name is set to {nameInput}')
usernameInput = user_inputs.get('username', '')
print(f'username is set to {usernameInput}')
emailInput = user_inputs.get('email', None)
print(f'email is set to {emailInput}')
archiveAsScreenshotInput = user_inputs.get('archiveasscreenshot', True)
print(f'archiveAsScreenshot is set to {archiveAsScreenshotInput}')
archiveAsPDFInput = user_inputs.get('archiveaspdf', True)
print(f'archiveAsPDF is set to {archiveAsPDFInput}')
archiveAsWaybackMachineInput = user_inputs.get('archiveaswaybackmachine', False)
print(f'archiveAsWaybackMachine is set to {archiveAsWaybackMachineInput}')
isPrivateInput = user_inputs.get('isprivate', False)
print(f'isPrivate is set to {isPrivateInput}')

date = datetime.now().astimezone(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
print(f'date is set to {date} (current UTC time)\n')

@dataclass
class Tag:
    createdAt: str = date
    name: str = ''
    ownerId: int = 1
    updatedAt: str = date

@dataclass
class Link:
    collectionId: int = 0
    createdAt: str = date
    description: str = ''
    image: str = None
    lastPreserved: str = date
    name: str = ''
    pdf: str = None
    preview: str = None
    readable: str = None
    tags: list[Tag] = field(default_factory=list)
    textContent: str = None
    type: str = 'url'
    updatedAt: str = date
    url: str = ''
    
@dataclass
class Collection:
    color: str = '#0ea5e9'
    createdAt: str = date
    description: str = ''
    isPublic: bool = False
    links: list[Link] = field(default_factory=list)
    name: str = ''
    ownerId: int = 1
    updatedAt: str = date

@dataclass
class BackupJsonObject:
    name: str = nameInput
    username: str = usernameInput
    email: str = emailInput
    emailVerified: str = None
    image: str = None
    archiveAsScreenshot: bool = archiveAsScreenshotInput
    archiveAsPDF: bool = archiveAsPDFInput
    archiveAsWaybackMachine: bool = archiveAsWaybackMachineInput
    isPrivate: bool = isPrivateInput
    createdAt: str = date
    updatedAt: str = date
    collections: list[Collection] = field(default_factory=list)

linkaceFilename = 'LinkAce_export.csv'

backupObject = BackupJsonObject(name=nameInput, username=usernameInput, email=emailInput, collections=[])

lists = ['Unorganized']
newCollections = [Collection(name='Unorganized')]

#row[0] - id, row[1] - user_id, row[2] - url, row[3] - title, row[4] - description, row[5] - icon, row[6] - thumbnail, row[7] - is_private, row[8] - status, row[9] - check_disabled, row[10] - created_at, row[11] - updated_at, row[12] - deleted_at, row[13] - tags, row[14] - lists
with open(linkaceFilename, newline='', encoding='utf8') as csvfile:
     csv_reader = csv.reader(csvfile, delimiter=',')

     line_count = 0

     for row in csv_reader:
          if line_count == 0:
               line_count += 1
          else:
               lastCollectionId = 1
               if (row[14] != ''):
                    listNamesFromRow = row[14].split(',')
                    for listName in listNamesFromRow:
                         if listName not in lists:
                              lists.append(listName)
                              newCollections.append(Collection(name=listName))
                              lastCollectionId = len(lists)

               newTags = []
               if (row[13] != ''):
                    tagsFromRow = row[13].split(',')
                    for tag in tagsFromRow:
                         newTags.append(Tag(name=tag))
            
               link = Link(collectionId=lastCollectionId, description=row[4], name=row[3], tags=newTags, url=row[2])

               newCollections[lastCollectionId - 1].links.append(link)

               line_count += 1

     print(f'Processed the header line and {line_count - 1} link lines.')

backupObject.collections = newCollections

filename = 'backup.json'

with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(backupObject, json_file, default=lambda o: o.__dict__, indent=4)

print(f'Backup exported to {filename}')

