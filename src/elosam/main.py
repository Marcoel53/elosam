from .application import EloSamApplication
from .version import VERSION


def main() -> None:
    app = EloSamApplication()

    print("=" * 40)
    print(f"EloSam {VERSION}")
    print("=" * 40)

    app.start()

    print(f"STATUS: {app.state.name}")


if __name__ == "__main__":
    main()
