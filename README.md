
# Weather App

A simple weather dashboard built with **Flask** and the **OpenWeather API**.  
It displays real-time weather information based on city input.

---

##  ***Getting Started***

### 1. Clone the Repository
```bash
git clone https://github.com/Raihan-Naieem/weather_app.git
cd weather_app
```


### 2. Create and Activate a Virtual Environment

##### On **Linux/macOS**:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

##### On **Windows (PowerShell)**:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Create ***.env*** File

##### Create a ***.env*** file in the project root:

```bash
touch .env
```

##### Add your keys inside:

```python
SECRET_KEY = 'your secret key'
OpenWeather_API_KEY = 'your open weather api key'
```



### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```


