from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
 
Base = declarative_base()

class User(Base):
    
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'email'        : self.email,
           'picture'      : self.picture,
       }
    
class Category(Base):
    
    __tablename__ ='category'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    items_val = Column(Integer)
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'items_val'    : self.items_val,
       }
    
    
    
class Item(Base): 

    __tablename__ = 'item'  
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    price = Column(String(20), nullable=False)
    description = Column(String(500), nullable=False)
    when_added = Column(DateTime, default=datetime.datetime.utcnow)
    picture = Column(String(250))
    kind = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'price'        : self.price,
           'kind'         : self.kind,
           'description'  : self.description,
           'picture'      : self.picture,
           'when_added'   : self.when_added,  
           
       }
       
engine = create_engine('sqlite:///musicstore.db')
 

Base.metadata.create_all(engine)
