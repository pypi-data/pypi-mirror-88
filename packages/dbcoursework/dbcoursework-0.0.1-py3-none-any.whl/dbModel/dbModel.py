from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import exc

class DBModel:
    def __init__(self, dbname_, user_, password_, host_):
        self._dbname = dbname_
        self._user = user_
        self._password = password_
        self._host = host_
        try:
            self.engine = create_engine(
                "postgres://{}:{}@{}/{}".format(self._user, self._password, self._host, self._dbname))
            self.session = Session(bind=self.engine)
        except (Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            self.session.execute("ROLLBACK")
            print(error)

    def __del__(self):
        try:
            self.session.close()
        except (Exception, exc.InvalidRequestError) as error:
            self.session.execute("ROLLBACK")
            print(error)

    def add_entity(self, new_entity):
        try:
            self.session.add(new_entity)
            self.session.commit()
        except (Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            self.session.execute('ROLLBACK')
            print(error)

    def check_news(self, entity_type, news_title):
        exists = False
        try:
            exists = self.session.query(entity_type).filter_by(title=news_title).first()
            if exists is None:
                exists = False
            else:
                exists = True
        except (Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            self.session.execute('ROLLBACK')
            print(error)
        return exists

    def get_entity(self, entity_type, entity_id):
        try:
            entity = self.session.query(entity_type).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return entity

    def get_entities(self, entity_type):
        entities = None
        try:
            entities = self.session.query(entity_type)
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return entities

    def update_entity(self, update_entity):
        try:
            self.session.add(update_entity)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")


    def do_request(self , request):
        try:
            result = self.session.execute(request).fetchall()
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")
        return result