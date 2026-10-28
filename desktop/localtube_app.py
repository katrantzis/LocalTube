"""LocalTube desktop starter.

This version downloads directly linked MP3/MP4 files from sources the user is
authorized to download. It intentionally does not extract media from YouTube
pages or bypass provider restrictions.
"""
from __future__ import annotations

import ipaddress
import os
import re
import socket
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

APP_NAME = "LocalTube"
DOWNLOADS = Path.home() / "Downloads"
MAX_BYTES = 2 * 1024 * 1024 * 1024  # 2 GiB safety limit


def validate_public_url(raw: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(raw.strip())
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Bitte gib einen gültigen HTTP- oder HTTPS-Link ein.")
    if parsed.username or parsed.password:
        raise ValueError("Links mit eingebetteten Zugangsdaten werden nicht unterstützt.")
    try:
        addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))
    except socket.gaierror as exc:
        raise ValueError("Der Hostname konnte nicht aufgelöst werden.") from exc
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0])
        if not ip.is_global:
            raise ValueError("Aus Sicherheitsgründen sind lokale oder private Netzwerkadressen nicht erlaubt.")
    return parsed


def safe_filename(name: str, extension: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")
    name = name[:140] or "download"
    if not name.lower().endswith(extension):
        name += extension
    return name


class LocalTubeApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("LocalTube")
        root.geometry("620x490")
        root.minsize(480, 430)
        root.configure(bg="#10131b")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#10131b")
        style.configure("TLabel", background="#10131b", foreground="#f2f5fa", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 25, "bold"), foreground="#b8f36b")
        style.configure("Hint.TLabel", foreground="#a0aabd", font=("Segoe UI", 9))
        style.configure("TButton", padding=9, font=("Segoe UI", 10, "bold"))
        style.configure("TEntry", padding=8)

        frame = ttk.Frame(root, padding=26)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="LocalTube", style="Header.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Direktlinks · lokal gespeichert · ohne Konto", style="Hint.TLabel").pack(anchor="w", pady=(2, 24))

        ttk.Label(frame, text="Direkter Link zu einer Datei").pack(anchor="w", pady=(0, 7))
        self.url = tk.StringVar()
        ttk.Entry(frame, textvariable=self.url).pack(fill="x", ipady=4)

        ttk.Label(frame, text="Format").pack(anchor="w", pady=(20, 7))
        self.format = tk.StringVar(value="mp3")
        format_row = ttk.Frame(frame)
        format_row.pack(anchor="w")
        ttk.Radiobutton(format_row, text="MP3 · Audio", value="mp3", variable=self.format).pack(side="left", padx=(0, 20))
        ttk.Radiobutton(format_row, text="MP4 · Video", value="mp4", variable=self.format).pack(side="left")

        self.rights = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Ich darf diese Datei herunterladen.", variable=self.rights).pack(anchor="w", pady=(19, 0))

        self.button = ttk.Button(frame, text="In Downloads speichern", command=self.start_download)
        self.button.pack(fill="x", pady=(18, 12))
        self.status = tk.StringVar(value=f"Speicherort: {DOWNLOADS}")
        ttk.Label(frame, textvariable=self.status, wraplength=550).pack(anchor="w")
        ttk.Label(
            frame,
            text="Hinweis: Diese Startversion lädt direkte MP3-/MP4-Dateilinks. "
                 "Sie wandelt keine YouTube-Seiten in Dateien um und umgeht keine Schutzmaßnahmen.",
            style="Hint.TLabel", wraplength=550, justify="left"
        ).pack(anchor="w", pady=(20, 0))

    def start_download(self):
        raw = self.url.get().strip()
        extension = self.format.get()
        if not self.rights.get():
            messagebox.showinfo(APP_NAME, "Bitte bestätige, dass du zum Download berechtigt bist.")
            return
        if not raw:
            messagebox.showinfo(APP_NAME, "Füge zuerst einen direkten Dateilink ein.")
            return
        self.button.configure(state="disabled")
        self.status.set("Link wird geprüft …")
        threading.Thread(target=self.download, args=(raw, extension), daemon=True).start()

    def download(self, raw: str, extension: str):
        try:
            parsed = validate_public_url(raw)
            request = urllib.request.Request(raw, headers={"User-Agent": "LocalTube/1.0"})
            with urllib.request.urlopen(request, timeout=25) as response:
                final = urllib.parse.urlparse(response.geturl())
                if final.scheme not in ("http", "https") or not final.hostname:
                    raise ValueError("Unerwartetes Weiterleitungsziel.")
                if response.status != 200:
                    raise ValueError(f"Der Server antwortete mit HTTP {response.status}.")
                content_type = response.headers.get_content_type().lower()
                if content_type.startswith("text/") or content_type in ("text/html", "application/json"):
                    raise ValueError("Der Link scheint keine direkte Mediendatei zu sein.")
                length = response.headers.get("Content-Length")
                if length and int(length) > MAX_BYTES:
                    raise ValueError("Die Datei ist größer als das Sicherheitslimit von 2 GiB.")

                path_name = urllib.parse.unquote(Path(final.path).name)
                desired = "." + extension
                if Path(path_name).suffix.lower() not in (".mp3", ".mp4", ".m4a", ".m4v"):
                    raise ValueError("Der Link enthält keine erkennbare MP3-/MP4-Dateiendung.")
                filename = safe_filename(path_name, desired)
                DOWNLOADS.mkdir(parents=True, exist_ok=True)
                destination = DOWNLOADS / filename
                counter = 1
                while destination.exists():
                    destination = DOWNLOADS / f"{Path(filename).stem} ({counter}){desired}"
                    counter += 1

                total = 0
                with destination.open("wb") as out:
                    while True:
                        chunk = response.read(1024 * 128)
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > MAX_BYTES:
                            out.close()
                            destination.unlink(missing_ok=True)
                            raise ValueError("Die Datei überschreitet das Sicherheitslimit von 2 GiB.")
                        out.write(chunk)
            self.root.after(0, self.finish, f"Fertig: {destination}", None)
        except (ValueError, urllib.error.URLError, TimeoutError, OSError) as exc:
            self.root.after(0, self.finish, f"Download nicht abgeschlossen: {exc}", str(exc))
        except Exception:
            self.root.after(0, self.finish, "Download fehlgeschlagen. Bitte prüfe den Link.", "Der Download ist fehlgeschlagen.")

    def finish(self, text: str, error: str | None):
        self.status.set(text)
        self.button.configure(state="normal")
        if error:
            messagebox.showerror(APP_NAME, error)
        else:
            messagebox.showinfo(APP_NAME, "Datei wurde im Windows-Ordner Downloads gespeichert.")


if __name__ == "__main__":
    window = tk.Tk()
    LocalTubeApp(window)
    window.mainloop()
