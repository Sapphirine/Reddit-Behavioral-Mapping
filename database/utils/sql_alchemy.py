from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Thread(Base):

    __tablename__ = "Threads"

    id = Column(String, primary_key=True)
    author = Column(String)
    body = Column(String) # TODO: change this for threads
    ups = Column(Integer)
    downs = Column(Integer)
    children = relationship("Comments")
    
    def __repr__(self):
        return "<Thread(id='%s', author='%s', body='%s', ups='%d', downs='%d', children='%s')>" % \
                (self.id, self.author, self.body, self.ups, \
                 self.downs, self.children)

class Comment(Base):

    __tablename__ = "Comments"

    id = Column(String, primary_key=True)
    parent_id = Column(String, ForeignKey("Comments.id"))
    author = Column(String)
    body = Column(String)
    ups = Column(Integer)
    downs = Column(Integer)
    children = relationship("Comment",
                            backref=backref('parent', remote_side=[id])
                            )
    
    def __repr__(self):
        return "<Thread(id='%s', author='%s', body='%s', ups='%d', downs='%d', parent='%s', children='%s')>" % \
                (self.id, self.author, self.body, self.ups, \
                self.downs, self.parent, self.children)