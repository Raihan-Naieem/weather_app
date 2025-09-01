from functools import wraps

from typing import  Any
import sqlite3

from flask import redirect, url_for, session

import json

# by doing this outside server will read the json only one...
# else it had to read everytime get_cities() is called
with open('static/city.list.json', 'r', encoding='utf-8') as file:
    cities = json.load(file)
def get_cities(country_code: str) -> list[str]:
    '''
        filters cities according to country code from a static json file
    '''
    filtered_cities: list[str] = [city['name'] for city in cities if city['country'] == country_code]

    return filtered_cities


def get_country_codes() -> list[str]:
    with open('static/country.txt', 'r') as file:
        country_codes: list[str] = file.read().strip().split(', ')
        return country_codes



def login_required(function):
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        
        if 'user_id' in session:
            return function(*args, **kwargs)
        
        return redirect(url_for("login"))
    
    return wrapper



def SQL(command: str, *placeholder: Any) -> list[dict[Any,Any]] | None:
    
    # Connect to the database (creates the database if it doesn't exist) and return rows as dictionaries
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    try:
        # Execute the command
        cursor.execute(command, placeholder)
        
        if command.strip().upper().startswith('SELECT'):
            # Fetch all rows for SELECT command and converts rows to a list of dictionaries
            rows = cursor.fetchall()
            result = [dict(row) for row in rows ]
            return result
        else:
            # Commit for non-SELECT commands (INSERT, UPDATE, DELETE)
            connection.commit()

    except sqlite3.IntegrityError as e: # Unique error
        raise ValueError(e)
    except sqlite3.Error as e:
        raise ValueError(e)
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
