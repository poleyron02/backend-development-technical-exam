import sys
sys.path.append('../')
import os
import shutil
from fastapi import FastAPI, UploadFile, HTTPException, Query
import csv
from globals import collection, UPLOAD_DIR
import math
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Medalist(BaseModel):
    """
    Medalist represents an individual who has won a medal.
    
    Attributes:
        `name (str | None)`: The name of the medalist.
        `medal_type (str | None)`: The type of medal won (e.g., gold, silver, bronze).
        `gender (str | None)`: The gender of the medalist.
        `country (str | None)`: The country the medalist represents.
        `country_code (str | None)`: The country code of the medalist's country.
        `nationality (str | None)`: The nationality of the medalist.
        `medal_code (int | None)`: A code representing the medal.
        `medal_date (str | None)`: The date the medal was awarded.
    """
    
    name: str | None
    medal_type: str | None
    gender: str | None
    country: str | None
    country_code: str | None
    nationality: str | None
    medal_code: int | None
    medal_date: str | None

class EventStats(BaseModel):
    """
    EventStats represents the statistics of an event in a sports competition.
    
    Attributes:
        `discipline (str)`: The discipline or category of the event.
        `event (str)`: The name of the event.
        `event_date (str)`: The date when the event took place.
        `medalists (List[Medalist])`: A list of Medalist objects representing the winners of the event.
    """

    discipline: str
    event: str
    event_date: str
    medalists: List[Medalist]

@app.post('/upload')
async def upload_file(file: UploadFile):
    """
    Uploads a CSV file to the server.
    
    Args:
        `file (UploadFile)`: The file to be uploaded. Must be a CSV file.
    Raises:
        `HTTPException`: If the file is not a CSV file or if there is an error reading the CSV file.
        `HTTPException`: If there is an error saving the file to the server.
    Returns:
        `dict`: A dictionary containing a success message and the filename of the uploaded file.
    """

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail='Only CSV files are allowed.')
    
    try:
        csv.reader(file.file)
        file.file.seek(0)
    except csv.Error:
        raise HTTPException(status_code=400, detail='Invalid CSV file.')

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {'message' : 'File uploaded successfully', 'filename' : file.filename}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args)

@app.get('/aggregated_stats/event')
def get_aggregated_stats(page: int = Query(1, alias='page', ge=1), page_size: int = 10):
    """
    Retrieve aggregated statistics of medalists grouped by discipline, event, and event date.
    
    Args:
        `page (int)`: The page number for pagination. Defaults to 1. Must be greater than or equal to 1.
        `page_size (int)`: The number of records per page. Defaults to 10.
    Returns:
        `dict`: A dictionary containing the following keys:

                    - `data (list)`: A list of EventStats objects containing the aggregated statistics.
                    - `paginate (dict)`: A dictionary containing pagination information:
                
                        - `current_page (int)`: The current page number.
                        - `total_pages (int)`: The total number of pages.
                        - `next_page (str or None)`: The URL for the next page, if it exists.
                        - `previous_page (str or None)`: The URL for the previous page, if it exists.
    Raises:
        `HTTPException`: If an error occurs during the aggregation process, an HTTP 500 error is raised with the error details.
    """
    
    try:
        skip_count = (page - 1) * page_size

        pipeline = [
            {
                '$group': {
                    '_id': {'discipline': '$discipline', 'event': '$event', 'event_date': '$medal_date'},
                    'medalists': {
                        '$push': {
                            'name': '$name',
                            'medal_type': '$medal_type',
                            'gender': '$gender',
                            'country': '$country',
                            'country_code': '$country_code',
                            'nationality': '$nationality',
                            'medal_code': '$medal_code',
                            'medal_date': '$medal_date'
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'discipline': '$_id.discipline',
                    'event': '$_id.event',
                    'event_date': '$_id.event_date',
                    'medalists': {
                        '$map': {
                            'input': '$medalists',
                            'as': 'medalist',
                            'in': {
                                'name': '$$medalist.name',
                                'medal_type': '$$medalist.medal_type',
                                'gender': '$$medalist.gender',
                                'country': '$$medalist.country',
                                'country_code': '$$medalist.country_code',
                                'nationality': '$$medalist.nationality',
                                'medal_code': '$$medalist.medal_code',
                                'medal_date': '$$medalist.medal_date'
                            }
                        }
                    }
                }
            },
            {'$sort': {'event_date': -1}},
            {'$skip': skip_count}, 
            {'$limit': page_size} 
        ]

        data = list(collection.aggregate(pipeline))
        total_documents = collection.aggregate([{'$group': {'_id': '$event'}}])
        total_events = len(list(total_documents))  
        total_pages = math.ceil(total_events / page_size)

        validated_data = [EventStats(**event) for event in data]

        return {
            'data': validated_data,
            'paginate': {
                'current_page': page,
                'total_pages': total_pages,
                'next_page': f'/aggregated_stats/event?page={page + 1}' if page < total_pages else None,
                'previous_page': f'/aggregated_stats/event?page={page - 1}' if page > 1 else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))