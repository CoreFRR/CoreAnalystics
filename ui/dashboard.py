import customtkinter as ctk


MODULES = [
    ("💻", "CPU / RAM",    "Performances processeur\net mémoire vive",  "#4f6ef7"),
    ("💾", "Disque Dur",   "Santé et espace\ndisponible",                "#10b981"),
    ("🌐", "Réseau",       "Latence et vitesse\nde connexion",            "#f59e0b"),
    ("📋", "Logs Système", "Erreurs et événements\nWindows",              "#ef4444"),
]


class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("CoreAnalystics")
        self.parent.geometry("820x580")
        self.parent.resizable(True, True)
        self.parent.configure(fg_color="#0f0f13")
        self._center_window()
        self._build_ui()

    def _center_window(self):
        self.parent.update_idletasks()
        w = self.parent.winfo_screenwidth()
        h = self.parent.winfo_screenheight()
        self.parent.geometry(f"820x580+{(w//2)-410}+{(h//2)-290}")

    def _build_ui(self):
        header = ctk.CTkFrame(self.parent, fg_color="#1a1a2e", corner_radius=0, height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="🖥️  CoreAnalystics",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#7c83ff"
        ).pack(side="left", padx=24, pady=18)

        ctk.CTkLabel(
            header,
            text="v0.1",
            font=ctk.CTkFont(size=11),
            text_color="#475569"
        ).pack(side="right", padx=24)

        ctk.CTkLabel(
            self.parent,
            text="Choisissez un module d'analyse",
            font=ctk.CTkFont(size=15),
            text_color="#94a3b8"
        ).pack(pady=(30, 20))

        grid = ctk.CTkFrame(self.parent, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        grid.columnconfigure((0, 1), weight=1, uniform="col")
        grid.rowconfigure((0, 1), weight=1, uniform="row")

        for i, (icon, title, desc, color) in enumerate(MODULES):
            row, col = divmod(i, 2)
            self._make_card(grid, icon, title, desc, color, row, col)

        footer = ctk.CTkFrame(self.parent, fg_color="#1a1a2e", corner_radius=0, height=38)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkLabel(
            footer,
            text="Les modules seront activés progressivement",
            font=ctk.CTkFont(size=11),
            text_color="#334155"
        ).pack(pady=10)

    def _make_card(self, parent, icon, title, desc, color, row, col):
        card = ctk.CTkFrame(
            parent,
            fg_color="#1a1a2e",
            corner_radius=14,
            border_width=1,
            border_color="#2d2d4e"
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkFrame(card, fg_color=color, height=4, corner_radius=2).pack(fill="x")

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=34)
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#e2e8f0"
        ).pack()

        ctk.CTkLabel(
            card,
            text=desc,
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
            justify="center"
        ).pack(pady=(6, 16))

        ctk.CTkButton(
            card,
            text="Bientôt disponible",
            fg_color="#0f172a",
            hover_color="#1e293b",
            text_color="#475569",
            font=ctk.CTkFont(size=11),
            height=32,
            corner_radius=8,
            state="disabled"
        ).pack(pady=(0, 18), padx=20, fill="x")
