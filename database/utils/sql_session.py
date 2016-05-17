from sql_alchemy import Thread, Comment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: Define engine.
engine = create_engine('sqlite:///:memory:', echo=True) # 'sqlite:///:memory:' puts a database in RAM
Session = sessionmaker(bind=engine)
session = Session()

# Ensure inputs are valid
def encode(utf8str):

    # Catch bad inputs
    if utf8str is None:
        return 'None'

    # Catch boolean
    if isinstance(utf8str, bool):
        return utf8str

    # Catch all numericals
    if isinstance(utf8str, float) or isinstance(utf8str, long) or isinstance(utf8str, int):
        return int(utf8str)

    if isinstance(utf8str, list) or isinstance(utf8str, dict):
        utf8str = str(utf8str)

    utf8str = utf8str.encode('ascii','ignore')
    if utf8str.isspace():
        return 'None'
    if utf8str == '':
        return 'None'
    return utf8str

# Define put comments and threads
def put_thread(id, author, body, ups, downs, children):
    
    # For batch writing
    if hasattr(id, '__iter__'):
        # Make sure lens line up
        assert len(id) == len(author) == len(body) == len(ups) == len(downs)
        
        # Batch write
        session.add_all(
            [Thread(id=encode(i), author=encode(a), body=encode(b), \
                ups=encode(u), downs=encode(d), children=c) for \
                    i, a, b, u, d, c in zip(id, author, body, ups, downs, children)])
        
        # If entry is modified
        if session.dirty:
            print("WARNING: Overwriting Thread(s)")
            print session.dirty
            
        # Commit entries
        session.commit()
    
    # Single insertion
    else:
        session.add(Thread(id=encode(id), author=encode(author), body=encode(body), \
                        ups=encode(ups), downs=encode(downs), children=children))
        
