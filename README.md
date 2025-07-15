<div align="center">
  <img src="https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white" alt="Svelte" />
  <img src="https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
</div>

<h1 align="center">
  Broke n' Hungry
</h1>
<h2 align="center">
  🍽️ Your Personalized Meal Planner & Grocery Assistant 🥗
</h2>

<p align="center">
  <strong>Built for students on a budget.</strong> This app helps you eat well without a lot of time or money. Get custom meal plans and grocery lists that fit your student lifestyle.
</p>

---

## 🎯 Our Mission

This project is for students who want to eat well but are constrained by time and a tight budget. We aim to solve the "what to cook?" problem by providing personalized, affordable, and quick-to-prepare meal plans. Our goal is to make healthy eating accessible, reduce food waste, and eliminate the stress of daily meal planning.

## 🎥 Video Demo

Check out the video demo of our project MVP:

[![Broke n' Hungry Demo](https://img.youtube.com/vi/aVz0dD2MiGk/0.jpg)](https://youtu.be/aVz0dD2MiGk?si=fquaQXW63RXmFEl9)

## ✨ How It Works

The process is simple. You provide the application with some key information, and our AI-powered backend does the rest.

### Step 1: Tell Us About Yourself (The Inputs)

We build your profile based on a few simple questions:

-   **Food Preferences:** What cuisines do you love? (e.g., Indian, Mexican, Italian, Chinese, etc.)
-   **Weekly Budget:** How much do you want to spend on groceries?
-   **Cooking Time:** How much time can you dedicate to cooking each day?
-   **Allergies:** We take your health seriously. Let us know about any allergies.
-   **Nutrition Goals:** Are you looking to lose weight, gain muscle, or maintain your current physique?
-   **Dietary Restrictions:** We cater to all kinds of dietary needs, including:
    -   **Dietary:** Vegetarian, Vegan, Pescatarian, Paleo, Keto, etc.
    -   **Religious:** Halal, Kosher, Jain, etc.
    -   **Health-Related:** Gluten-free, Low-sodium, Diabetic-friendly, etc.
    -   And many more personal preferences and intolerances.

### Step 2: Get Your Personalized Plan (The Outputs)

Based on your inputs, our application generates:

1.  **🛒 A Smart Grocery List:** An itemized list of all the ingredients you'll need for the week, carefully calculated to fit within your budget.
2.  **🗓️ A 1-Week Meal Plan:** A delicious and varied 7-day meal plan, complete with recipes you can create using the groceries you've just bought. The plan is designed to be exciting, nutritious, and perfectly aligned with your preferences.

## 🛠️ Technology Stack

This project is built with a modern, powerful stack to deliver a seamless user experience.

### Frontend

| Technology                                                                                                  | Description                              |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **[SvelteKit](https://kit.svelte.dev/)**                                                                    | A cutting-edge framework for building fast, modern web applications. |
| **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**                                   | For building interactive web applications. |
| **[Vite](https://vitejs.dev/)**                                                                             | A next-generation frontend tooling for a blazing-fast development experience. |

### Backend

| Technology                                                                                                    | Description                              |
| ------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **[Python](https://www.python.org/)**                                                                         | The core language for our backend logic. |
| **[FastAPI](https://fastapi.tiangolo.com/)**                                                                  | A modern, high-performance web framework for building APIs. |
| **[Google Gemini](https://ai.google/discover/geminipro/)**                                                    | The AI model that powers our intelligent meal and grocery generation. |
| **[Pydantic](https://docs.pydantic.dev/)**                                                                    | For data validation and settings management. |

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v18 or higher)
- [Python](https://www.python.org/downloads/) (v3.9 or higher)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/food_app.git
    cd food_app
    ```

2.  **Set up the Backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r ../requirements.txt
    ```

3.  **Set up the Frontend:**
    ```bash
    cd ../frontend
    npm install
    ```

### Running the Application

1.  **Start the Backend Server:**
    
    Open a terminal, navigate to the `backend` directory, and run:
    ```bash
    uvicorn main:app --reload
    ```
    The backend API will be running at `http://127.0.0.1:8000`.

2.  **Start the Frontend Development Server:**

    Open a second terminal, navigate to the `frontend` directory, and run:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`.

---

<p align="center">
  Made with ❤️ for food lovers everywhere. 
</p> 