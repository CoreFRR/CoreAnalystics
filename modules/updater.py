import urllib.request
import json
import zipfile
import os
import sys
import shutil
import threading
import customtkinter as ctk


GITHUB_USER = "CoreFRR"
GITHUB_REPO = "CoreAnalystics"
VERSION     = "0.1.0"

API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"


def get_latest_release():
    try:
        req = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "CoreAnalystics-Updater"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        tag = data.get("tag_name", "").lstrip("v")

        zip_url = None
        for asset in data.get("assets", []):
            if asset["name"].endswith(".zip"):
                zip_url = asset["browser_download_url"]
                break

        return tag, zip_url

    except Exception:
        return None, None


def is_newer(remote_version, local_version):
    try:
        r = tuple(int(x) for x in remote_version.split("."))
        l = tuple(int(x) for x in local_version.split("."))
        return r > l
    except Exception:
        return False


def download_and_install(zip_url, progress_callback=None):
    tmp_zip = os.path.join(os.path.dirname(__file__), "..", "_update.zip")
    tmp_dir = os.path.join(os.path.dirname(__file__), "..", "_update_tmp")

    try:
        req = urllib.request.Request(
            zip_url,
            headers={"User-Agent": "CoreAnalystics-Updater"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0

            with open(tmp_zip, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0 and progress_callback:
                        progress_callback(downloaded / total)

        with zipfile.ZipFile(tmp_zip, "r") as zf:
            zf.extractall(tmp_dir)

        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        for root, dirs, files in os.walk(tmp_dir):
            for file in files:
                src = os.path.join(root, file)
                rel = os.path.relpath(src, tmp_dir)
                dst = os.path.join(app_dir, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

        os.remove(tmp_zip)
        shutil.rmtree(tmp_dir)

        os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        return str(e)


class UpdateWindow(ctk.CTkToplevel):
    def __init__(self, parent, current_version, new_version, zip_url):
        super().__init__(parent)

        self.zip_url = zip_url
        self.title("Mise à jour disponible")
        self.geometry("420x260")
        self.resizable(False, False)
        self.configure(fg_color="#0f0f13")
        self._center_window()
        self._build_ui(current_version, new_version)

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"420x260+{(w//2)-210}+{(h//2)-130}")

    def _build_ui(self, current, new):
        ctk.CTkLabel(
            self,
            text="🔄  Mise à jour disponible",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#7c83ff"
        ).pack(pady=(28, 6))

        ctk.CTkLabel(
            self,
            text=f"v{current}  →  v{new}",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        ).pack(pady=(0, 20))

        self.progress = ctk.CTkProgressBar(
            self, width=300, height=8, corner_radius=4,
            fg_color="#1e1e2e", progress_color="#7c83ff"
        )
        self.progress.set(0)
        self.progress.pack(pady=(0, 10))

        self.label_status = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11),
            text_color="#475569"
        )
        self.label_status.pack(pady=(0, 16))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        ctk.CTkButton(
            btn_frame, text="Mettre à jour",
            fg_color="#4f6ef7", hover_color="#3b5bdb",
            command=self._start_update, width=140
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_frame, text="Plus tard",
            fg_color="#1e1e2e", hover_color="#2d2d4e",
            text_color="#94a3b8",
            command=self.destroy, width=100
        ).pack(side="left", padx=8)

    def _start_update(self):
        self.label_status.configure(text="Téléchargement en cours...")

        def _progress(value):
            self.after(0, self.progress.set, value)
            self.after(0, self.label_status.configure,
                       {"text": f"Téléchargement... {int(value * 100)}%"})

        def _run():
            err = download_and_install(self.zip_url, _progress)
            if err:
                self.after(0, self.label_status.configure, {"text": f"Erreur : {err}"})

        threading.Thread(target=_run, daemon=True).start()


def check_for_update(parent_window):
    def _check():
        tag, zip_url = get_latest_release()
        if tag and zip_url and is_newer(tag, VERSION):
            parent_window.after(
                0, lambda: UpdateWindow(parent_window, VERSION, tag, zip_url)
            )

    threading.Thread(target=_check, daemon=True).start()
