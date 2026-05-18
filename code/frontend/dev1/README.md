# Repository Explorer Frontend

This is a modern React application built with TypeScript, Vite, and Vanilla CSS. It provides a beautiful, ChatGPT-like interface for managing repositories and interacting with an LLM trained/indexed on your codebase.

## Prerequisites

Before running the frontend, ensure you have the following running:
1. **Node.js** (v18 or higher recommended)
2. **FastAPI Backend**: The backend API should be running locally (default: `http://localhost:8000`).
3. **LLM Server**: The local LLM server (like `llama-server.exe`) should be running locally (default: `http://localhost:8080`).

## Setup Instructions

1. **Navigate to the frontend directory**
   ```bash
   cd code/frontend/dev1
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   Ensure the `.env` file exists in the root of the frontend directory (`code/frontend/dev1/.env`) with the following contents:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_WS_BASE_URL=ws://localhost:8000
   ```
   *Note: Adjust the ports if your backend server runs on a different port.*

4. **Start the Development Server**
   ```bash
   npm run dev
   ```

5. **Open the Application**
   Open your browser and navigate to the local URL provided in the terminal (usually `http://localhost:5173`).

## Usage

- **Add a Project**: Click the `+` icon in the sidebar to add a new GitHub repository URL. The backend will clone and index it.
- **Select a Project**: Click on a project in the sidebar to view its details.
- **Update a Project**: Use the "Update Project" button to trigger a re-indexing.
- **Start Chatting**: Click "New Chat" inside a project to start a conversation with the LLM about that specific repository. Messages stream in real-time over WebSockets and support Markdown formatting.

## Tech Stack
- **React 19**
- **TypeScript**
- **Vite**
- **React Router v6** (for navigation)
- **Lucide React** (for icons)
- **React Markdown & Remark GFM** (for formatting LLM responses)
