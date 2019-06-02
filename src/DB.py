from cloudant import CouchDB
import config

def connectClient():
    client = CouchDB(config.username, config.password, url=config.url,
                     connect=True,
                     auto_renew=True)
    return client


def initdb():
    client = connectClient()
    db = client[config.database]
    return db


class DB():
    def __init__(self):
        self.db = initdb()
        if self.db.exists():
            print('DEBUG:New DB!')
        else:
            print('DEBUG:Can not connect db')


    def isExist(self, username):
        result = username in self.db
        return result

    def findDoc(self, username):
        return self.db[username]

    def newDoc(self, doc):
        doc = self.db.create_document(doc)
        return  doc.exists()
