Here’s a **README.md** file with clear instructions on how to set up and run your **Docker Compose** environment. 🚀  

---

### **📘 README.md**

```md
# 🛠️ RAG-Based Chatbot with Streamlit Frontend & FastAPI Backend

This project consists of a **Retrieval-Augmented Generation (RAG) API** powered by **FastAPI** and a **Streamlit-based frontend** for user interaction. The system enables PDF uploads, document processing, and conversational AI responses.

---

## 🚀 **Getting Started**

### **1️⃣ Prerequisites**
Ensure you have the following installed on your machine:
- **Docker**: [Download & Install](https://www.docker.com/get-started)
- **Docker Compose**: (Comes with Docker Desktop)
  
---

## 🔧 **Installation & Setup**

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/alich03/AI-Conversation-Chatbot--Docker.git
cd rag-chatbot
```

---

### **3️⃣ Create a `.env` File**
Before running the application, create a `.env` file in the **RAG_API** directory and add your OpenAI API key:

```bash
cd RAG_API
touch .env
```

Inside the `.env` file, add:
```
OPENAI_API_KEY=your_openai_api_key_here
```
> Replace `your_openai_api_key_here` with your actual OpenAI API key.

---


### **3️⃣ Build & Run Containers**
Use Docker Compose to build and start both services (**FastAPI Backend** & **Streamlit Frontend**).
```bash
docker-compose up --build
```
> This will:
> - Build & start the **RAG API** (`rag-api`)
> - Build & start the **Streamlit Frontend** (`rag-frontend`)

---

## 🎯 **Accessing the Application**
Once the services are up, you can access them at:
- **Frontend (Chat Interface)**: [http://localhost:8501](http://localhost:8501)
- **Backend (FastAPI Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ **Project Structure**
```
/rag-chatbot
│── RAG_API/           # FastAPI Backend
│   ├── main.py        # Main API logic
│   ├── requirements.txt  # Dependencies
│   ├── Dockerfile     # Docker setup for API
│── RAG_Frontend/      # Streamlit Frontend
│   ├── app.py         # Main frontend logic
│   ├── Dockerfile     # Docker setup for frontend
│── docker-compose.yml # Docker Compose configuration
│── README.md          # Documentation
```

---

## 🐳 **Stopping the Containers**
To stop the running containers, use:
```bash
docker-compose down
```
> This will shut down all running services.

---

## ⚙️ **Common Issues & Fixes**
### **1. API Not Accessible?**
- Ensure the backend runs on port `8000`. If the issue persists, modify the `uvicorn` command in the **FastAPI Dockerfile**:
    ```dockerfile
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```
- Rebuild the container:
    ```bash
    docker-compose up --build
    ```

### **2. Docker Compose Fails to Start?**
Try:
```bash
docker-compose down --remove-orphans
docker-compose up --build
```

---

## 📜 **License**
This project is open-source and available under the [MIT License](LICENSE).

---

## 👨‍💻 **Author**
Developed by **Ali Hasnain** 🚀  
For any issues or feature requests, please [open an issue](https://github.com/alich03/AI-Conversation-Chatbot--Docker.git/issues).

---

Happy Coding! 🎉
```

---

### **📌 Key Highlights of the README**
✅ **Clear setup instructions** for cloning, building, and running  
✅ **Access URLs** for frontend and backend  
✅ **Troubleshooting section** for common Docker issues  
✅ **Proper project structure breakdown**  

This README ensures **anyone** can set up and run your project **easily!** 🚀