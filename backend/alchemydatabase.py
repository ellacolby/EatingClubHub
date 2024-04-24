import os
import sys
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.environ['ALCHEMY_DATABASE_URL']

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Announcement(Base):
    __tablename__ = 'announcements'

    announcement_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    description = Column(Text)
    image = Column(Text)

class ClubAnnouncement(Base):
    __tablename__ = 'club_announcements'

    user_id = Column(Text, ForeignKey('users.user_id'), primary_key=True)
    announcement_id = Column(Integer, ForeignKey('announcements.announcement_id'), primary_key=True)

    user = relationship('User', backref='club_announcements')
    announcement = relationship('Announcement', backref='club_announcements')


class ClubEvent(Base):
    __tablename__ = 'club_events'

    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)

    club = relationship('Club', backref='club_events')
    event = relationship('Event', backref='club_events')

class Club(Base):
    __tablename__ = 'clubs'

    club_id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(Text)
    description = Column(Text)
    image = Column(Text)
    coffee_chat_link = Column(Text)

class EventAttendee(Base):
    __tablename__ = 'event_attendees'

    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)
    user_id = Column(Text, ForeignKey('users.user_id'), primary_key=True)

    event = relationship('Event', backref='event_attendees')
    user = relationship('User', backref='event_attendees')

class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(Text)
    location = Column(Text)
    description = Column(Text)
    start_time = Column(Text)
    end_time = Column(Text)

class FavoriteClub(Base):
    __tablename__ = 'favorite_clubs'

    user_id = Column(Text, ForeignKey('users.user_id'), primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    user = relationship('User', backref='favorite_clubs')
    club = relationship('Club', backref='favorite_clubs')

class Officer(Base):
    __tablename__ = 'officers'

    user_id = Column(Text, ForeignKey('users.user_id'), primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    user = relationship('User', backref='officers')
    club = relationship('Club', backref='officers')

class UserEvent(Base):
    __tablename__ = 'user_events'

    user_id = Column(Text, ForeignKey('users.user_id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)

    user = relationship('User', backref='user_events')
    event = relationship('Event', backref='user_events')

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Text, primary_key=True)
    name = Column(Text)
    netid = Column(Text)
    profile_pic = Column(Text)
    pronouns = Column(Text)
    about_me = Column(Text)

def get_records(class_name):
    records = []
    with sqlalchemy.orm.Session(engine) as session:
        table_class = globals()[class_name.capitalize()]  # Get the class corresponding to the table name
        results = session.query(table_class).all()
        for result in results:
            record_tuple = tuple(getattr(result, column.name) for column in result.__table__.columns)
            records.append(record_tuple)
    return records

# def get_announcements():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(Announcement).all() 

# def get_club_announcements():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(ClubAnnouncement).all()

# def get_club_events():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(ClubEvent).all()

# def get_clubs():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(Club).all()

# def get_event_attendees():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(EventAttendee).all() 
    
# def get_events():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(Event).all() 

# def get_favorite_clubs():
#     with sqlalchemy.orm.Session(engine) as session:
#         return session.query(FavoriteClub).all() 

def get_officer_club_info(user_id):
    with sqlalchemy.orm.Session(engine) as session:
        club_id = session.query(Officer).filter(Officer.user_id == user_id).first()
        if club_id:
            club_id = club_id.club_id
        else:
            return None
        club_name = session.query(Club).filter(Club.club_id == club_id).first().name

        return club_id, club_name

def get_officers():
    with sqlalchemy.orm.Session(engine) as session:
        return session.query(Officer).all()

def get_user_events():
    with sqlalchemy.orm.Session(engine) as session:
        return session.query(UserEvent).all()

def get_users():
   with sqlalchemy.orm.Session(engine) as session:
        return session.query(User).all() 
   
def create_announcement(announcement_id=None, title=None, description=None, image=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_announcement = Announcement(announcement_id=announcement_id, title=title, description=description, image=image)
        session.add(new_announcement)
        session.commit()

def create_club_announcement(user_id=None, announcement_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_club_announcement = ClubAnnouncement(user_id=user_id, announcement_id=announcement_id)
        session.add(new_club_announcement)
        session.commit()

def create_club_event(club_id=None, event_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_club_event = ClubEvent(club_id=club_id, event_id=event_id)
        session.add(new_club_event)
        session.commit()

def create_club(club_id=None, name=None, description=None, image=None, coffee_chat_link=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_club = Club(club_id=club_id, name=name, description=description, image=image, coffee_chat_link=coffee_chat_link)
        session.add(new_club)
        session.commit()

def create_event_attendee(event_id=None, user_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_event_attendee = EventAttendee(event_id=event_id, user_id=user_id)
        session.add(new_event_attendee)
        session.commit()

def create_event(event_id=None, name=None, location=None, description=None, start_time=None, end_time=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_event = Event(event_id=event_id, name=name, location=location, description=description, start_time=start_time, end_time=end_time)
        session.add(new_event)
        session.commit()

def create_favorite_club(user_id=None, club_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_favorite_club = FavoriteClub(user_id=user_id, club_id=club_id)
        session.add(new_favorite_club)
        session.commit()

def create_officer(user_id=None, club_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_officer = Officer(user_id=user_id, club_id=club_id)
        session.add(new_officer)
        session.commit()

def create_user_event(user_id=None, event_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_user_event = UserEvent(user_id=user_id, event_id=event_id)
        session.add(new_user_event)
        session.commit()

# def create_user(user_id=None, name=None, netid=None, profile_pic=None):
#     with sqlalchemy.orm.Session(engine) as session:
#         new_user = User(user_id=user_id, name=name, netid=netid, profile_pic=profile_pic)
#         session.add(new_user)
#         session.commit()

def create_user(user_id=None, name=None, netid=None, profile_pic=None, pronouns=None, about_me=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_user = User(user_id=user_id, name=name, netid=netid, profile_pic=profile_pic, pronouns=pronouns, about_me=about_me)
        session.add(new_user)
        session.commit()

def main():
    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        Base.metadata.create_all(engine)
        # create_user(user_id="test", name="test")
        # create_event(name="test", location="TigerINN")
        print(get_officer_club_info('hello'))
        # events = get_records('event')
        # for event in events:
        #     print(event)
        
            
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
