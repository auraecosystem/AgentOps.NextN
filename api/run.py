# api/run.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "agentops.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["agentops"],  # Only watch specific directories
        reload_excludes=["*.pyc", "*.log"],  # Exclude certain files
    )
