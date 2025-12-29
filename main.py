#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import json
import re
import shutil
import socket
import subprocess
import sys
import unicodedata

# Import PIP packages
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QSpacerItem
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

# Import local packages
from pytubefix import Playlist
from pytubefix import YouTube
from pytubefix.cli import on_progress as progressdownload

# Define 'VERSION'
VERSION = "v1.3.5"

# Define 'APPNAME'
APPNAME = "TubeReaver"

# Define 'WEBSITEURL'
WEBSITEURL = "https://neoslab.com"

# Define 'CONFIGPATH'
CONFIGPATH = Path.home() / ".config" / "tubereaver"

# Define 'CONFIGFILE'
CONFIGFILE = CONFIGPATH / "tubereaver.conf"

# Define 'ITAGS'
ITAGS: List[Tuple[int, str]] = [
    (18, "360p MP4 (progressive, video+audio)"),
    (22, "720p MP4 (progressive, video+audio)"),
    (137, "1080p MP4 (video-only/DASH)"),
    (248, "1080p WebM (video-only/DASH)"),
    (313, "2160p (4K) WebM (video-only/DASH)"),
    (399, "1080p MP4 (AV1 video-only/DASH)"),
    (140, "m4a (audio-only)"),
    (251, "webm/opus (audio-only)"),
]

# Define 'GENRES'
GENRES: List[str] = [
    "A capella",
    "Abstract",
    "Acid",
    "Acid Jazz",
    "Acid Punk",
    "Acoustic",
    "Alternative",
    "Alternative Rock",
    "Ambient",
    "Anime",
    "Art Rock",
    "Audio Theatre",
    "Audiobook",
    "Avantgarde",
    "Ballad",
    "Baroque",
    "Bass",
    "Beat",
    "Bebop",
    "Bhangra",
    "Big Band",
    "Big Beat",
    "Black Metal",
    "Bluegrass",
    "Blues",
    "Booty Bass",
    "Breakbeat",
    "BritPop",
    "Cabaret",
    "Celtic",
    "Chamber Music",
    "Chanson",
    "Chillout",
    "Chorus",
    "Christian Gangsta Rap",
    "Christian Rap",
    "Christian Rock",
    "Classic Rock",
    "Classical",
    "Club",
    "Club-House",
    "Comedy",
    "Contemporary Christian",
    "Country",
    "Crossover",
    "Cult",
    "Dance",
    "Dance Hall",
    "Darkwave",
    "Death Metal",
    "Disco",
    "Downtempo",
    "Dream",
    "Drum & Bass",
    "Drum Solo",
    "Dub",
    "Dubstep",
    "Duet",
    "Easy Listening",
    "EBM",
    "Eclectic",
    "Electro",
    "Electroclash",
    "Electronic",
    "Emo",
    "Ethnic",
    "Euro-House",
    "Euro-Techno",
    "Eurodance",
    "Experimental",
    "Fast Fusion",
    "Folk",
    "Folk-Rock",
    "Folklore",
    "Freestyle",
    "Funk",
    "Fusion",
    "G-Funk",
    "Game",
    "Gangsta",
    "Garage",
    "Garage Rock",
    "Global",
    "Goa",
    "Gospel",
    "Gothic",
    "Gothic Rock",
    "Grunge",
    "Hard Rock",
    "Hardcore Techno",
    "Heavy Metal",
    "Hip-Hop",
    "House",
    "Humour",
    "IDM",
    "Illbient",
    "Index,Title",
    "Indie",
    "Indie Rock",
    "Industrial",
    "Industro-Goth",
    "Instrumental",
    "Instrumental Pop",
    "Instrumental Rock",
    "Italian",
    "Jam Band",
    "Jazz",
    "Jazz & Funk",
    "Jpop",
    "Jungle",
    "Krautrock",
    "Latin",
    "Leftfield",
    "Lo-Fi",
    "Lounge",
    "Math Rock",
    "Meditative",
    "Merengue",
    "Metal",
    "Musical",
    "National Folk",
    "Native US",
    "Negerpunk",
    "Neoclassical",
    "Neue Deutsche Welle",
    "New Age",
    "New Romantic",
    "New Wave",
    "Noise",
    "Nu-Breakz",
    "Oldies",
    "Opera",
    "Other",
    "Podcast",
    "Polka",
    "Polsk Punk",
    "Pop",
    "Pop-Folk",
    "Pop/Funk",
    "Porn Groove",
    "Post-Punk",
    "Post-Rock",
    "Power Ballad",
    "Pranks",
    "Primus",
    "Progressive Rock",
    "Psybient",
    "Psychadelic",
    "Psychedelic Rock",
    "Psytrance",
    "Punk",
    "Punk Rock",
    "R&B",
    "Rap",
    "Ragga",
    "Rave",
    "Reggae",
    "Reggaeton",
    "Retro",
    "Revival",
    "Rhythmic Soul",
    "Rock",
    "Rock'n Roll",
    "Salsa",
    "Samba",
    "Satire",
    "Shoegaze",
    "Showtunes",
    "Ska",
    "Slow Jam",
    "Slow Rock",
    "Sonata",
    "Soul",
    "Sound Clip",
    "Soundtrack",
    "Southern Rock",
    "Space",
    "Space Rock",
    "Speech",
    "Swing",
    "Symphonic Rock",
    "Symphony",
    "Synthpop",
    "Tango",
    "Techno",
    "Techno-Industrial",
    "Terror",
    "Thrash Metal",
    "Top 40",
    "Trailer",
    "Trance",
    "Tribal",
    "Trip-Hop",
    "Trop Rock",
    "Variété",
    "Vocal",
    "World Music",
]


# Class 'SysUtils'
class SysUtils:
    """
    Utility helpers for system-related operations used across the application.
    Provides functions to format sizes, timestamps, and ensure FFmpeg is available.
    Designed to be stateless with only static methods.
    """

    # Function 'unitsize'
    @staticmethod
    def unitsize(numbytes: int) -> str:
        """
        Convert a raw byte size into a human-readable string (KB, MB, GB, etc.).
        Safely handles invalid inputs and negative values by coercing to zero.
        Returns a string formatted with two decimal places and the unit suffix.
        """
        try:
            n = max(0, int(numbytes))
        except (ValueError, TypeError):
            n = 0
        units = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
        x = float(n)
        i = 0
        while x >= 1024 and i < len(units) - 1:
            x /= 1024.0
            i += 1
        return f"{x:.2f} {units[i]}"

    # Function 'mtimestring'
    @staticmethod
    def mtimestring(p: Path) -> str:
        """
        Convert a file's modification time into a human-readable timestamp string.
        Handles permission, I/O, and missing file errors by returning a dash.
        The returned format is 'YYYY-MM-DD HH:MM:SS' in local time.
        """
        try:
            return datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        except (OSError, ValueError, PermissionError, FileNotFoundError):
            return "-"

    # Function 'ffmpegnotice'
    @staticmethod
    def ffmpegnotice() -> None:
        """
        Ensure that FFmpeg is available in the current environment PATH.
        If FFmpeg is missing, raise a RuntimeError with basic install hints.
        Used before any audio conversion or tagging operations are performed.
        """
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "FFmpeg not found. Please install FFmpeg to convert/tag audio.\n"
                "• macOS:  brew install ffmpeg\n"
                "• Linux:  sudo apt install ffmpeg\n"
                "• Windows: choco install ffmpeg (or download from ffmpeg.org)"
            )

    # Function 'metaparams'
    @staticmethod
    def metaparams(meta: Dict[str, str]) -> list:
        """
        Build a list of FFmpeg '-metadata' arguments from a metadata dictionary.
        Only recognized keys (title, artist, album, album_artist, genre) are used.
        Returns a flat list of command-line arguments ready to append to FFmpeg.
        """
        args: list = []
        meta = {**(meta or {})}
        meta.setdefault("encoded_by", "www.tubereaver.com")
        mapping = {
            "title": "title",
            "artist": "artist",
            "album": "album",
            "album_artist": "album_artist",
            "genre": "genre",
            "encoded_by": "encoded_by",
        }

        for k, v in meta.items():
            if not v:
                continue
            ffk = mapping.get(k)
            if not ffk:
                continue
            args += ["-metadata", f"{ffk}={v}"]
        return args


