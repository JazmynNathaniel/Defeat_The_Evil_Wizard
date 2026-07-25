#THIS IS YOUR CLI ENTRY POINT, YOU CANNOT RUN THE GAME FROM ANY OTHER FILE
#SHIFT+R IN THIS FILE 

try:
    from .game import main
except ImportError:
    from game import main


if __name__ == "__main__":
    main()
