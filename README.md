# 🚛 Waste Collection Route Optimization

An intelligent system to optimize waste collection routes based on real-time requests and vehicle capacities.  

## 🛠️ **Project Overview**

This application simulates waste collection requests, optimizes routes for available vehicles, and visualizes the routes on an interactive map.

### 🧩 **Tech Stack**
- 🌐 **Backend:** FastAPI  
- 🔢 **Optimization:** Google OR-Tools  
- 📊 **Visualization:** Folium  
- 🖥️ **CLI Interface:** Click  
- 🛠️ **Database (In-Memory):** Python Objects  

---

## 🚀 **1️⃣ Setup Instructions**

### 🛠️ **Step 1: Clone the Repository**

```bash
git clone git@github.com:Rugved-142/Innovate---Team4.git
cd waste-route-optimizer
```
### 🖥️ **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate   # For Mac/Linux
# On Windows: venv\Scripts\activate
```
### 📦 Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
#  Running the Application
### 🚀 Start the Backend Server
```Bash
cd server
uvicorn app:app --reload
```
