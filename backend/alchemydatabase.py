import os
import sys
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    club = relationship('Club', backref='announcements')

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

class Officer(Base):
    __tablename__ = 'officers'

    user_id = Column(Text, ForeignKey('users.user_id'), primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    user = relationship('User', backref='officers')
    club = relationship('Club', backref='officers')

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Text, primary_key=True)
    name = Column(Text)
    netid = Column(Text)
    profile_pic = Column(Text)
    pronouns = Column(Text)
    about_me = Column(Text)

def get_records(class_name):
    possible_class_names = ['User', 'Officer', 'Announcement', 'Event', 'Club']
    assert (class_name.capitalize() in possible_class_names), "Not a valid class name"

    records = []
    try:
        with sqlalchemy.orm.Session(engine) as session:
            table_class = globals()[class_name.capitalize()]  # Get the class corresponding to the table name
            results = session.query(table_class).all()
            for result in results:
                record_tuple = tuple(getattr(result, column.name) for column in result.__table__.columns)
                records.append(record_tuple)
        return records
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def get_clubs():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            return session.query(Club).all()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def get_event_attendees(event_id=None):
    assert isinstance(int(event_id), (int, type(None))), "event_id must be an integer or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            if event_id == None:
                return []
            attendees = list(map(lambda attendee: attendee.user_id, session.query(EventAttendee).filter(EventAttendee.event_id == event_id).all()))
            return attendees
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def get_user_info(user_id):
    assert isinstance(user_id, (str, type(None))), "user_id must be an string or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                return user.name, user.pronouns, user.about_me
            else:
                return None
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex
        
def get_officer_club_info(user_id):
    assert isinstance(user_id, (str, type(None))), "user_id must be an string or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            club_id = session.query(Officer).filter(Officer.user_id == user_id).first()
            if club_id:
                club_id = club_id.club_id
            else:
                return None
            club_name = session.query(Club).filter(Club.club_id == club_id).first().name

            return club_id, club_name
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def get_officers():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            return session.query(Officer).all()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def get_users():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            return session.query(User).all() 
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex
    
def get_announcements_with_club_names():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # Querying all announcements along with the related club object
            announcements = get_records('announcement')
            results = []
            for announcement in announcements:
                club_id = announcement[4]
                club_name = session.query(Club).filter(Club.club_id == club_id).first().name
                results.append((announcement[0], announcement[1], announcement[2], announcement[4], club_name))
            return results
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def create_announcement(announcement_id=None, title=None, description=None, image=None, club_id=None):
    assert isinstance(announcement_id, (int , type(None))), "announcement_id must be a int or None"
    assert isinstance(title, (str, type(None))), "title must be a string or None"
    assert isinstance(description, (str, type(None))), " must be a string or None"
    assert isinstance(image, (str, type(None))), " must be a string or None"
    assert isinstance(club_id, (int, type(None))), " must be a int or None"
    
    if title is not None:
        assert len(title) <= 75, "title must be at most 75 characters"
    
    if description is not None:
        assert len(description) <= 3000, "description must be at most 3000 characters"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            new_announcement = Announcement(announcement_id=announcement_id, title=title, description=description, image=image, club_id=club_id)
            session.add(new_announcement)
            session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def create_club(club_id=None, name=None, description=None, image=None, coffee_chat_link=None):
    assert isinstance(club_id, (int, type(None))), "club_id must be a int or None"
    assert isinstance(name, (str, type(None))), "name must be a string or None"
    assert isinstance(description, (str, type(None))), "description must be a string or None"
    assert isinstance(image, (str, type(None))), "image must be a string or None"
    assert isinstance(coffee_chat_link, (str, type(None))), "coffee_chat_link must be a string or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            new_club = Club(club_id=club_id, name=name, description=description, image=image, coffee_chat_link=coffee_chat_link)
            session.add(new_club)
            session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def create_event_attendee(event_id=None, user_id=None):
    assert isinstance(int(event_id), (int, type(None))), "event_id must be a int or None"
    assert isinstance(user_id, (str, type(None))), "user_id must be a string or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            new_event_attendee = EventAttendee(event_id=event_id, user_id=user_id)
            session.add(new_event_attendee)
            session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def create_event(event_id=None, name=None, location=None, description=None, start_time=None, end_time=None):
    assert isinstance(event_id, (int, type(None))), "event_id must be a int or None"
    assert isinstance(name, (str, type(None))), "name must be a string or None"
    assert isinstance(location, (str, type(None))), "location must be a string or None"
    assert isinstance(description, (str, type(None))), "description must be a string or None"
    assert isinstance(start_time, (str, type(None))), "start_time must be a string or None"
    assert isinstance(end_time, (str, type(None))), "end_time must be a string or None"

    if name is not None:
        assert len(name) <= 75, "name must be at most 75 characters"
    
    if description is not None:
        assert len(description) <= 3000, "description must be at most 3000 characters"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            new_event = Event(event_id=event_id, name=name, location=location, description=description, start_time=start_time, end_time=end_time)
            session.add(new_event)
            session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def create_officer(user_id=None, club_id=None):
    assert isinstance(user_id, (str, type(None))), "user_id must be a string or None"
    assert isinstance(club_id, (int, type(None))), "club_id must be a int or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            new_officer = Officer(user_id=user_id, club_id=club_id)
            session.add(new_officer)
            session.commit()
            return None
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def create_user(user_id=None, name=None, netid=None, profile_pic=None, pronouns=None, about_me=None):
    assert isinstance(user_id, (str, type(None))), "user_id must be a string or None"
    assert isinstance(name, (str, type(None))), "name must be a string or None"
    assert isinstance(netid, (str, type(None))), "netid must be a string or None"
    assert isinstance(profile_pic, (str, type(None))), "profile_pic must be a string or None"
    assert isinstance(pronouns, (str, type(None))), "pronouns must be a string or None"
    assert isinstance(about_me, (str, type(None))), "about_me must be a string or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            new_user = User(user_id=user_id, name=name, netid=netid, profile_pic=profile_pic, pronouns=pronouns, about_me=about_me)
            session.add(new_user)
            session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def delete_event(event_id):
    assert isinstance(int(event_id), (int, type(None))), "event_id must be a int or None"

    try:
        with sqlalchemy.orm.Session(engine) as session:
            event = session.query(Event).filter_by(event_id=event_id).first()
            if event:
                session.query(EventAttendee).filter(EventAttendee.event_id == event_id).delete()
                session.query(Event).filter(Event.event_id == event_id).delete()
                session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def delete_announcement(announcement_id):
    assert isinstance(announcement_id, (int, type(None))), "announcement_id must be a int or None"
    try:
        with sqlalchemy.orm.Session(engine) as session:
            announcement = session.query(Announcement).filter_by(announcement_id=announcement_id).first()

            if announcement:
                session.query(Announcement).filter(Announcement.announcement_id == announcement_id).delete()
                session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def edit_user_field(user_id, field, value):
    assert isinstance(user_id, (str, type(None))), "user_id must be a string or None"
    
    try:
        with sqlalchemy.orm.Session(engine) as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user:
                setattr(user, field, value)
                session.commit()
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise ex

def main():
    if len(sys.argv) != 1:
        print('Usage: python ' + sys.argv[0], file=sys.stderr)
        sys.exit(1)

    try:
        Base.metadata.create_all(engine)
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
