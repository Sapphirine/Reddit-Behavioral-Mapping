from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
import ast
import praw

"""
Consts
"""

Base = declarative_base()

"""
Thread Tables
"""

class Thread(Base):
    """
    Table for Thread items, includes all
    items available from the Reddit API.
    """

    __tablename__           = "Threads"

    approved_by             = Column(String)
    archived                = Column(Boolean)
    author                  = Column(String)
    author_flair_css_class  = Column(String)
    banned_by               = Column(String)
    clicked                 = Column(Boolean)
    created                 = Column(Integer)
    created_utc             = Column(Integer)
    distinguished           = Column(String)
    domain                  = Column(String)
    downs                   = Column(Integer)
    edited                  = Column(Integer)
    from_id                 = Column(String)
    from_kind               = Column(String)
    gilded                  = Column(Integer)
    hidden                  = Column(Boolean)
    hide_score              = Column(Boolean)
    id                      = Column(String, primary_key=True)
    is_self                 = Column(Boolean)
    likes                   = Column(String)
    link_flair_css_class    = Column(String)
    link_flair_text         = Column(String)
    locked                  = Column(Boolean)
    media                   = relationship("Media", back_populates="thread", uselist=False)
    media_embed             = relationship("Media_embed", back_populates="thread", uselist=False)
    mod_reports             = relationship("Thread_mod_report", back_populates="thread")
    name                    = Column(String)
    num_comments            = Column(Integer)
    num_reports             = Column(Integer)
    over_18                 = Column(Boolean)
    permalink               = Column(String)
    quarantine              = Column(Boolean)
    removal_reason          = Column(String)
    report_reasons          = Column(String)
    saved                   = Column(Boolean)
    score                   = Column(Integer)
    secure_media            = relationship("Secure_media", back_populates="thread", uselist=False)
    secure_media_embed      = relationship("Secure_media_embed", back_populates="thread", uselist=False)
    selftext                = Column(String)
    selftext_html           = Column(String)
    stickied                = Column(Boolean)
    subreddit               = Column(String)
    subreddit_id            = Column(String)
    suggested_sort          = Column(String)
    thumbnail               = Column(String)
    title                   = Column(String)
    ups                     = Column(Integer)
    url                     = Column(Integer)
    user_reports            = relationship("Thread_user_report", back_populates="thread") #<----
    visited                 = Column(Boolean)

    # Replies to thread
    children                = relationship("Comment", back_populates="thread")

class Media(Base):
    """
    Table to hold media objects from threads.
    """

    __tablename__           = "Medias"

    id                      = Column(String, primary_key=True)

    oembed                  = relationship("Oembed", back_populates="media", uselist=False)
    type                    = Column(String)

    # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="media")

class Oembed(Base):
    """
    Table to hold oembed objects from
    in Media table
    """

    __tablename__           = "Oembeds"

    id                      = Column(String, primary_key=True)
    author_name             = Column(String)
    author_url              = Column(String)
    description             = Column(String)
    height                  = Column(Integer)
    html                    = Column(String)
    provider_name           = Column(String)
    provider_url            = Column(String)
    thumbnail_height        = Column(Integer)
    thumbnail_url           = Column(String)
    thumbnail_width         = Column(Integer)
    title                   = Column(String)
    type                    = Column(String)
    url                     = Column(String)
    version                 = Column(String)
    width                   = Column(Integer)

    # Owning table
    media_id                = Column(String, ForeignKey("Medias.id"))
    media                   = relationship("Media", back_populates="oembed")
    secure_media_id         = Column(String, ForeignKey("Secure_medias.id"))
    secure_media            = relationship("Secure_media", back_populates="oembed")

class Media_embed(Base):
    """
    Table to hold embedded media objects from
    media_embed fields in Threads.
    """

    __tablename__           = "Media_embeds"

    id                      = Column(String, primary_key=True)
    content                 = Column(String)
    width                   = Column(Integer)
    height                  = Column(Integer)
    scrolling               = Column(Boolean)

    # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="media_embed")

class Thread_mod_report(Base):
    """
    Table to hold mod reports from
    mod_reports fields in Threads.
    """

    __tablename__           = "Thread_mod_reports"

    id                      = Column(String, primary_key=True)
    value                   = Column(String) # TODO: Temporary

    # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="mod_reports")

