"""Application entrypoint."""

import uvicorn


def main() -> None:
    """Start the Hummel IT Frame web service."""
    uvicorn.run("hummel_it_frame.web.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
