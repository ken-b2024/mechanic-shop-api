from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


service_ticket_mechanics = db.Table(
    'assigned_tickets',
    Base.metadata,
    db.Column('mechanic_id', db.ForeignKey('mechanics.id')),
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'))
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(12))
    make_model: Mapped[str] = mapped_column(db.String(200), nullable=False)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(12), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=service_ticket_mechanics)
    
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=datetime.now)
    service_desc: Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_ticket_mechanics,)