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

    announcement_id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    image = Column(Text)

class Club(Base):
    __tablename__ = 'clubs'

    club_id = Column(Integer, primary_key = True)
    name = Column(Text)
    description = Column(Text)
    image = Column(Text)
    coffee_chat_link = Column(Text)

class ClubAnnouncement(Base):
    __tablename__ = 'club_announcements'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    announcement_id = Column(Integer, ForeignKey('announcements.announcement_id'), primary_key=True)

    user = relationship('User', backref='club_announcements')
    announcement = relationship('Announcement', backref='club_announcements')

class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key = True)
    name = Column(Text)
    location = Column(Text)
    description = Column(Text)
    start_time = Column(Text)
    end_time = Column(Text)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(Text)
    netid = Column(Text)
    profile_pic = Column(Text)

    # favorite_clubs = Column(ARRAY(Integer), ForeignKey('clubs.club_id'))
    # events = Column(ARRAY(Integer), ForeignKey('events.event_id'))
    # # Define relationships
    # clubs = relationship('Club', foreign_keys=[favorite_clubs])
    # event = relationship('Event', foreign_keys=[events])

def get_announcements():
    with sqlalchemy.orm.Session(engine) as session:
        return session.query(Announcement).all() # Select * from announcements

def get_clubs():
    with sqlalchemy.orm.Session(engine) as session:
        return session.query(Club).all() # Select * from clubs

def get_club_announcements():
    with sqlalchemy.orm.Session(engine) as session:
        return session.query(ClubAnnouncement).all()
    
def get_events():
    with sqlalchemy.orm.Session(engine) as session:
        return session.query(Event).all() # Select * from events

def get_users():
   with sqlalchemy.orm.Session(engine) as session:
        return session.query(User).all() # Select * from users
   
def create_announcement(announcement_id=None, title=None, description=None, image=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_announcement = Announcement(announcement_id=announcement_id, title=title, description=description, image=image)
        session.add(new_announcement)
        session.commit()

def create_club(club_id=None, name=None, description=None, image=None, coffee_chat_link=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_club = Club(club_id=club_id, name=name, description=description, image=image, coffee_chat_link=coffee_chat_link)
        session.add(new_club)
        session.commit()

def create_club_announcement(user_id=None, announcement_id=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_club_announcement = ClubAnnouncement(user_id=user_id, announcement_id=announcement_id)
        session.add(new_club_announcement)
        session.commit()
       
def create_event(event_id=None, name=None, location=None, description=None, start_time=None, end_time=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_event = Event(event_id=event_id, name=name, location=location, description=description, start_time=start_time, end_time=end_time)
        session.add(new_event)
        session.commit()

def create_user(user_id=None, name=None, netid=None, profile_pic=None):
    with sqlalchemy.orm.Session(engine) as session:
        new_user = User(user_id=user_id, name=name, netid=netid, profile_pic=profile_pic)
        session.add(new_user)
        session.commit()
 
def main():
    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        clubs = get_clubs()
        for club in clubs:
            print(f"Club ID: {club.club_id}")
            print(f"Name: {club.name}")
            print(f"Description: {club.description}")
            print(f"Image: {club.image}")
            print(f"Coffee Chat Link: {club.coffee_chat_link}")
            print()  
        
        create_user(user_id = 7, name = "Johnny", netid="jr___")
        create_announcement(announcement_id=4, title="Test2")
        create_club_announcement(user_id=7, announcement_id=4)

        club_announcements = get_club_announcements()
        for club_announcement in club_announcements:
            print(club_announcement.user_id, club_announcement.announcement_id)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
