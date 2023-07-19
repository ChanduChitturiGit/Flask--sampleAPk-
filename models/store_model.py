from db import db 

class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    
    items = db.relationship("ItemsModel",back_populates="stores",lazy="dynamic")