class Secure_media(Base):
    """
    Table to hold media objects from threads.
    """

    __tablename__           = "Secure_medias"

    id                      = Column(String, primary_key=True)

    oembed                  = relationship("Oembed", back_populates="secure_media", uselist=False)
    type                    = Column(String)

        # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="secure_media")

class Secure_media_embed(Base):
    """
    Table to hold embedded media objects from
    media_embed fields in Threads.
    """

    __tablename__           = "Secure_media_embeds"

    id                      = Column(String, primary_key=True)
    content                 = Column(String)
    width                   = Column(Integer)
    height                  = Column(Integer)
    scrolling               = Column(Boolean)

    # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="secure_media_embed")

class Thread_user_report(Base):
    """
    Table to hold user_reports objects from
    media_embed fields in Threads.
    """
    __tablename__           = "Thread_user_reports"

    id                      = Column(String, primary_key=True)
    value                   = Column(String) # TODO: Temporary

    # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="user_reports")

"""
Comment Tables
"""

class Comment(Base):
    """
    Table for Comment items, includes all
    items available from the Reddit API.
    """

    __tablename__           = "Comments"

    approved_by             = Column(String)
    #archived                = Column(Boolean)
    author                  = Column(String)
    author_flair_css_class  = Column(String)
    author_flair_text       = Column(String)
    banned_by               = Column(String)
    body                    = Column(String)
    body_html               = Column(String)
    controversiality        = Column(Integer)
    created                 = Column(Integer)
    created_utc             = Column(Integer)
    distinguished           = Column(String)
    downs                   = Column(Integer)
    #edited                  = Column(Boolean)
    #gilded                  = Column(Integer)
    id                      = Column(String, primary_key=True)
    likes                   = Column(String)
    link_id                 = Column(String)
    mod_reports             = relationship("Comment_mod_report", back_populates="comment")
    name                    = Column(String)
    num_reports             = Column(Integer)
    parent_id               = Column(String, ForeignKey("Comments.id"))
    removal_reason          = Column(String)
    ups                     = Column(Integer)
    user_reports            = relationship("Comment_user_report", back_populates="comment")

    # Replies
    children                = relationship("Comment",
                                        backref=backref("parent", remote_side=[id])
                                        )

    # Owning thread
    thread_id               = Column(String, ForeignKey("Threads.id"))
    thread                  = relationship("Thread", back_populates="children")

class Comment_mod_report(Base):
    """
    Table to hold mod reports from
    mod_reports fields in Comments.
    """

    __tablename__           = "Comment_mod_reports"

    id                      = Column(String, primary_key=True)
    value                   = Column(String) # TODO: Temporary

    # Owning comment
    comment_id              = Column(String, ForeignKey("Comments.id"))
    comment                 = relationship("Comment", back_populates="mod_reports")

class Comment_user_report(Base):
    """
    Table to hold user_reports objects from
    media_embed fields in Threads.
    """
    __tablename__           = "Comment_user_reports"

    id                      = Column(String, primary_key=True)
    value                   = Column(String) # TODO: Temporary

    # Owning comment
    comment_id              = Column(String, ForeignKey("Comments.id"))
    comment                 = relationship("Comment", back_populates="user_reports")

"""
Funcs
"""

# Define engine
engine = create_engine('sqlite:///test.db', echo=True) # 'sqlite:///:memory:' puts a database in RAM
Base.metadata.create_all(engine)

# Create a session to link to the db
Session = sessionmaker(bind=engine)
session = Session()

# Ensure keys are valid
def encode(utf8str):

    # Catch bad inputs
    if utf8str is None:
        return None

    # Catch boolean
    if isinstance(utf8str, bool):
        return utf8str

    # Catch all numericals
    if isinstance(utf8str, float) or isinstance(utf8str, long) or isinstance(utf8str, int):
        return int(utf8str)

    utf8str = utf8str.encode('ascii','ignore')
    if utf8str.isspace():
        return 'None'
    if utf8str == '':
        return 'None'
    return utf8str

