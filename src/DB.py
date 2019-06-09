from cloudant.client import CouchDB
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
        print('DEBUG:' + username + ' exists:' + str(result))
        return result

    def findDoc(self, username):
        return self.db[username]

    def newDoc(self, data):
        print(data)
        doc = self.db.create_document(data)
        return doc.exists()
