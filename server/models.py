from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError("Name is required")
        if Author.query.filter_by(name=name).first():
            raise ValueError(f"Author {name} already exists")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
      if len(phone_number) != 10 or not phone_number.isdigit():
          raise ValueError("Phone number should contain exactly 10 digits.")
      return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    
    @validates('content')
    def validate_content(self,key,content):
        if len(content) < 250:
            raise ValueError("Content should have more than 250 characters")
        return content
    
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary) > 250 :
            raise ValueError("Summary should be a maximum of 250 characters")
        return summary
    
    @validates('category')
    def validate_phone_category(self,key,category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category can either 'Fiction' or 'Non-Fiction'")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Title must contain one of the following keywords: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return title





    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