def put_oembed(id, submission):

    # If empty
    if not submission:
        return None

    # Intitialize table
    oembed = Oembed(id=encode(id))

    # Define fields
    oembed.author_name             = encode(submission['author_name'])
    oembed.author_url              = encode(submission['author_url'])
    oembed.description             = encode(submission['description'])
    oembed.height                  = encode(submission['height'])
    oembed.html                    = encode(submission['html'])
    oembed.provider_name           = encode(submission['provider_name'])
    oembed.provider_url            = encode(submission['provider_url'])
    oembed.thumbnail_height        = encode(submission['thumbnail_height'])
    oembed.thumbnail_url           = encode(submission['thumbnail_url'])
    oembed.thumbnail_width         = encode(submission['thumbnail_width'])
    oembed.title                   = encode(submission['title'])
    oembed.type                    = encode(submission['type'])
    oembed.url                     = encode(submission['url'])
    oembed.version                 = encode(submission['version'])
    oembed.width                   = encode(submission['width'])

    # Add to DB queue
    session.add(oembed)

    return oembed

def put_media(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    media = Media(id=encode(id))

    # Define fields
    media.oembed                   = put_oembed(id, submission['oembed'])
    media.type                     = encode(submission['type'])

    # Add to DB queue
    session.add(media)

    return media

def put_media_embed(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    media_embed = Media_embed(id=encode(id))

    # Define fields
    media_embed.content            = encode(submission['content'])
    media_embed.width              = encode(submission['width'])
    media_embed.height             = encode(submission['height'])
    media_embed.scrolling          = encode(submission['scrolling'])

    # Add to DB queue
    session.add(media_embed)

    return media_embed

def put_thread_mod_report(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    mod_report = Thread_mod_report(id=encode(id))

    # Define fields
    mod_report.value               = encode(submission)

    # Add to DB queue
    session.add(mod_report)

    return mod_report

def put_secure_media(id, submission):

    # If empty
    if not submission:
        return None

    # Intitialize table
    secure_media = Secure_media(id=encode(id))

    # Define fields
    secure_media.oembed            = put_oembed(id, submission['oembed'])
    secure_media.type              = encode(submission['type'])

    # Add to DB queue
    session.add(secure_media)

    return secure_media

def put_secure_media_embed(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    secure_media_embed = Secure_media_embed(id=encode(id))

    # Define fields
    secure_media_embed.content            = encode(submission['content'])
    secure_media_embed.width              = encode(submission['width'])
    secure_media_embed.height             = encode(submission['height'])
    secure_media_embed.scrolling          = encode(submission['scrolling'])
    secure_media_embed.allowfullscreen    = encode(submission['allowfullscreen'])

    # Add to DB queue
    session.add(secure_media_embed)

    return secure_media_embed

def put_thread_user_report(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    user_report = Thread_user_report(id=encode(id))

    # Define fields
    user_report.value                = encode(submission)

    # Add to DB queue
    session.add(user_report)

    return user_report

def put_comment_mod_report(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    mod_report = Comment_mod_report(id=encode(id))

    # Define fields
    mod_report.value               = encode(submission)

    # Add to DB queue
    session.add(mod_report)

    return mod_report

def put_comment_user_report(id, submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    user_report = Comment_user_report(id=encode(id))

    # Define fields
    user_report.value               = encode(submission)

    # Add to DB queue
    session.add(user_report)

    return user_report

def put_comment(submission):

    # If empty
    if not submission:
        return None

    # Initialize table
    comment = Comment(id=encode(submission.id))

    # Take care of PRAW objects
    author = encode(submission.author.name) if isinstance(submission.author, praw.objects.Redditor) else encode(submission.author)

    # Define fields
    comment.approved_by             = encode(submission.approved_by)
    #comment.archived                = encode(submission.archived)
    comment.author                  = author
    comment.author_flair_css_class  = encode(submission.author_flair_css_class)
    comment.author_flair_text       = encode(submission.author_flair_text)
    comment.banned_by               = encode(submission.banned_by)
    comment.body                    = encode(submission.body)
    comment.body_html               = encode(submission.body_html)
    comment.controversiality        = encode(submission.controversiality)
    comment.created                 = encode(submission.created)
    comment.created_utc             = encode(submission.created_utc)
    comment.distinguished           = encode(submission.distinguished)
    comment.downs                   = encode(submission.downs)
    #comment.edited                  = encode(submission.edited)
    #comment.gilded                  = encode(submission.gilded)
    # id
    comment.likes                   = encode(submission.likes)
    comment.link_id                 = encode(submission.link_id)
    comment.mod_reports             = [put_comment_mod_report(submission.id, mod_report) for mod_report in submission.mod_reports]
    comment.name                    = encode(submission.name)
    comment.num_reports             = encode(submission.num_reports)
    #comment.parent_id               = encode(submission.parent_id)
    comment.removal_reason          = encode(submission.removal_reason)
    comment.ups                     = encode(submission.ups)
    comment.user_reports            = [put_comment_user_report(submission.id, user_report) for user_report in submission.user_reports]

    comment.children                = [put_comment(reply) for reply in submission.replies]

    # Add to DB queue
    session.add(comment)

    return comment

def put_thread(submission):

    # Inititialize thread
    thread = Thread(id=encode(submission.id))

    # Take care of PRAW classes
    author = encode(submission.author.name) if isinstance(submission.author, praw.objects.Redditor) else encode(submission.author)
    subreddit = encode(submission.subreddit.display_name) if isinstance(submission.subreddit, praw.objects.Subreddit) else encode(submission.subreddit)

    # Define fields
    thread.approved_by             = encode(submission.approved_by)
    thread.archived                = encode(submission.archived)
    thread.author                  = author
    thread.author_flair_css_class  = encode(submission.author_flair_css_class)
    thread.banned_by               = encode(submission.banned_by)
    thread.clicked                 = encode(submission.clicked)
    thread.created                 = encode(submission.created)
    thread.created_utc             = encode(submission.created_utc)
    thread.distinguished           = encode(submission.distinguished)
    thread.domain                  = encode(submission.domain)
    thread.downs                   = encode(submission.downs)
    thread.edited                  = encode(submission.edited)
    thread.from_id                 = encode(submission.from_id)
    thread.from_kind               = encode(submission.from_kind)
    thread.gilded                  = encode(submission.gilded)
    thread.hidden                  = encode(submission.hidden)
    thread.hide_score              = encode(submission.hide_score)
    # id
    thread.is_self                 = encode(submission.is_self)
    thread.likes                   = encode(submission.likes)
    thread.link_flair_css_class    = encode(submission.link_flair_css_class)
    thread.link_flair_text         = encode(submission.link_flair_text)
    thread.locked                  = encode(submission.locked)
    thread.media                   = put_media(submission.id, submission.media)
    thread.media_embed             = put_media_embed(submission.id, submission.media_embed)
    thread.mod_reports             = [put_thread_mod_report(submission.id, mod_report) for mod_report in submission.mod_reports]
    thread.name                    = encode(submission.name)
    thread.num_comments            = encode(submission.num_comments)
    thread.num_reports             = encode(submission.num_reports)
    thread.over_18                 = encode(submission.over_18)
    thread.permalink               = encode(submission.permalink)
    thread.quarantine              = encode(submission.quarantine)
    thread.removal_reason          = encode(submission.removal_reason)
    thread.report_reasons          = encode(submission.report_reasons)
    thread.saved                   = encode(submission.saved)
    thread.score                   = encode(submission.score)
    thread.secure_media            = put_secure_media(submission.id, submission.secure_media)
    thread.secure_media_embed      = put_secure_media_embed(submission.id, submission.secure_media)
    thread.selftext                = encode(submission.selftext)
    thread.selftext_html           = encode(submission.selftext_html)
    thread.stickied                = encode(submission.stickied)
    thread.subreddit               = subreddit
    thread.subreddit_id            = encode(submission.subreddit_id)
    thread.suggested_sort          = encode(submission.suggested_sort)
    thread.thumbnail               = encode(submission.thumbnail)
    thread.title                   = encode(submission.title)
    thread.ups                     = encode(submission.ups)
    thread.url                     = encode(submission.url)
    thread.user_reports            = [put_thread_user_report(submission.id, user_report) for user_report in submission.user_reports]
    thread.visited                 = encode(submission.visited)

    thread.children                = [put_comment(comment) for comment in submission.comments]

    # Add to DB queue
    session.add(thread)

    # Commit
    session.commit()
