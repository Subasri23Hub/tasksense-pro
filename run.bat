@echo off
echo ============================================
echo   TaskSense Pro - Setup Script
echo ============================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo [3/4] Building vector store...
python -c "from core.retriever import build_vectorstore; build_vectorstore(); print('Vector store built!')"

echo [4/4] Done! Starting the app...
echo.
echo ============================================
echo   Open your browser at: http://localhost:8501
echo ============================================
echo.
streamlit run app.py
