import customtkinter as ctk


LOADING_STEPS = [
    (400,  "Vérification des mises à jour...", 0.15),
    (900,  "Chargement de l'interface...",     0.35),
    (1400, "Vérification du système...",       0.55),
    (1900, "Chargement des modules...",        0.75),
    (2400, "Prêt !",                           1.00),
]


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("")
        self.geometry("480x300")
        self.resizable(False, False)
        self.overrideredirect(True)
        self._center_window()
        self._build_ui()
        self._schedule_steps()

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"480x300+{(w//2)-240}+{(h//2)-150}")

    def _build_ui(self):
        self.configure(fg_color="#0f0f13")

        ctk.CTkLabel(
            self,
            text="🖥️  CoreAnalystics",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#7c83ff"
        ).pack(pady=(55, 4))

        ctk.CTkLabel(
            self,
            text="Analyse de votre système...",
            font=ctk.CTkFont(size=13),
            text_color="#64748b"
        ).pack(pady=(0, 28))

        self.progress_bar = ctk.CTkProgressBar(
            self, width=320, height=8, corner_radius=4,
            fg_color="#1e1e2e", progress_color="#7c83ff"
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 14))

        self.label_status = ctk.CTkLabel(
            self,
            text="Initialisation...",
            font=ctk.CTkFont(size=11),
            text_color="#475569"
        )
        self.label_status.pack()

    def _schedule_steps(self):
        for delay_ms, message, value in LOADING_STEPS:
            self.after(delay_ms, self._update_step, message, value)
        self.after(LOADING_STEPS[-1][0] + 600, self.destroy)

    def _update_step(self, message, value):
        self.progress_bar.set(value)
        self.label_status.configure(text=message)
