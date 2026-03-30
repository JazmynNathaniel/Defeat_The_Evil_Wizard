try:
    from .game import main
except ImportError:
    from game import main


if __name__ == "__main__":
    main()
