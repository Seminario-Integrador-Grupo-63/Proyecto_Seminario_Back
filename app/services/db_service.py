#create db and engine
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine, select, delete

from models import Category

class DB_Service:
    db_url = "postgresql://admin:admin@QResto_db:5432/root"

    engine = create_engine(db_url, echo=True)

    @classmethod
    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)
    
    @classmethod
    def get_list_from_db(self, model:SQLModel):
        with Session(self.engine) as session:
            statement = select(model)
            result = session.exec(statement).all() 
            return result
    
    @classmethod
    def get_object_by_id(self, model: SQLModel, id:int):
        with Session(self.engine) as session:
            statement = select(model).where(model.id == id)
            result = session.exec(statement).one()
            return result
    
    @classmethod
    def create_object(self, model: SQLModel):
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model
    
    @classmethod
    def update_object(self, model: SQLModel, body: SQLModel):
        with Session(self.engine) as session:
            result = session.get(model, body.id)
            if not result:
                raise HTTPException(status_code=404, detail="Hero not found")
            data = body.dict()
            for key, value in data.items():
                setattr(result, key, value)
            session.add(result)
            session.commit()
            session.refresh(result)
            return result

    @classmethod
    def get_with_filters(self, statement):
        with Session(self.engine) as session:
            result = session.exec(statement).all()
            if len(result) == 1 and isinstance(result[0], tuple):
                result = [result[0][0]]
            return result if result else []
    
    @classmethod
    def delete_dable(self, model:SQLModel):
        with Session(self.engine) as session:
            statement = delete(model)
            result = session.exec(statement)
            session.commit()
    
    @classmethod
    def delete_row(self, model:SQLModel, where_statement: list):
        with Session(self.engine) as session:
            statement = delete(model).where(*where_statement)
            result = session.exec(statement)
            session.commit()
        
db_service = DB_Service()