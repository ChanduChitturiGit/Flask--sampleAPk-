from db import db 

class ItemsModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"),nullable=False,unique=False)
    
    stores = db.relationship("StoreModel",back_populates="items")