# Class 'TextUtils'
class TextUtils:
    """
    Text and filename related helper utilities used by the downloader.
    Provides functions for cleaning titles, building slugs, and title-casing.
    All methods are static and side-effect free for easy reuse.
    """

    # Function 'remparentheses'
    @staticmethod
    def remparentheses(text: str) -> str:
        """
        Strip any parenthesized segments from a text string, including spaces.
        Useful for removing version notes like '(Official Video)' from titles.
        Returns the cleaned text with duplicated spaces collapsed and trimmed.
        """
        if not text:
            return text
        text = re.sub(r"\([^)]*\)", "", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip()

    # Function 'slugify'
    @staticmethod
    def slugify(text: str) -> str:
        """
        Convert an arbitrary string to a filesystem-safe slug in ASCII.
        Removes accents, lowercases characters, and replaces non-alphanumerics with dashes.
        Returns a clean slug without leading or trailing dashes.
        """
        if not text:
            return ""
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        text = re.sub(r"-{2,}", "-", text).strip("-")
        return text

    # Function 'slugname'
    @staticmethod
    def slugname(provided_filename: Optional[str], fallback_title: str) -> str:
        """
        Build a slugged base filename from either a user-supplied filename or title.
        Removes file extensions and parenthesized parts, then delegates to slugify().
        Returns an empty string if no usable text is available.
        """
        base = provided_filename.strip() if provided_filename else (fallback_title or "")
        base = Path(base).stem if base else ""
        base = TextUtils.remparentheses(base)
        return TextUtils.slugify(base)

    # Function 'titlecase'
    @staticmethod
    def titlecase(title: str) -> str:
        """
        Convert a title string to a simple title-case style.
        Lowercases the full string and capitalizes the first character.
        Returns an empty string when given falsy input.
        """
        if not title:
            return ""
        t = title.strip().lower()
        return t[:1].upper() + t[1:]


# Class 'ConfigManager'
class ConfigManager:
    """
    Simple configuration loader/saver for TubeReaver settings.
    Uses a plain text key=value file under the user's config directory.
    Only non-sensitive values are persisted; passwords are kept in memory only.
    """

    # Function 'load'
    @staticmethod
    def load() -> Dict[str, str]:
        """
        Load all configuration entries from the config file into a dictionary.
        Ignores empty lines, comments, and malformed entries without '='.
        Returns an empty dict if the file does not exist or cannot be read.
        """
        data: Dict[str, str] = {}
        try:
            if CONFIGFILE.is_file():
                for line in CONFIGFILE.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    data[k.strip()] = v.strip()
        except (OSError, UnicodeDecodeError):
            pass
        return data

    # Function 'save'
    @staticmethod
    def save(settings: Dict[str, str]) -> None:
        """
        Persist selected configuration settings to disk as key=value pairs.
        The config directory is created if needed, and sensitive keys are skipped.
        Any I/O errors are silently ignored to avoid breaking the GUI flow.
        """
        try:
            CONFIGPATH.mkdir(parents=True, exist_ok=True)
            lines = []
            for k, v in settings.items():
                if k == "auth_password":
                    continue
                lines.append(f"{k}={v}")
            CONFIGFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except OSError:
            pass


# Class 'DialogPrefs'
class DialogPrefs(QDialog):
    """
    Preferences dialog allowing the user to adjust general and auth settings.
    Manages output directory, default download mode, and audio and tagging options.
    Reads from the provided settings dict and exposes updated values on accept.
    """

    # Function '__init__'
    def __init__(self, parent: QWidget, settings: Dict[str, str]):
        """
        Initialize the preference dialog UI with current settings values.
        Creates tabs for general download options and authentication/OAuth choices.
        Stores changes locally until the dialog is accepted by the user.
        """
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.resize(780, 560)
        self.settings = settings.copy()

        self.settings.setdefault("outputdir", str(Path.home() / "Downloads"))
        self.settings.setdefault("default_mode", "Highest MP4")
        self.settings.setdefault("audiotype", "m4a")
        self.settings.setdefault("prefix", "")
        self.settings.setdefault("suffix", "")
        self.settings.setdefault("itagvalue", str(22))
        self.settings.setdefault("use_oauth", "0")
        self.settings.setdefault("allow_cache", "1")
        self.settings.setdefault("auth_email", "")
        self.passwordmemory = ""
        tabs = QTabWidget(self)

        wgen = QWidget()
        g = QFormLayout(wgen)

        self.editoutput = QLineEdit(self.settings.get("outputdir", str(Path.home() / "Downloads")))
        btnbrowse = QPushButton("Browse…")
        outrow = QHBoxLayout()
        outrow.setContentsMargins(0, 0, 0, 0)
        outrow.addWidget(self.editoutput)
        outrow.addWidget(btnbrowse)

        self.cmbdefaultmode = QComboBox()
        self.cmbdefaultmode.addItems(["Highest MP4", "Audio-only", "itag"])
        self.cmbdefaultmode.setCurrentText(self.settings.get("default_mode", "Highest MP4"))

        self.cmbaudiotype = QComboBox()
        self.cmbaudiotype.addItems(["m4a", "mp3"])
        self.cmbaudiotype.setCurrentText(self.settings.get("audiotype", "m4a"))

        self.editprefix = QLineEdit(self.settings.get("prefix", ""))
        self.editsuffix = QLineEdit(self.settings.get("suffix", ""))

        self.cmbitag = QComboBox()
        for val, label in ITAGS:
            self.cmbitag.addItem(label, val)

        try:
            currentitag = int(self.settings.get("itagvalue", "22"))
        except ValueError:
            currentitag = 22
        idx = max(0, next((i for i in range(self.cmbitag.count()) if self.cmbitag.itemData(i) == currentitag), 0))
        self.cmbitag.setCurrentIndex(idx)

        g.addRow(QLabel("Output directory:"), QWidget())
        g.addRow(outrow)
        g.addRow(QLabel("Default download mode:"), self.cmbdefaultmode)
        g.addRow(QLabel("Default audio type:"), self.cmbaudiotype)
        g.addRow(QLabel("Filename prefix:"), self.editprefix)
        g.addRow(QLabel("Filename suffix:"), self.editsuffix)
        g.addRow(QLabel("Default iTag:"), self.cmbitag)

        wauth = QWidget()
        h = QFormLayout(wauth)

        self.chkoauth = QCheckBox("Use OAuth (recommended for age-restricted or gated content)")
        self.chkoauth.setChecked(self.settings.get("use_oauth", "0") in ("1", "true", "True", "yes"))
        self.chkcache = QCheckBox("Allow OAuth Cache (persist refresh token securely on your machine)")
        self.chkcache.setChecked(self.settings.get("allow_cache", "1") in ("1", "true", "True", "yes"))

        self.editemail = QLineEdit(self.settings.get("auth_email", ""))
        self.editpassword = QLineEdit("")  # not persisted
        self.editpassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.editpassword.setPlaceholderText("(Not required for OAuth; not saved to disk)")

        h.addRow(self.chkoauth)
        h.addRow(self.chkcache)
        h.addRow(QLabel("Email address:"), self.editemail)
        h.addRow(QLabel("Password:"), self.editpassword)

        tabs.addTab(wgen, "General")
        tabs.addTab(wauth, "Authentication")

        # Buttons
        btns = QDialogButtonBox()
        btnok = QPushButton("OK")
        btncancel = QPushButton("Cancel")
        btns.addButton(btnok, QDialogButtonBox.ButtonRole.AcceptRole)
        btns.addButton(btncancel, QDialogButtonBox.ButtonRole.RejectRole)

        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addStretch(1)
        layout.addWidget(btns)

        btnbrowse.clicked.connect(self.browseout)
        btnok.clicked.connect(self.accept)
        btncancel.clicked.connect(self.reject)

    # Function 'browseout'
    def browseout(self) -> None:
        """
        Open a directory selection dialog for choosing the output folder.
        Starts from the current output path or the user home directory by default.
        When a folder is chosen, update the corresponding line edit widget.
        """
        base = self.editoutput.text().strip() or str(Path.home())
        d = QFileDialog.getExistingDirectory(self, "Choose output directory", base)
        if d:
            self.editoutput.setText(d)

    # Function 'addvalues'
    def addvalues(self) -> Dict[str, str]:
        """
        Collect the current UI values and merge them into a new settings dict.
        Updates mode, audio type, filename prefix/suffix, OAuth flags and iTag.
        Also caches the password in memory without persisting it to disk.
        """
        out: Dict[str, str] = self.settings.copy()
        out["outputdir"] = self.editoutput.text().strip()
        out["default_mode"] = self.cmbdefaultmode.currentText()
        out["audiotype"] = self.cmbaudiotype.currentText()
        out["prefix"] = self.editprefix.text().strip()
        out["suffix"] = self.editsuffix.text().strip()
        out["itagvalue"] = str(self.cmbitag.currentData())
        out["use_oauth"] = "1" if self.chkoauth.isChecked() else "0"
        out["allow_cache"] = "1" if self.chkcache.isChecked() else "0"
        out["auth_email"] = self.editemail.text().strip()
        self.passwordmemory = self.editpassword.text()
        return out

    # Function 'passwdmemory'
    def passwdmemory(self) -> str:
        """
        Return the password value that was entered in the preferences dialog.
        This value is kept only in memory and never written to the config file.
        Intended for temporary use by components that need runtime credentials.
        """
        return self.passwordmemory


# Class 'DialogAbout'
class DialogAbout(QDialog):
    """
    Modal dialog that shows general information about the TubeReaver app.
    Displays name, version, a short description and a link to the website.
    Optionally loads and displays an application logo if it can be found.
    """

    # Function '__init__'
    def __init__(self, parent: Optional[QWidget], version: str, website: str):
        """
        Initialize the About dialog with the given version string and website URL.
        Sets up labels, logo image, and a close button within a vertical layout.
        The dialog is centered over its parent when shown by the caller.
        """
        super().__init__(parent)
        self.setWindowTitle(f"About {APPNAME}")
        self.setModal(True)
        self.setMinimumSize(520, 360)

        logolabel = QLabel()
        logolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logopath = [
            Path("/usr/share/pixmaps/tubereaver.png")
        ]

        pix: Optional[QPixmap] = None
        for pth in logopath:
            if pth.is_file():
                tmp = QPixmap(str(pth))
                if not tmp.isNull():
                    pix = tmp
                    break
        if pix:
            logolabel.setPixmap(
                pix.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        title = QLabel(f"<b>{APPNAME}</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px;")

        ver = QLabel(f"Version: {version}")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)

        link = QLabel(f'<a href="{website}">{website}</a>')
        link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link.setTextFormat(Qt.TextFormat.RichText)
        link.setOpenExternalLinks(True)

        msg = QLabel(
            "Automatic YouTube downloader\n"
            "Download videos, playlists, and audio"
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #999;")

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, parent=self)
        btns.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(logolabel)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(ver)
        layout.addWidget(msg)
        layout.addWidget(link)
        layout.addStretch(1)
        layout.addSpacing(10)
        layout.addWidget(btns)


# Class 'DialogCompleted'
class DialogCompleted(QDialog):
    """
    Modal dialog that informs the user when downloads have completed.
    Can represent either a success state or a failure with an error message.
    Also tries to show a success/error icon if the corresponding file exists.
    """

    # Function '__init__'
    def __init__(self, parent: Optional[QWidget], error_message: Optional[str] = None):
        """
        Build the completion dialog UI with title, icon, message, and close button.
        The title and icon differ depending on whether an error message is passed.
        Keeps the content simple so it can be reused after each batch of downloads.
        """
        super().__init__(parent)
        self.setWindowTitle("Download Completed" if not error_message else "Download Failed")
        self.setModal(True)
        self.setMinimumSize(420, 280)

        iconlabel = QLabel()
        iconlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconpath = [
            Path("/usr/share/tubereaver/icons/success.png")
        ] if not error_message else [
            Path("/usr/share/tubereaver/icons/error.png")
        ]

        pix: Optional[QPixmap] = None
        for pth in iconpath:
            if pth.is_file():
                tmp = QPixmap(str(pth))
                if not tmp.isNull():
                    pix = tmp
                    break
        if pix:
            iconlabel.setPixmap(
                pix.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        title = QLabel(
            "<b>All downloads finished successfully</b>" if not error_message else "<b>Some downloads failed</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg = QLabel(
            "All selected files have been downloaded\n"
            "You can safely close this window"
            if not error_message
            else f"{error_message}\nPlease review logs or try again"
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, parent=self)
        btns.rejected.connect(self.reject)
        btns.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(iconlabel)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(msg)
        layout.addStretch(1)
        layout.addSpacing(10)
        layout.addWidget(btns)

    # Function 'showcenter'
    def showcenter(self) -> None:
        """
        Center the dialog over its parent widget and execute it modally.
        Adjusts size to fit contents before computing the center position.
        If no parent is available, it simply executes without repositioning.
        """
        self.adjustSize()
        if self.parent() and isinstance(self.parent(), QWidget):
            parent: QWidget = self.parent()
            center = parent.geometry().center()
            self.move(center - self.rect().center())
        self.exec()


# Class 'DownloadTask'
@dataclass
class DownloadTask:
    """
    Container dataclass describing a single download job configuration.
    Holds URL, playlist flag, mode, audio type, paths, and tagging metadata.
    Instances are passed from the GUI to the DownloadWorker thread.
    """

    # Define 'useoauth'
    useoauth: bool

    # Define 'allowcache'
    allowcache: bool

    # Define 'url'
    url: str

    # Define 'isplaylist'
    isplaylist: bool

    # Define 'mode'
    mode: str

    # Define 'audiotype'
    audiotype: str

    # Define 'itag'
    itag: Optional[int]

    # Define 'outputdir'
    outputdir: str

    # Define 'filename'
    filename: str

    # Define 'prefix'
    prefix: str

    # Define 'suffix'
    suffix: str

    # Define 'tagtitle'
    tagtitle: str

    # Define 'tagartist'
    tagartist: str

    # Define 'tagalbum'
    tagalbum: str

    # Define 'tagalbumartist'
    tagalbumartist: str

    # Define 'taggenre'
    taggenre: str

    # Define 'coverimage'
    coverimage: str


# Class 'DownloadWorker'
class DownloadWorker(QThread):
    """
    Worker thread responsible for fetching and saving YouTube videos/audio.
    Uses pytubefix to handle streams and emits Qt signals to update the GUI.
    Can process either a single URL or all items in a playlist transparently.
    """

    # Define 'sigprogress'
    sigprogress = pyqtSignal(str, int)

    # Define 'sigstatus'
    sigstatus = pyqtSignal(str, str)

    # Define 'signitemstart'
    signitemstart = pyqtSignal(str, str, str)

    # Define 'sigitemdone'
    sigitemdone = pyqtSignal(str, str, int, str)

    # Define 'sigitemerror'
    sigitemerror = pyqtSignal(str, str)

    # Define 'sigitemcomplete'
    sigitemcomplete = pyqtSignal(bool, str)

    # Function '__init__'
    def __init__(self, task: DownloadTask, parent=None):
        """
        Initialize the worker with a DownloadTask and optional parent object.
        Stores the task and sets internal error tracking variables to defaults.
        Signals must be connected by the GUI before invoking the worker logic.
        """
        super().__init__(parent)
        self.task = task
        self.anyerror = False
        self.errmsg = ""

    # Function 'run'
    def run(self) -> None:
        """
        Qt thread entry point delegating to download logic.
        Keeps heavy download operations off the main GUI thread.
        Uses startdownloads() to perform the actual work safely.
        """
        self.startdownloads()

    # Function 'convtomp3'
    @staticmethod
    def convtomp3(inputfile: Path, meta: Dict[str, str] | None = None, bitrate: str = "192k",
        samplerate: str = "44100", coverimage: Optional[Path] = None) -> Path:
        """
        Convert an input audio file to MP3 format using FFmpeg with metadata.
        Optionally embeds a cover image and ID3 tags, then deletes the source file.
        Returns the path to the newly created MP3 file, raising on FFmpeg failure.
        """
        SysUtils.ffmpegnotice()
        outputfile = inputfile.with_suffix(".mp3")

        cmd = ["ffmpeg", "-y", "-i", str(inputfile)]
        if coverimage and coverimage.is_file():
            cmd += [
                "-i", str(coverimage),
                "-map", "0:a",
                "-map", "1:v",
                "-c:a", "libmp3lame",
                "-b:a", bitrate,
                "-ar", samplerate,
                "-id3v2_version", "3",
                "-metadata:s:v", "title=Album cover",
                "-metadata:s:v", "comment=Cover (front)",
            ]
        else:
            cmd += [
                "-vn",
                "-c:a", "libmp3lame",
                "-b:a", bitrate,
                "-ar", samplerate,
                "-id3v2_version", "3",
            ]

        cmd += SysUtils.metaparams(meta or {})
        cmd += ["-f", "mp3", str(outputfile)]

        proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if proc.returncode != 0:
            raise RuntimeError("FFmpeg failed to convert to MP3.")
        try:
            inputfile.unlink()
        except OSError:
            pass
        return outputfile

    # Function 'm4atagsapply'
    @staticmethod
    def m4atagsapply(inputfile: Path, meta: Dict[str, str] | None = None, coverimage: Optional[Path] = None) -> Path:
        """
        Apply metadata and optional cover art to an existing M4A audio file.
        Uses FFmpeg to create a tagged temporary output file and then replaces the original.
        Returns the final file path, raising an error if FFmpeg processing fails.
        """
        SysUtils.ffmpegnotice()
        tmp_out = inputfile.with_suffix(".tagged.m4a")
        cmd = ["ffmpeg", "-y", "-i", str(inputfile)]

        if coverimage and coverimage.is_file():
            cmd += [
                "-i", str(coverimage),
                "-map", "0:a",
                "-map", "1:v",
                "-c", "copy",
                "-disposition:v:1", "attached_pic",
            ]
        else:
            cmd += ["-vn", "-c", "copy"]

        cmd += SysUtils.metaparams(meta or {})
        cmd += [str(tmp_out)]
        proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if proc.returncode != 0:
            raise RuntimeError("FFmpeg failed to apply metadata to M4A.")
        try:
            inputfile.unlink()
            tmp_out.rename(inputfile)
        except OSError:
            pass
        return inputfile

    # Function 'metafromtask'
    def metafromtask(self, originaltitle: str | None = None) -> Dict[str, str]:
        """
        Build a metadata dictionary based on task tag fields and video title.
        Prefers explicit task tags, falling back to a cleaned version of the title.
        Only includes non-empty values, suitable for passing into FFmpeg helpers.
        """
        meta: Dict[str, str] = {}
        if self.task.tagtitle:
            meta["title"] = self.task.tagtitle
        elif originaltitle:
            cleaned = TextUtils.remparentheses(originaltitle)
            meta["title"] = TextUtils.titlecase(cleaned)

        if self.task.tagartist:
            meta["artist"] = self.task.tagartist
        if self.task.tagalbum:
            meta["album"] = self.task.tagalbum
        if self.task.tagalbumartist:
            meta["album_artist"] = self.task.tagalbumartist
        if self.task.taggenre:
            meta["genre"] = self.task.taggenre
        return meta

    # Function 'coverpath'
    def coverpath(self) -> Optional[Path]:
        """
        Resolve the cover image path from the task into a validated Path object.
        Expands user shortcuts like '~' and checks that the file actually exists.
        Returns None if no valid image path is configured on the task.
        """
        path = (self.task.coverimage or "").strip()
        if not path:
            return None
        p = Path(path).expanduser()
        if p.is_file():
            return p
        return None

    # Function 'showprogress'
    def showprogress(self, rowkey: str):
        """
        Create a progress callback closure bound to a specific table row key.
        Computes a percentage based on remaining bytes and emits a Qt signal.
        Falls back to pytubefix's on_progress handler if size information is missing.
        """

        # Function 'callbackprogress'
        def callbackprogress(stream, chunk, rembytes):
            """Inner callback used by pytubefix to report per-chunk progress."""
            try:
                if self.isInterruptionRequested():
                    raise RuntimeError("Download interrupted by user.")
                total = getattr(stream, "filesize", None) or getattr(stream, "filesize_approx", None)
                if not total:
                    return progressdownload(stream, chunk, rembytes)
                done = int((1 - (rembytes / total)) * 100)
                done = max(0, min(100, done))
                self.sigprogress.emit(rowkey, done)
            except (AttributeError, ZeroDivisionError, TypeError):
                progressdownload(stream, chunk, rembytes)

        return callbackprogress

    # Function 'startdownloads'
    def startdownloads(self) -> None:
        """
        Entry point for running the download task, handling errors and completion.
        Selects between single-video and playlist workflows based on the task.
        Always emits the completion signal with success flag and last error text.
        """
        try:
            if self.task.isplaylist:
                self.runplaylist()
            else:
                self.runsingle()
        except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as e:
            self.anyerror = True
            self.errmsg = str(e)
        finally:
            self.sigitemcomplete.emit(not self.anyerror, self.errmsg)

    # Function 'prepareoutput'
    def prepareoutput(self) -> Path:
        """
        Ensure that the configured output directory exists on disk.
        Creates intermediate folders if required and returns the resulting Path.
        Raises no error if the directory already exists or is created successfully.
        """
        outdir = Path(self.task.outputdir).expanduser()
        outdir.mkdir(parents=True, exist_ok=True)
        return outdir

    # Function 'finalbase'
    def finalbase(self, title: str) -> str:
        """
        Compute the final base filename for a video or audio item.
        Combines optional title, artist, prefix, and suffix into a slugified string.
        Ensures a stable, safe filename for use across all download modes.
        """
        effectivetitle = self.task.tagtitle or title
        cleanedfilename = TextUtils.remparentheses(effectivetitle)
        base = TextUtils.slugname(self.task.filename, cleanedfilename)

        if self.task.tagartist:
            artist_clean = TextUtils.remparentheses(self.task.tagartist)
            artist_slug = TextUtils.slugify(artist_clean)
            if artist_slug:
                base = f"{artist_slug}-{base}" if base else artist_slug

        if self.task.prefix:
            pre = TextUtils.slugify(TextUtils.remparentheses(self.task.prefix))
            base = f"{pre}-{base}" if base else pre

        if self.task.suffix:
            suf = TextUtils.slugify(TextUtils.remparentheses(self.task.suffix))
            base = f"{base}-{suf}" if base else suf
        return base

    # Function 'runsingle'
    def runsingle(self) -> None:
        """
        Handle downloading a single YouTube video according to the task options.
        Selects the appropriate stream (itag, audio-only, or highest resolution).
        Emits row start, progress, status, and completion signals for the GUI.
        """
        if self.isInterruptionRequested():
            raise RuntimeError("Download interrupted by user.")

        outdir = self.prepareoutput()
        rowkey = f"{self.task.url}::0"

        yt = YouTube(
            self.task.url,
            use_oauth=self.task.useoauth,
            allow_oauth_cache=self.task.allowcache,
            on_progress_callback=self.showprogress(rowkey),
        )

        title = yt.title or "video"
        base = self.finalbase(title)

        self.signitemstart.emit(rowkey, title, base or "")
        coverpath = self.coverpath()

        if self.task.mode == "itag" and self.task.itag is not None:
            stream = yt.streams.get_by_itag(self.task.itag)
            if not stream:
                raise RuntimeError(f"itag {self.task.itag} not found for this video.")
            if self.isInterruptionRequested():
                raise RuntimeError("Download interrupted by user.")
            saved = (
                stream.download(output_path=str(outdir), filename=base)
                if base
                else stream.download(output_path=str(outdir))
            )
            finalpath = Path(saved)

        elif self.task.mode == "Audio-only":
            stream = yt.streams.get_audio_only()
            if self.isInterruptionRequested():
                raise RuntimeError("Download interrupted by user.")
            saved = (
                stream.download(output_path=str(outdir), filename=base)
                if base
                else stream.download(output_path=str(outdir))
            )
            meta = self.metafromtask(originaltitle=title)
            if self.task.audiotype == "mp3":
                finalpath = self.convtomp3(Path(saved), meta=meta, coverimage=coverpath)
            else:
                finalpath = self.m4atagsapply(Path(saved), meta=meta, coverimage=coverpath)

        else:
            stream = yt.streams.get_highest_resolution()
            if self.isInterruptionRequested():
                raise RuntimeError("Download interrupted by user.")
            saved = (
                stream.download(output_path=str(outdir), filename=base)
                if base
                else stream.download(output_path=str(outdir))
            )
            finalpath = Path(saved)

        try:
            size = finalpath.stat().st_size
        except (OSError, FileNotFoundError):
            size = 0
        self.sigprogress.emit(rowkey, 100)
        self.sigstatus.emit(rowkey, "Completed")
        self.sigitemdone.emit(rowkey, str(finalpath), size, SysUtils.mtimestring(finalpath))

    # Function 'runplaylist'
    def runplaylist(self) -> None:
        """
        Process all entries in a YouTube playlist as a batch download.
        Iterates over videos, applies the same task options, and reports per-item status.
        Marks items as errored when an itag is missing but continues with remaining videos.
        """
        outdir = self.prepareoutput()
        pl = Playlist(self.task.url)
        coverpath = self.coverpath()

        index = 0
        for vid in pl.videos:
            if self.isInterruptionRequested():
                self.anyerror = True
                self.errmsg = "Download interrupted by user."
                break

            rowkey = f"{vid.watch_url}::{index}"
            yt = YouTube(
                vid.watch_url,
                use_oauth=self.task.useoauth,
                allow_oauth_cache=self.task.allowcache,
                on_progress_callback=self.showprogress(rowkey),
            )
            title = yt.title or f"video-{index + 1}"
            base = self.finalbase(title)
            self.signitemstart.emit(rowkey, title, base or "")

            if self.task.mode == "Audio-only":
                stream = yt.streams.get_audio_only()
                if self.isInterruptionRequested():
                    self.anyerror = True
                    self.errmsg = "Download interrupted by user."
                    break
                saved = (
                    stream.download(output_path=str(outdir), filename=base)
                    if base
                    else stream.download(output_path=str(outdir))
                )
                meta = self.metafromtask(originaltitle=title)
                if self.task.audiotype == "mp3":
                    finalpath = self.convtomp3(Path(saved), meta=meta, coverimage=coverpath)
                else:
                    finalpath = self.m4atagsapply(Path(saved), meta=meta, coverimage=coverpath)
            elif self.task.mode == "itag" and self.task.itag is not None:
                stream = yt.streams.get_by_itag(self.task.itag)
                if not stream:
                    self.anyerror = True
                    self.sigitemerror.emit(
                        rowkey,
                        f"itag {self.task.itag} not available for this entry.",
                    )
                    index += 1
                    continue
                if self.isInterruptionRequested():
                    self.anyerror = True
                    self.errmsg = "Download interrupted by user."
                    break
                saved = (
                    stream.download(output_path=str(outdir), filename=base)
                    if base
                    else stream.download(output_path=str(outdir))
                )
                finalpath = Path(saved)
            else:
                stream = yt.streams.get_highest_resolution()
                if self.isInterruptionRequested():
                    self.anyerror = True
                    self.errmsg = "Download interrupted by user."
                    break
                saved = (
                    stream.download(output_path=str(outdir), filename=base)
                    if base
                    else stream.download(output_path=str(outdir))
                )
                finalpath = Path(saved)

            try:
                size = finalpath.stat().st_size
            except (OSError, FileNotFoundError):
                size = 0
            self.sigprogress.emit(rowkey, 100)
            self.sigstatus.emit(rowkey, "Completed")
            self.sigitemdone.emit(rowkey, str(finalpath), size, SysUtils.mtimestring(finalpath))
            index += 1


# Class 'TubeReaver'
class TubeReaver(QWidget):
    """
    Main application widget providing the TubeReaver GUI interface.
    Hosts URL input, tagging fields, progress table, and menu actions.
    Orchestrates download workers and updates the user interface via signals.
    """

    # Function '__init__'
    def __init__(self):
        """
        Initialize the main window, menus, controls, and default state.
        Loads configuration settings, wires up signals, and builds layouts.
        Prepares all widgets required to collect user input and show progress.
        """
        super().__init__()
        self.setWindowTitle(f"{APPNAME} {VERSION} - YouTube Downloader GUI")
        self.resize(1100, 760)

        menubar = QMenuBar(self)
        mfile = menubar.addMenu("File")
        actquit = QAction("Quit", self)
        actquit.triggered.connect(QApplication.quit)
        mfile.addAction(actquit)

        medit = menubar.addMenu("Edit")
        actprefs = QAction("Preferences", self)
        actprefs.triggered.connect(self.onprefs)
        medit.addAction(actprefs)

        mhelp = menubar.addMenu("Help")
        actabout = QAction("About", self)
        actabout.triggered.connect(self.onabout)
        mhelp.addAction(actabout)

        self.settings: Dict[str, str] = ConfigManager.load()
        self.settings.setdefault("outputdir", str(Path.home() / "Downloads"))
        self.settings.setdefault("default_mode", "Highest MP4")
        self.settings.setdefault("audiotype", "m4a")
        self.settings.setdefault("prefix", "")
        self.settings.setdefault("suffix", "")
        self.settings.setdefault("itagvalue", str(22))
        self.settings.setdefault("use_oauth", "0")
        self.settings.setdefault("allow_cache", "1")
        self.settings.setdefault("auth_email", "")
        self._authpasswordmemory = ""

        form = QGroupBox("Download")
        f = QFormLayout()

        self.editurl = QLineEdit()
        self.editurl.setPlaceholderText(
            "https://www.youtube.com/watch?v=…  or  https://www.youtube.com/playlist?list=…")
        self.chkplaylist = QCheckBox("Treat as Playlist")
        self.chkplaylist.setToolTip("Check to download all items of the provided playlist URL.")

        sepone = QFrame()
        sepone.setFrameShape(QFrame.Shape.HLine)
        sepone.setFrameShadow(QFrame.Shadow.Sunken)

        self.cmbmode = QComboBox()
        self.cmbmode.addItems(["Highest MP4", "Audio-only", "itag"])
        self.cmbmode.setCurrentText(self.settings.get("default_mode", "Highest MP4"))

        self.cmbaudiotype = QComboBox()
        self.cmbaudiotype.addItems(["m4a", "mp3"])
        self.cmbaudiotype.setCurrentText(self.settings.get("audiotype", "m4a"))

        self.editfilename = QLineEdit()
        self.editfilename.setPlaceholderText("(Optional) desired base filename (slugged). Leave empty to use title")

        septwo = QFrame()
        septwo.setFrameShape(QFrame.Shape.HLine)
        septwo.setFrameShadow(QFrame.Shadow.Sunken)

        self.edittagtitle = QLineEdit()
        self.edittagtitle.setPlaceholderText("(Optional) Audio tag Title")
        self.edittagartist = QLineEdit()
        self.edittagartist.setPlaceholderText("(Optional) Audio tag Artist")
        self.edittagalbum = QLineEdit()
        self.edittagalbum.setPlaceholderText("(Optional) Audio tag Album")
        self.edittagalbumartist = QLineEdit()
        self.edittagalbumartist.setPlaceholderText("(Optional) Audio tag Album Artist")

        self.cmbtaggenre = QComboBox()
        self.cmbtaggenre.setEditable(True)
        self.cmbtaggenre.addItems(GENRES)
        self.cmbtaggenre.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.cmbtaggenre.setPlaceholderText("(Optional) Audio tag Genre")

        self.editcover = QLineEdit()
        self.editcover.setPlaceholderText("(Optional) Cover image (JPEG/PNG/WebP) for audio")
        btncoverbrowse = QPushButton("Browse…")
        coverlayout = QHBoxLayout()
        coverlayout.setContentsMargins(0, 0, 0, 0)
        coverlayout.setSpacing(4)
        coverlayout.addWidget(self.editcover)
        coverlayout.addWidget(btncoverbrowse)
        coverwidget = QWidget()
        coverwidget.setLayout(coverlayout)

        self.btnrun = QPushButton("Download")
        self.btnstop = QPushButton("Stop")
        self.btnstop.setEnabled(False)

        f.addRow(QLabel("URL:"), self.editurl)
        f.addRow(self.chkplaylist)
        f.addItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        f.addRow(sepone)

        f.addItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        f.addRow(QLabel("Mode:"), self.cmbmode)
        f.addRow(QLabel("Audio type:"), self.cmbaudiotype)
        f.addRow(QLabel("Filename:"), self.editfilename)

        f.addItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        f.addRow(septwo)
        f.addItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        f.addRow(QLabel("Tags (audio):"), QLabel())
        f.addRow(QLabel("Title:"), self.edittagtitle)
        f.addRow(QLabel("Artist:"), self.edittagartist)
        f.addRow(QLabel("Album:"), self.edittagalbum)
        f.addRow(QLabel("Album Artist:"), self.edittagalbumartist)
        f.addRow(QLabel("Genre:"), self.cmbtaggenre)
        f.addRow(QLabel("Cover:"), coverwidget)

        form.setLayout(f)
        self.lbltotal = QLabel("Downloaded Size\n0.00 MB")
        self.lbltotal.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbltotal.setStyleSheet("font-weight: 600;")

        controlsrow = QHBoxLayout()
        controlsrow.addWidget(self.btnrun)
        controlsrow.addWidget(self.btnstop)
        controlsrow.addStretch(1)
        controlsrow.addWidget(self.lbltotal)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Title", "URL", "File", "Datetime", "Size", "Progress"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(True)

        root = QVBoxLayout()
        root.setMenuBar(menubar)
        root.addWidget(form)
        root.addLayout(controlsrow)
        root.addWidget(self.table, stretch=1)
        self.setLayout(root)

        self.rows: Dict[str, int] = {}
        self.rowbars: Dict[str, QProgressBar] = {}
        self.totalbytes = 0
        self.worker: Optional[DownloadWorker] = None
        self.fadeanimation: Optional[QPropertyAnimation] = None
        self._last_error_text = ""

        self.btnrun.clicked.connect(self.onrun)
        self.btnstop.clicked.connect(self.onstop)
        btncoverbrowse.clicked.connect(self.browsecover)

    # Function 'browsecover'
    def browsecover(self) -> None:
        """
        Open a file picker dialog to choose a cover image for audio tagging.
        Filters to common image formats but allows selecting any file if needed.
        When a file is chosen, its path is written into the cover line edit.
        """
        base = self.editcover.text().strip() or str(Path.home())
        fname, _ = QFileDialog.getOpenFileName(
            self,
            "Choose cover image",
            base,
            "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All files (*)",
        )
        if fname:
            self.editcover.setText(fname)

    # Function 'taskcollect'
    def taskcollect(self) -> DownloadTask:
        """
        Build a DownloadTask instance based on the current UI state.
        Validates that a URL is present and infers playlist mode from content.
        Reads preferences such as output directory and audio type from settings.
        """
        url = self.editurl.text().strip()
        if not url:
            raise RuntimeError("Please enter a YouTube video or playlist URL.")
        isplaylist = self.chkplaylist.isChecked() or ("playlist" in url and "list=" in url)
        mode = self.cmbmode.currentText()
        audiotype = self.cmbaudiotype.currentText()

        try:
            itag = int(self.settings.get("itagvalue", "22")) if mode == "itag" else None
        except ValueError:
            itag = None

        outputdir = self.settings.get("outputdir", str(Path.home() / "Downloads"))
        filename = self.editfilename.text().strip()
        prefix = self.settings.get("prefix", "")
        suffix = self.settings.get("suffix", "")
        useoauth = self.settings.get("use_oauth", "0") in ("1", "true", "True", "yes")
        allowcache = self.settings.get("allow_cache", "1") in ("1", "true", "True", "yes")
        coverimage = self.editcover.text().strip()

        return DownloadTask(
            url=url,
            isplaylist=isplaylist,
            mode=mode,
            audiotype=audiotype,
            itag=itag,
            outputdir=outputdir,
            filename=filename,
            prefix=prefix,
            suffix=suffix,
            useoauth=useoauth,
            allowcache=allowcache,
            tagtitle=self.edittagtitle.text().strip(),
            tagartist=self.edittagartist.text().strip(),
            tagalbum=self.edittagalbum.text().strip(),
            tagalbumartist=self.edittagalbumartist.text().strip(),
            taggenre=self.cmbtaggenre.currentText().strip(),
            coverimage=coverimage,
        )

    # Function 'preparetable'
    def preparetable(self) -> None:
        """
        Reset the progress table and related tracking state before a new run.
        Clears rows, resets progress bars, total downloaded size, and error text.
        Ensures the UI reflects a fresh state when starting new downloads.
        """
        self.table.setRowCount(0)
        self.rows.clear()
        self.rowbars.clear()
        self.totalbytes = 0
        self.lbltotal.setText("Downloaded Size\n0.00 MB")
        self._last_error_text = ""

    # Function 'workersignals'
    def workersignals(self, w: DownloadWorker) -> None:
        """
        Connect all worker signals to the corresponding handler methods.
        Binds start, progress, status, done, error, and completion events.
        Must be called before running the worker to keep the UI in sync.
        """
        w.signitemstart.connect(self.onrowstart)
        w.sigprogress.connect(self.onrowprogress)
        w.sigstatus.connect(self.onrowstatus)
        w.sigitemdone.connect(self.onrowdone)
        w.sigitemerror.connect(self.onrowerror)
        w.sigitemcomplete.connect(self.onworkerdone)

    # Function 'workerstart'
    def workerstart(self, task: DownloadTask) -> None:
        """
        Start a new DownloadWorker for the given task if none is running.
        Guards against concurrent runs and updates the enabled state of buttons.
        Immediately invokes the worker's main logic method instead of QThread.run().
        """
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Busy", "A download is already running.")
            return

        self.btnstop.setEnabled(True)
        self.btnrun.setEnabled(False)
        self.worker = DownloadWorker(task, parent=self)
        self.workersignals(self.worker)
        self.worker.start()

    # Function 'addrow'
    def addrow(self, rowkey: str, title: str, url: str, saved: str, status: str) -> int:
        """
        Insert a new row into the progress table and initialize its widgets.
        Sets columns for title, URL, saved file, and status, plus a QProgressBar.
        Stores row index and progress bar in dictionaries keyed by rowkey.
        """
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(title))
        self.table.setItem(r, 1, QTableWidgetItem(url))
        self.table.setItem(r, 2, QTableWidgetItem(saved))
        self.table.setItem(r, 3, QTableWidgetItem(""))
        self.table.setItem(r, 4, QTableWidgetItem(status))

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        self.table.setCellWidget(r, 5, bar)

        self.rows[rowkey] = r
        self.rowbars[rowkey] = bar
        return r

    # Function 'setrowprogress'
    def setrowprogress(self, rowkey: str, pct: int) -> None:
        """
        Update the progress bar of a specific row based on a row key.
        Clamps the percentage between 0 and 100 to keep the bar valid.
        Does nothing if the given row key is unknown or already removed.
        """
        bar = self.rowbars.get(rowkey)
        if bar:
            bar.setValue(max(0, min(100, int(pct))))

    # Function 'setrowstatus'
    def setrowstatus(self, rowkey: str, status: str) -> None:
        """
        Change the status text column for a table row identified by row key.
        Leaves the table untouched when the row key is not found.
        Typically used to reflect states like 'Downloading…' or 'Completed'.
        """
        r = self.rows.get(rowkey)
        if r is not None:
            self.table.setItem(r, 4, QTableWidgetItem(status))

    # Function 'setrowsaved'
    def setrowsaved(self, rowkey: str, saved_path: str) -> None:
        """
        Update the 'Saved File' column for a particular row key.
        Used after a download finishes to show the full path of the output file.
        Silently ignores missing rows (e.g., if the table was cleared).
        """
        r = self.rows.get(rowkey)
        if r is not None:
            self.table.setItem(r, 2, QTableWidgetItem(saved_path))

    # Function 'setrowmtime'
    def setrowmtime(self, rowkey: str, mtime: str) -> None:
        """
        Update the 'Mtime' column for a given row identified by row key.
        Stores the human-readable modification time string in the table cell.
        Silently ignores unknown rows that may have been cleared earlier.
        """
        r = self.rows.get(rowkey)
        if r is not None:
            self.table.setItem(r, 3, QTableWidgetItem(mtime))

    # Function 'onprefs'
    def onprefs(self) -> None:
        """
        Open the preferences dialog and apply changes if the user accepts.
        Saves updated settings to disk and synchronizes relevant UI elements.
        Also stores any in-memory password value for temporary use.
        """
        dlg = DialogPrefs(self, self.settings)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.settings = dlg.addvalues()
            self._authpasswordmemory = dlg.passwdmemory()
            ConfigManager.save(self.settings)
            self.cmbmode.setCurrentText(self.settings.get("default_mode", "Highest MP4"))
            self.cmbaudiotype.setCurrentText(self.settings.get("audiotype", "m4a"))

    # Function 'onabout'
    def onabout(self) -> None:
        """
        Show the 'About' dialog containing version and website information.
        Executes the dialog modally and returns only when it is closed.
        This handler is connected to the Help → About menu action.
        """
        dlg = DialogAbout(self, VERSION, WEBSITEURL)
        dlg.exec()

    # Function 'onrun'
    def onrun(self) -> None:
        """
        Start a new download session based on the current user inputs.
        Validates the task, resets the progress table, and spawns a worker.
        Shows a warning message box when required input is missing or invalid.
        """
        try:
            task = self.taskcollect()
        except (RuntimeError, ValueError) as e:
            QMessageBox.warning(self, "Input error", str(e))
            return

        self.preparetable()
        self.workerstart(task)

    # Function 'onstop'
    def onstop(self) -> None:
        """
        Attempt to stop an ongoing download worker in a best-effort manner.
        Requests interruption, informs the user, and disables the Stop button.
        Does not forcibly kill the worker but signals that it should exit soon.
        """
        if self.worker and self.worker.isRunning():
            try:
                self.worker.requestInterruption()
            except (RuntimeError, AttributeError):
                pass
            QMessageBox.information(
                self,
                "Stopping",
                "Stopping the current downloads (best effort).",
            )
        self.btnstop.setEnabled(False)

    # Function 'onrowstart'
    def onrowstart(self, rowkey: str, title: str, base: str) -> None:
        """
        Slot called when the worker begins processing a new item.
        Adds a new row to the table with initial 'Starting' status.
        Uses the row key to associate future progress and status updates.
        """
        self.addrow(rowkey, title, rowkey.split("::")[0], base, "Starting")

    # Function 'onrowprogress'
    def onrowprogress(self, rowkey: str, pct: int) -> None:
        """
        Slot that updates a row's progress bar and status while downloading.
        Displays a human-friendly 'Downloading…' label alongside the percentage.
        Called repeatedly by the worker's progress callback function.
        """
        self.setrowprogress(rowkey, pct)
        self.setrowstatus(rowkey, "Wait…")

    # Function 'onrowstatus'
    def onrowstatus(self, rowkey: str, message: str) -> None:
        """
        Slot that sets a row's status text directly from the worker.
        Allows the worker to report intermediate or final messages to the user.
        Used for states like 'Completed' or custom error messages per item.
        """
        self.setrowstatus(rowkey, message)

    # Function 'onrowdone'
    def onrowdone(self, rowkey: str, saved_path: str, bytes_size: int, mtime: str) -> None:
        """
        Slot called when an item finishes downloading successfully.
        Marks the row as saved, sets progress to 100%, and aggregates total size.
        Updates the label showing the cumulative downloaded volume.
        """
        self.setrowprogress(rowkey, 100)
        self.setrowmtime(rowkey, mtime)
        self.setrowstatus(rowkey, SysUtils.unitsize(bytes_size))
        self.setrowsaved(rowkey, saved_path)
        try:
            self.totalbytes += int(bytes_size)
        except (ValueError, TypeError, OverflowError):
            pass
        self.lbltotal.setText(f"Downloaded Size\n{SysUtils.unitsize(self.totalbytes)}")

    # Function 'onrowerror'
    def onrowerror(self, rowkey: str, errmsg: str) -> None:
        """
        Slot invoked when a specific playlist entry fails to download.
        Records the error message, marks the row status as an error, and clears progress.
        The most recent error text is also cached for use in the final summary dialog.
        """
        self._last_error_text = errmsg
        self.setrowstatus(rowkey, f"Error: {errmsg}")
        self.setrowprogress(rowkey, 0)

    # Function 'onworkerdone'
    def onworkerdone(self, success: bool, errmsg: str) -> None:
        """
        Slot called when the download worker signals overall completion.
        Re-enables the Run button, disables Stop, and shows a completion dialog.
        Afterwards triggers a fade-out animation to clear the table contents.
        """
        self.btnstop.setEnabled(False)
        self.btnrun.setEnabled(True)

        err = errmsg or (self._last_error_text or None)
        dlg = DialogCompleted(self, error_message=(err if not success else None))
        dlg.showcenter()
        self.fadecleaner()

    # Function 'fadecleaner'
    def fadecleaner(self) -> None:
        """
        Animate the table with a fade-out effect and clear its contents afterward.
        Applies a QGraphicsOpacityEffect to smoothly transition to transparency.
        Once the animation finishes, the table is reset and opacity is restored.
        """
        if self.table.rowCount() == 0:
            return

        effect = QGraphicsOpacityEffect(self.table)
        self.table.setGraphicsEffect(effect)
        effect.setOpacity(1.0)

        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(700)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)

        # Function 'fadeafter'
        def fadeafter() -> None:
            """Clear rows and remove the opacity effect after the fade animation."""
            self.table.setRowCount(0)
            self.table.setGraphicsEffect(None)

        anim.finished.connect(fadeafter)
        self.fadeanimation = anim
        anim.start()


