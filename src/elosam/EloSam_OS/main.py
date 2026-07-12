from elosam.app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("ELOSAM OS DESKTOP BETA 1.9")
    print("=" * 60)
    print("Dashboard: http://127.0.0.1:8080")
    print("API:       http://127.0.0.1:8080/api/status")
    print("Docs:      http://127.0.0.1:8080/docs")
    print("=" * 60)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        log_level="info",
    )


