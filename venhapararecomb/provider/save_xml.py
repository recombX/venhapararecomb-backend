from datetime import datetime
import shutil


def save_xml(files):
    for file in files:
        if file.filename[-3:] == 'xml':
            timestamp = datetime.timestamp(datetime.now())
            with open(f"./static/xmlDocs/{timestamp}-{file.filename}", "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
