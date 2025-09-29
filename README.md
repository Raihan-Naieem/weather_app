
# Weather App (work in progress)

A simple weather dashboard built with **Flask** and the **OpenWeather API**.  

---

##  ***Getting Started***

### 1. Clone the Repository
```bash
git clone https://github.com/Raihan-Naieem/weather_app.git
cd weather_app
```
##### 2. Create a ***.env*** file in the project root:

```bash
touch .env
```

##### Add your keys inside .env:

```bash
SECRET_KEY = 'your secret key'
OpenWeather_API_KEY = 'your open weather api key'
```



### 3. Build and Start with Docker Compose (you must have docker and docker-compose installed first)
``` bash
docker compose up --build
```
### OR run in background
```bash
docker compose up -d
```

### 4. Access the App

Open your browser and go to:  
[http://localhost](http://localhost)

### 5. To fully close docker container
``` bash
docker compose down -v
```



