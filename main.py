from fastapi import FastAPI
import pydantic
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

app = FastAPI(title="Events App")


fake_events = [
    {'title': 'Derchein', 'event_author': 'label1', 'place': 'Jasna 1', 'category': 'techno', 'id': '1', 'price': 500},
    {'title': 'Derchein2', 'event_author': 'label1', 'place': 'Smolna', 'category': 'techno', 'id': '2', 'price': 500},
    {'title': 'Derchein3', 'event_author': 'label2', 'place': 'Smolna', 'category': 'techno', 'id': '3', 'price': 500},
    {'title': 'Djset', 'event_author': 'label2', 'place': 'K-Bar', 'category': 'eurodance', 'id': '4', 'price': 500},
    {'title': 'Derchein4', 'event_author': 'label2', 'place': 'Jasna 1', 'category': 'trance', 'id': '5', 'price': 500}
]

fake_users = [
    {"id": 1, "role": "admin", "name": "Nikita"},
    {"id": 2, "role": "user", "name": "Bob", "degree":[
        {"id": 1, "created_at": "2024-01-01T00:00:00", "type_degree": "expert"}
    ]},
    {"id": 3, "role": "user", "name": "Jack"},
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: List[Optional[Degree]] = None

@app.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]

@app.get("/events/")
async def see_all_events(limit: int = 1, offset: int = 0):
    return fake_events[offset:][:limit]


@app.get("/events/{event_title}")
async def see_event(event_title: str):
    for event in fake_events:
        if event.get('title').casefold() == event_title.casefold():
            return event


@app.get("/events/{event_author}/")
async def read_author_category_by_query(event_author: str, category: str):
    events_to_return = []
    for event in fake_events:
        if event.get('event_author').casefold() == event_author.casefold() and \
                event.get ('category').casefold() == category.casefold():
            events_to_return.append(event)
    return events_to_return


class Event(BaseModel):
    title: str
    event_author: str
    category: str
    id: int
    price: int = Field(ge=0)



@app.post("/events/")
async def add_events(events: List[Event]):
    fake_events.extend(events)
    return {"status": 200, "data": fake_events}
