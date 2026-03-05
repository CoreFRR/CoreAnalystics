import customtkinter as ctk
from ui.splash import SplashScreen
from ui.dashboard import Dashboard
from modules.updater import check_for_update

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    app = ctk.CTk()
    app.withdraw()

    splash = SplashScreen(app)
    app.wait_window(splash)

    Dashboard(app)
    app.deiconify()

    check_for_update(app)
    app.mainloop()


if __name__ == "__main__":
    main()
