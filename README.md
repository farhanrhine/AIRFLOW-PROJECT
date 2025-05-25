
![alt text](<Screenshot 2025-05-25 184809.png>)
![alt text](<Screenshot 2025-05-25 190048.png>) 
![alt text](<Screenshot 2025-05-25 190027.png>) 



## **How to Set Up the Airflow Project (Using Astronomer and Docker)**

### **1. Install Prerequisites**

* **Docker Desktop** (for containerization)
* **Astronomer CLI**
  Install with:

  ```
  winget install -e --id Astronomer.Astro
  ```

---

### **2. Set Up Project Directory**

* Navigate to your workspace in terminal
* Initialize the Astronomer project with:

  ```
  astro dev init
  ```

  This sets up the whole project structure automatically (DAGs, plugins, etc.)

---

### **3. Create New DAG File**

* In the `dags/` folder, create your DAG Python file (e.g., `etl_weather.py`)
* Make sure to **always place your ETL/logic scripts in the `dags/` folder**

---

### **4. Define API**

* You're using:

  ```
  https://api.open-meteo.com/v1/forecast?latitude=30.748882&longitude=76.641357&current_weather=true
  ```

---

### **5. Key Files**

* `docker-compose.yml` — for defining services (like Airflow scheduler, webserver, etc.)
* `[Dockerfile]` — for custom images if needed

---

### **6. Run the Project**

Start the local dev environment with:

```
astro dev start
```

* This will launch the Airflow UI — accessible via your browser (typically at `localhost:8080`)

---

### **7. Tools Used**

* **VS Code** — for writing and editing DAGs
* **DBeaver** — for working with PostgreSQL (or any other database integration in your pipeline)