# Class 'UpdateChecker'
class UpdateChecker:
    """
    Check GitHub releases for a newer version.
    Show a modal popup reusing the About-style layout.
    Intended to be called once at application startup.
    """

    # Function '__init__'
    def __init__(self, parent: QWidget, appname: str, currvers: str, gitrepo: str,
                 logo_paths: Optional[List[Path]] = None):
        """
        Store configuration needed for update checks.
        Accepts parent widget, app name, current version and repo.
        Optional logo paths override the default guessed location.
        """
        self.parent = parent
        self.appname = appname
        self.currvers = currvers
        self.gitrepo = gitrepo
        self.logo_paths = logo_paths or [
            Path(f"/usr/share/pixmaps/{appname.lower()}.png")
        ]

    # Function 'versionparser'
    @staticmethod
    def versionparser(ver: str) -> Tuple[int, ...]:
        """
        Parse a version string like 'v1.2.3' into integers.
        Ignores any non-numeric suffixes after the core numbers.
        Returns a tuple suitable for safe semantic comparison.
        """
        v = ver.strip()
        if v.startswith(("v", "V")):
            v = v[1:]
        parts: List[int] = []
        for part in v.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break
        return tuple(parts) or (0,)

    # Function 'checknewer'
    def checknewer(self, current: str, latest: str) -> bool:
        """
        Compare two version strings in semantic order.
        Pads shorter tuples with zeros before comparison.
        Returns True when latest is strictly greater.
        """
        c = self.versionparser(current)
        l = self.versionparser(latest)
        ln = max(len(c), len(l))
        c = c + (0,) * (ln - len(c))
        l = l + (0,) * (ln - len(l))
        return c < l

    # Function 'checknotify'
    def checknotify(self, timeout: int = 3):
        """
        Perform a single update check against GitHub releases.
        If a newer tag exists, show the update popup dialog.
        Intended to be called from the main GUI thread.
        """
        latest = self.fetchtag(timeout=timeout)
        if not latest:
            return
        if not self.checknewer(self.currvers, latest):
            return
        url = f"https://github.com/{self.gitrepo}/releases/tag/{latest}"
        self.showupdate(latest, url)

    # Function 'fetchtag'
    def fetchtag(self, timeout: int = 3) -> Optional[str]:
        """
        Call GitHub API to obtain the latest release tag.
        Uses /repos/{repo}/releases/latest with a short timeout.
        Returns the tag name string or None on any failure.
        """
        try:
            url = f"https://api.github.com/repos/{self.gitrepo}/releases/latest"
            req = Request(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": self.appname,
                },
            )
            with urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8", "ignore"))

            tag = str(data.get("tag_name") or "").strip()
            return tag or None

        except (HTTPError, URLError, socket.timeout, ValueError, OSError):
            return None

    # Function 'showupdate'
    def showupdate(self, latest: str, url: str):
        """
        Build and display the update popup dialog.
        Reuses the About layout with logo, text and link.
        Blocks until user closes the window or presses OK.
        """
        dlg = QDialog(self.parent)
        dlg.setWindowTitle("Update Available")
        dlg.setModal(True)
        dlg.setMinimumSize(520, 360)

        logolabel = QLabel()
        logolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pix: Optional[QPixmap] = None
        for pth in self.logo_paths:
            if pth.is_file():
                tmp = QPixmap(str(pth))
                if not tmp.isNull():
                    pix = tmp
                    break
        if pix:
            logolabel.setPixmap(
                pix.scaled(
                    96,
                    96,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        title = QLabel(f"<b>A new version of {self.appname} is available</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px;")

        ver = QLabel(f"Current version {self.currvers}\nLatest version {latest}")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)

        msg = QLabel(
            "A newer release is available on GitHub.\n"
            "Please download the latest version from the link below."
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #999;")

        link = QLabel(f'<a href="{url}">{url}</a>')
        link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link.setTextFormat(Qt.TextFormat.RichText)
        link.setOpenExternalLinks(True)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, parent=dlg)
        btns.accepted.connect(dlg.accept)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(logolabel)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(ver)
        layout.addWidget(msg)
        layout.addWidget(link)
        layout.addStretch(1)
        layout.addSpacing(10)
        layout.addWidget(btns)
        dlg.exec()


# Class 'AppEntry'
class AppEntry:
    """
    Application bootstrapper encapsulating the Qt event loop startup logic.
    Creates a QApplication instance, instantiates the main TubeReaver window.
    Provides a single static main() entry point for running the GUI application.
    """

    # Function "main"
    @staticmethod
    def main() -> None:
        """
        Initialize QApplication, build the main window, and start the event loop.
        Ensures command-line arguments are passed through to Qt as usual.
        Exits the process with the return code from app.exec().
        """
        app = QApplication(sys.argv)

        if hasattr(QGuiApplication, "setDesktopFileName"):
            QGuiApplication.setDesktopFileName("tubereaver")

        app.setApplicationName(f"{APPNAME}")
        app.setWindowIcon(QIcon("/usr/share/pixmaps/tubereaver.png"))

        win = TubeReaver()
        win.show()

        checker = UpdateChecker(
            parent=win,
            appname=APPNAME,
            currvers=VERSION,
            gitrepo="neoslab/tubereaver",
            logo_paths=[Path("/usr/share/pixmaps/tubereaver.png")],
        )
        win.updatecheck = checker
        QTimer.singleShot(1500, checker.checknotify)
        sys.exit(app.exec())


# Callback
if __name__ == "__main__":
    AppEntry.main()
