"""Public command for the approved daily-card renderer."""
try:
    from .daily_card_visual import *
except ImportError:
    from daily_card_visual import *

if __name__ == "__main__":
    main()
