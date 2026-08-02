# Weather Dashboard Web Application
## A modular Flask-based Weather Dashboard app containerized with Docker, served via Nginx, and powered by the OpenWeatherMap API for real-time global weather data.

[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/) [![Flask](https://img.shields.io/badge/flask-2.x-lightgrey?logo=flask&logoColor=black)](https://flask.palletsprojects.com/) [![Docker](https://img.shields.io/badge/docker-latest-blue?logo=docker&logoColor=white)](https://www.docker.com/) [![OpenWeather API](https://img.shields.io/badge/OpenWeather-API-1abc9c?logo=openweathermap&logoColor=white)](https://openweathermap.org/api)



#### Live URL: https://weather-app-pq79.onrender.com/

#### Video Demo (YouTube): https://youtu.be/oS4Rd4KVmFM

#### Video Demo (Local): [video/demo.mp4](video/demo.mp4)

---

## 📌 Table of Contents

1. [Project Overview](#project-overview)  
2. [Project Structure](#project-structure)  
3. [File and Module Explanations](#file-and-module-explanations)  
4. [Design Choices and Trade-offs](#design-choices-and-trade-offs)  
5. [Future Considerations](#future-considerations)  
6. [Conclusion](#conclusion)  
7. [Running it on Local Device](#to-run-it-on-local-device)

---
#### Description:

This project is a **Weather Dashboard Web Application** built with **Flask**, using a modular blueprint structure, containerized with **Docker**, and served behind **Nginx** with **docker-compose** orchestration. The app connects to the **OpenWeatherMap API** to retrieve and display real-time weather data for cities worldwide. It also includes features for user authentication, city management, and error handling, while keeping future scalability in mind.

The goal of this project was not only to build a working weather application but also to practice proper project structuring, containerization, and deployment workflows. It is designed as a stepping stone for more complex applications, incorporating both backend fundamentals and initial exposure to frontend elements.

---

## Project Overview

At its core, the application allows a registered user to:

- **Register and log in** to their own account.
- **Search for city weather information** using OpenWeatherMap’s data.
- **Add cities** of interest to their personal dashboard.
- **View stored cities** along with details like temperature, weather condition, and country code.
- **Delete cities** from their dashboard.
- **Experience flash messages** (success, error, etc.), which automatically disappear after a short delay.

The project also demonstrates the integration of multiple technologies:
- **Flask Blueprints** for modular routing and maintainable code.
- **Docker + docker-compose** for containerization and service orchestration.
- **Nginx** as a reverse proxy to serve the Flask application.
- **SQLite**  as the lightweight database engine.

---

## Project Structure

The repository has the following structure:

```bash
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── dashboard
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── weather
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── errors
│   │   └── __init__.py
│   ├── util.py
│   ├── templates
│   │   ├── base.html
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard
│   │   │   └── index.html
│   │   ├── errors
│   │   │   └── error.html
│   │   └── weather
│   │       ├── search_city_info.html
│   │       └── show_city_info.html
│   └── static
│       ├── city.list.json
│       ├── country.txt
│       ├── style.css
│       └── script.js
├── config.py
├── requirements.txt
├── README.md
├── Dockerfile
├── nginx.conf
└── docker-compose.yml
```


---

## File and Module Explanations

### 1. **Core Application**
`app/__init__.py`  
 - Initializes the Flask app, registers blueprints (`auth`, `dashboard`, `weather`, `errors`).
 - Connects configuration.

`config.py`
 - Loads environment variables such as `SECRET_KEY` and `OPENWEATHER_API_KEY`.
 - Configures session handling.

### 2. **Authentication**
`app/auth/routes.py`  
- Handles **register, login, and logout** functionality.
- Sessions are managed via Flask’s session system, with password hashing applied for user security.  
- The authentication system was **coded manually (without Flask-Login or external libraries)** to better understand the underlying concepts of
	- session handling
	- password hashing
	- user verification.

- Templates: `templates/auth/login.html,register.html`  
  Provide simple forms for authentication.

### 3. **Dashboard**
`app/dashboard/routes.py`  
- Displays the **list of cities** saved by the user.
- For each city, it shows weather details and the associated country code.
- Includes **Delete** so that users can manage their city list.

- Template: `templates/dashboard/index.html`  
  Shows the dashboard page where cities are listed.

### 4. **Weather**
`app/weather/routes.py`  
- Provides routes to **search for a city**, retrieve its weather information
- User can add this information it to the dashboard. 
- This project uses the following **OpenWeather API request structure** to fetch weather data:
   
  `https://api.openweathermap.org/data/2.5/weather?q=CityName,CountryCode&appid=API_KEY&units=Units`
  
  where:
	- **CityName** → the name of the city you want weather data for (e.g., `Dhaka`).  
	- **CountryCode** → the 2-letter ISO country code (e.g., `BD` for Bangladesh).  
	- **API_KEY** → your personal API key obtained from [OpenWeather](https://openweathermap.org/api).  
	- **Units** → determines the measurement system (e.g., `metric` for Celsius & m/s, `imperial` for Fahrenheit & mph).

  **Example:** 
	`https://api.openweathermap.org/data/2.5/weather?q=Dhaka,BD&appid=YOUR_API_KEY&units=metric`

- Templates:  
  - `templates/weather/search_city_info.html` (search form and result preview).  
  - `templates/weather/show_city_info.html` (detailed city weather data).

### 5. **Errors**
`app/errors/__init__.py` and `templates/errors/error.html`  
- Provide centralized error handling for cases such as 404 (page not found) or invalid API responses.

### 6. **Utilities**
`app/util.py`  

##### Contains helper functions:
1. **`get_cities` and `get_country_codes`** → parse data from `static/city_list.json` and `country_list.json`.  
   These functions ensure that city names and country codes are formatted correctly for the OpenWeather API requests.  
2. **`login_required` decorator** → enforces authentication by restricting access to routes only for logged-in users.  
3. **Custom SQL utility function** → a helper I built to interact with the SQLite database more flexibly than standard ORM patterns.

 

### 8. **Deployment**
- `Dockerfile`  
  Builds a lightweight containerized Python environment with dependencies from `requirements.txt`.  
- `docker-compose.yml`  
  Manages multiple services: Flask app container + Nginx reverse proxy.  
- `nginx.conf`  
  Configures **reverse proxy** to pass requests from Nginx to Flask (via Gunicorn/WSGI).  

---

## Design Choices and Trade-offs

- **Blueprints**: Chosen for modularity, making it easier to scale features (e.g., adding new modules like notifications).  
- **SQLite**: Used for simplicity, though in production a more robust DB (PostgreSQL/MySQL) would be preferable.  
- **Nginx reverse proxy**: Selected to simulate production-grade deployment, even though this project is primarily for learning.  
- **Frontend**: Intentionally minimal. My focus was backend and deployment; frontend remains an area to improve.  

---

## Future Considerations

1. **Hosting on my own PC** with port forwarding to learn networking concepts.  
2. Experimenting with **free hosting services** (e.g., Render, Railway, or Fly.io).  
3. Extending the modular structure for a larger, more complex project.  
4. Learning **JavaScript and frontend frameworks** properly, as my current frontend is functional but rough.  
5. Applying **clean code principles** for scalability, readability, and maintainability.  

---

## Conclusion

This project represents a practical exercise in combining **Flask, Docker, and Nginx** into a deployable web app. While its core purpose is a weather dashboard, the real value lies in the skills developed: 
	- authentication logic
	- modular blueprints
	- containerized environments
	- reverse proxy setup
	- future-oriented thinking about **deployment** and **scalability**.  

I view this as both a learning milestone and a strong foundation for more advanced projects.

---

## ***To run it on local device***

### 1. Clone the Repository
```bash
git clone https://github.com/Raihan-Naieem/weather_app.git
cd weather_app
```


### 2. Create ***.env*** File

##### Copy the ***.env.example*** file and rename it to ***.env***:

```bash
cp .env.example .env
```

##### Add your keys inside .env:

```bash
SECRET_KEY = 'your secret key'
OPENWEATHER_API_KEY = 'your open weather api key'
```
[👉 Get your API key here](https://openweathermap.org/api)

### 3. Build with Docker (you have to have docker and docker-compose first)
``` bash
docker compose build
```
### 4. Start with Docker Compose
``` bash
docker compose up
```
### OR run in background
```bash

docker compose up -d
```

### 5. Access the App

Open your browser and go to:  
[http://localhost](http://localhost)

### 6. To close docker container
``` bash
docker compose down
```

### To fully close and reset (delete session and database) docker container
```bash
docker compose down -v
```

