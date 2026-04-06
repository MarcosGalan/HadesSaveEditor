import os
import sys

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox,
    QTabWidget, QScrollArea, QGroupBox, QGridLayout, QCheckBox,
    QSpinBox, QFrame, QSizePolicy
)

from models.save_file import HadesSaveFile


# ── Palette ───────────────────────────────────────────────────────────────────
BG_DARK   = "#0a0812"
BG_PANEL  = "#13101e"
BG_CARD   = "#1b1728"
BG_INSET  = "#0f0c1a"
GOLD      = "#e8a020"
GOLD_DIM  = "#7a4e0a"
GOLD_PALE = "#ffe0a0"
ORANGE    = "#c0671a"
RED       = "#b03022"
TEXT      = "#ede6d6"
TEXT_DIM  = "#7a7060"
BORDER    = "#2e2840"
BORDER_LT = "#4a3e60"
GREEN     = "#2a8c50"
BLUE      = "#3a6e9c"

QSS = f"""
* {{
    font-family: 'Segoe UI', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
}}
QMainWindow, QDialog {{
    background-color: {BG_DARK};
}}
QWidget {{
    background-color: transparent;
    color: {TEXT};
    font-size: 13px;
}}

/* ─── Scrollbars ─────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: {BG_DARK};
    width: 6px;
    margin: 0;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_LT};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {GOLD_DIM};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}

/* ─── Title bar ──────────────────────────────────────────────── */
#titleBar {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #0e0606, stop:0.25 #1a1030, stop:0.75 #1a1030, stop:1 #0e0606);
    border-bottom: 2px solid {GOLD};
}}
#appTitle {{
    font-size: 32px;
    font-weight: 900;
    color: {GOLD};
    letter-spacing: 8px;
}}
#appSubtitle {{
    font-size: 10px;
    color: {TEXT_DIM};
    letter-spacing: 4px;
}}

/* ─── Action bar ─────────────────────────────────────────────── */
#actionBar {{
    background: {BG_PANEL};
    border-bottom: 1px solid {BORDER};
}}

/* ─── Path bar ───────────────────────────────────────────────── */
#pathBar {{
    background: {BG_DARK};
    border-bottom: 1px solid {BORDER};
}}
#pathKey {{
    color: {TEXT_DIM};
    font-size: 10px;
    letter-spacing: 2px;
}}
#pathValue {{
    color: {GOLD};
    font-size: 11px;
}}

/* ─── Tabs ───────────────────────────────────────────────────── */
QTabWidget::pane {{
    border: none;
    background: {BG_DARK};
}}
QTabWidget::tab-bar {{
    alignment: left;
}}
QTabBar::tab {{
    background: {BG_DARK};
    color: {TEXT_DIM};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 12px 28px;
    font-size: 12px;
    letter-spacing: 2px;
    min-width: 130px;
}}
QTabBar::tab:selected {{
    background: {BG_PANEL};
    color: {GOLD};
    border-bottom: 2px solid {GOLD};
    font-weight: bold;
}}
QTabBar::tab:hover:!selected {{
    background: {BG_CARD};
    color: {TEXT};
    border-bottom: 2px solid {BORDER_LT};
}}

/* ─── GroupBox ───────────────────────────────────────────────── */
QGroupBox {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-top: 2px solid {BORDER_LT};
    border-radius: 10px;
    margin-top: 18px;
    padding: 14px 16px 14px 16px;
    font-size: 11px;
    font-weight: bold;
    color: {TEXT_DIM};
    letter-spacing: 2px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 2px 10px;
    color: {TEXT_DIM};
    background: {BG_CARD};
    border-radius: 3px;
}}

/* ─── Inputs ─────────────────────────────────────────────────── */
QLineEdit {{
    background: {BG_INSET};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT};
    padding: 7px 12px;
    font-size: 15px;
    font-weight: bold;
    selection-background-color: {ORANGE};
}}
QLineEdit:focus {{
    border: 1px solid {GOLD};
    background: #120e1e;
}}
QSpinBox {{
    background: {BG_INSET};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT};
    padding: 5px 8px;
    font-size: 14px;
    font-weight: bold;
    min-width: 56px;
}}
QSpinBox:focus {{ border: 1px solid {GOLD}; }}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {BG_CARD};
    border: none;
    width: 20px;
    border-radius: 3px;
}}
QSpinBox::up-arrow   {{ width: 8px; height: 8px; }}
QSpinBox::down-arrow {{ width: 8px; height: 8px; }}

/* ─── Checkboxes ─────────────────────────────────────────────── */
QCheckBox {{
    color: {TEXT};
    spacing: 10px;
    font-size: 13px;
}}
QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid {BORDER_LT};
    border-radius: 5px;
    background: {BG_INSET};
}}
QCheckBox::indicator:checked {{
    background: {GOLD};
    border-color: {GOLD};
    image: none;
}}
QCheckBox::indicator:checked:hover {{ background: {GOLD_PALE}; }}

/* ─── Buttons ────────────────────────────────────────────────── */
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #3c2810, stop:1 #1e1208);
    border: 1px solid {GOLD_DIM};
    border-radius: 7px;
    color: {GOLD};
    font-weight: bold;
    font-size: 12px;
    padding: 9px 22px;
    letter-spacing: 1px;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #5c3c18, stop:1 #2e1c0c);
    border-color: {GOLD};
    color: {GOLD_PALE};
}}
QPushButton:pressed {{
    background: #100c04;
    padding-top: 10px;
    padding-bottom: 8px;
}}
QPushButton:disabled {{
    color: {TEXT_DIM};
    border-color: {BORDER};
    background: {BG_CARD};
}}
#btnPrimary {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #4a3014, stop:1 #241808);
    border: 1px solid {GOLD};
    font-size: 13px;
    padding: 10px 28px;
}}
#btnPrimary:hover {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #7a5020, stop:1 #3c2810);
}}
#btnMax {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #183040, stop:1 #0c1820);
    border: 1px solid {BLUE};
    color: #80c0f0;
    font-size: 12px;
}}
#btnMax:hover {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #284858, stop:1 #182838);
    color: #b0d8ff;
    border-color: #60a0e0;
}}
#btnDanger {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #3a1010, stop:1 #1e0808);
    border: 1px solid #7a3020;
    color: #e06060;
}}
#btnDanger:hover {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #5a1818, stop:1 #300c0c);
    color: #ff9090;
    border-color: {RED};
}}

/* ─── Labels ─────────────────────────────────────────────────── */
#tagLabel {{
    font-size: 9px;
    letter-spacing: 3px;
    color: {TEXT_DIM};
    text-transform: uppercase;
}}
#bigValue {{
    font-size: 22px;
    font-weight: bold;
    color: {TEXT};
}}
#weaponTitle {{
    font-size: 15px;
    font-weight: bold;
    color: {TEXT};
    letter-spacing: 1px;
}}
#weaponSub {{
    font-size: 10px;
    color: {TEXT_DIM};
    letter-spacing: 2px;
}}
#badgeTop {{
    font-size: 9px;
    letter-spacing: 3px;
    color: {TEXT_DIM};
}}
#badgeBot {{
    font-size: 16px;
    font-weight: bold;
    color: {GOLD};
}}
#divLabel {{
    font-size: 10px;
    letter-spacing: 3px;
    color: {BORDER_LT};
}}
"""

# ── Weapon definitions ────────────────────────────────────────────────────────
WEAPON_COLOR = {
    "SwordWeapon":  ("#e8a020", "#3a2810"),
    "SpearWeapon":  ("#50c8e0", "#0e2430"),
    "ShieldWeapon": ("#a060e0", "#1e1038"),
    "BowWeapon":    ("#60c060", "#102010"),
    "FistWeapon":   ("#e07050", "#3a1808"),
    "GunWeapon":    ("#8090d0", "#141830"),
}

WEAPONS = [
    {"key": "SwordWeapon",  "name": "STYGIUS",    "sub": "Sword of Damocles",        "icon": "⚔",
     "aspects": ["Zagreus", "Nemesis", "Poseidon", "Arthur"]},
    {"key": "SpearWeapon",  "name": "VARATHA",     "sub": "Eternal Spear",            "icon": "🔱",
     "aspects": ["Zagreus", "Achilles", "Hades", "Guan Yu"]},
    {"key": "ShieldWeapon", "name": "AEGIS",       "sub": "Shield of Chaos",          "icon": "🛡",
     "aspects": ["Zagreus", "Chaos", "Zeus", "Beowulf"]},
    {"key": "BowWeapon",    "name": "CORONACHT",   "sub": "Heart-Seeking Bow",        "icon": "🏹",
     "aspects": ["Zagreus", "Chiron", "Hera", "Rama"]},
    {"key": "FistWeapon",   "name": "MALPHON",     "sub": "Twin Fists of Malphon",    "icon": "✊",
     "aspects": ["Zagreus", "Talos", "Demeter", "Gilgamesh"]},
    {"key": "GunWeapon",    "name": "EXAGRYPH",    "sub": "Adamant Rail",             "icon": "⚡",
     "aspects": ["Zagreus", "Eris", "Hestia", "Lucifer"]},
]


class PipLevel(QWidget):
    """5 glowing dots indicating aspect level. Click to change."""
    MAX = 5
    valueChanged = pyqtSignal(int)

    def __init__(self, color=GOLD, parent=None):
        super().__init__(parent)
        self._level = 0
        self._color = QColor(color)
        self.setFixedSize(120, 22)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Click para cambiar nivel")

    def value(self):
        return self._level

    def set_value(self, v):
        self._level = max(0, min(self.MAX, int(v)))
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            w = self.width() / self.MAX
            clicked = int(e.x() / w) + 1
            self._level = 0 if clicked == self._level else clicked
            self.valueChanged.emit(self._level)
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = 8
        gap = (self.width() - self.MAX * r * 2) / (self.MAX + 1)
        y = self.height() / 2
        for i in range(self.MAX):
            x = gap + i * (r * 2 + gap) + r
            filled = i < self._level
            if filled:
                # glow
                glow = QColor(self._color)
                glow.setAlpha(60)
                p.setBrush(QBrush(glow))
                p.setPen(Qt.NoPen)
                p.drawEllipse(int(x - r - 3), int(y - r - 3), (r + 3) * 2, (r + 3) * 2)
                p.setBrush(QBrush(self._color))
                p.setPen(QPen(self._color.lighter(130), 1))
            else:
                p.setBrush(QBrush(QColor(BG_INSET)))
                p.setPen(QPen(QColor(BORDER_LT), 1))
            p.drawEllipse(int(x - r), int(y - r), r * 2, r * 2)


# ── Ornamental divider ────────────────────────────────────────────────────────
class OrnaDivider(QWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._text = text
        self.setFixedHeight(20)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        c = QColor(BORDER_LT)
        pen = QPen(c, 1)
        p.setPen(pen)
        w, h = self.width(), self.height()
        mid = h // 2
        if self._text:
            fm = p.fontMetrics()
            tw = fm.horizontalAdvance(self._text) + 20
            lx = (w - tw) // 2
            p.drawLine(20, mid, lx, mid)
            p.drawLine(lx + tw, mid, w - 20, mid)
            p.setPen(QPen(QColor(BORDER_LT)))
            p.drawText(QRect(lx, 0, tw, h), Qt.AlignCenter, self._text)
        else:
            p.drawLine(20, mid, w - 20, mid)
            # diamond
            d = 4
            p.setBrush(QBrush(c))
            p.setPen(Qt.NoPen)
            for xc in (w // 2,):
                pts = [(xc, mid - d), (xc + d, mid), (xc, mid + d), (xc - d, mid)]
                from PyQt5.QtGui import QPolygon
                from PyQt5.QtCore import QPoint
                poly = QPolygon([QPoint(x, y) for x, y in pts])
                p.drawPolygon(poly)


# ── Star-style level widget (for keepsakes) ───────────────────────────────
class StarLevel(QWidget):
    """3 stars indicating keepsake rank. Click to change."""
    MAX = 3
    valueChanged = pyqtSignal(int)

    def __init__(self, color=GOLD, parent=None):
        super().__init__(parent)
        self._level = 0
        self._color = QColor(color)
        self.setFixedSize(80, 22)
        self.setCursor(Qt.PointingHandCursor)

    def set_value(self, room_count):
        # 0-24 = Rank 1, 25-74 = Rank 2, 75+ = Rank 3
        if room_count < 25: self._level = 1
        elif room_count < 75: self._level = 2
        else: self._level = 3
        self.update()

    def value(self):
        # Map back to room counts for the game
        if self._level == 1: return 0
        if self._level == 2: return 25
        return 75

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            w = self.width() / self.MAX
            clicked = int(e.x() / w) + 1
            self._level = clicked
            self.valueChanged.emit(self.value())
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        for i in range(self.MAX):
            filled = i < self._level
            x = i * 24 + 12
            y = 11
            
            p.setPen(QPen(self._color if filled else QColor(BORDER_LT), 1))
            p.setBrush(QBrush(self._color if filled else Qt.NoBrush))
            
            # Simple star polygon
            pts = []
            for j in range(5):
                import math
                angle = math.radians(j * 144 - 90)
                pts.append((x + 8 * math.cos(angle), y + 8 * math.sin(angle)))
            
            from PyQt5.QtGui import QPolygon
            from PyQt5.QtCore import QPoint
            poly = QPolygon([QPoint(int(px), int(py)) for px, py in pts])
            p.drawPolygon(poly)


# ── Resource card ─────────────────────────────────────────────────────────────
class ResourceCard(QWidget):
    def __init__(self, icon, label, color=GOLD, parent=None):
        super().__init__(parent)
        self._color = color
        self.setObjectName("resourceCard")
        self.setStyleSheet(f"""
            #resourceCard {{
                background: {BG_CARD};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 10, 14, 12)
        lay.setSpacing(6)

        top = QHBoxLayout()
        top.setSpacing(6)
        ico = QLabel(icon)
        ico.setStyleSheet(f"font-size: 22px; background: transparent;")
        top.addWidget(ico)
        lbl = QLabel(label.upper())
        lbl.setStyleSheet(f"background: transparent; font-size: 9px; letter-spacing: 3px; color: {TEXT_DIM};")
        top.addWidget(lbl)
        top.addStretch()
        lay.addLayout(top)

        self.edit = QLineEdit()
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setStyleSheet(f"""
            QLineEdit {{
                background: {BG_INSET};
                border: 1px solid {BORDER};
                border-radius: 6px;
                color: {color};
                padding: 6px 10px;
                font-size: 20px;
                font-weight: bold;
                selection-background-color: {ORANGE};
            }}
            QLineEdit:focus {{ border: 1px solid {color}; }}
        """)
        lay.addWidget(self.edit)

    def value(self):
        try:
            return float(self.edit.text())
        except ValueError:
            return 0.0

    def set_value(self, v):
        self.edit.setText(str(int(v)) if v == int(v) else str(round(v, 2)))


# ── Aspect row with pips ──────────────────────────────────────────────────────
class AspectRow(QWidget):
    def __init__(self, index: int, name: str, color=GOLD, is_base=False, parent=None):
        super().__init__(parent)
        self.index = index
        self._is_base = is_base
        lay = QHBoxLayout(self)
        lay.setContentsMargins(6, 4, 6, 4)
        lay.setSpacing(14)

        # Lock icon
        self.lock = QLabel("🔒" if not is_base else "✦")
        self.lock.setStyleSheet(f"font-size: 13px; background: transparent; min-width: 20px;")
        lay.addWidget(self.lock)

        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"""
            background: transparent;
            font-size: 13px;
            {"color: " + color + "; font-weight: bold;" if is_base else "color: " + TEXT + ";"}
            min-width: 100px;
        """)
        lay.addWidget(name_lbl)

        self.pips = PipLevel(color)
        if is_base:
            self.pips.set_value(1)
        lay.addWidget(self.pips)

        self.spin = QSpinBox()
        self.spin.setRange(0, 5)
        self.spin.setFixedWidth(58)
        if is_base:
            self.spin.setEnabled(False)
            self.spin.setValue(1)
        lay.addWidget(self.spin)

        # Keep pips and spin in sync
        self.spin.valueChanged.connect(self._spin_changed)
        self.pips.valueChanged.connect(self.spin.setValue)

        if is_base:
            # grey out slightly
            pass

    def _spin_changed(self, v):
        self.pips.set_value(v)
        # update lock icon
        self.lock.setText("✦" if v > 0 else "🔒")

    def set_value(self, v):
        self.spin.setValue(int(v))
        self.pips.set_value(int(v))
        self.lock.setText("✦" if v > 0 or self._is_base else "🔒")

    def value(self):
        return self.spin.value()


# ── Weapon card ───────────────────────────────────────────────────────────────
class WeaponCard(QFrame):
    def __init__(self, info: dict, parent=None):
        super().__init__(parent)
        self.weapon_key = info["key"]
        color, bg = WEAPON_COLOR[info["key"]]

        # QFrame supports border/background in QSS properly
        self.setObjectName("weaponCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame#weaponCard {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {BG_CARD}, stop:1 {bg});
                border: 1px solid {BORDER};
                border-radius: 10px;
            }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ──
        header = QWidget()
        header.setStyleSheet(f"""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {bg}, stop:1 transparent);
            border-bottom: 1px solid {BORDER};
            border-radius: 0px;
        """)
        header.setFixedHeight(56)
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(16, 0, 16, 0)

        ico = QLabel(info["icon"])
        ico.setStyleSheet(f"font-size: 26px; background: transparent; color: {color};")
        hlay.addWidget(ico)
        hlay.addSpacing(8)

        v = QVBoxLayout()
        v.setSpacing(1)
        t = QLabel(info["name"])
        t.setStyleSheet(f"font-size: 15px; font-weight: 900; color: {color}; "
                        f"letter-spacing: 3px; background: transparent;")
        s = QLabel(info["sub"].upper())
        s.setStyleSheet(f"font-size: 9px; color: {TEXT_DIM}; letter-spacing: 2px; background: transparent;")
        v.addWidget(t)
        v.addWidget(s)
        hlay.addLayout(v)
        hlay.addStretch()

        self.unlock_check = QCheckBox("DESBLOQUEADA")
        self.unlock_check.setStyleSheet(f"""
            QCheckBox {{ color: {color}; font-size: 11px; letter-spacing: 2px;
                         font-weight: bold; background: transparent; }}
            QCheckBox::indicator {{ border-color: {color}; }}
            QCheckBox::indicator:checked {{ background: {color}; border-color: {color}; }}
        """)
        hlay.addWidget(self.unlock_check)
        hlay.addSpacing(10)

        btn_max = QPushButton("▲ MAX")
        btn_max.setFixedSize(70, 28)
        btn_max.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                border: 1px solid {color};
                border-radius: 5px;
                color: {color};
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {color};
                color: {BG_DARK};
            }}
        """)
        btn_max.clicked.connect(self._max_all)
        hlay.addWidget(btn_max)
        # child widgets must be transparent so QFrame background shows through
        header.setAutoFillBackground(False)
        root.addWidget(header)

        # ── Aspects ──
        body = QWidget()
        body.setStyleSheet("background: transparent;")
        blay = QVBoxLayout(body)
        blay.setContentsMargins(14, 8, 14, 12)
        blay.setSpacing(2)

        tag = QLabel("ASPECTOS")
        tag.setStyleSheet(f"font-size: 9px; color: {TEXT_DIM}; letter-spacing: 3px; "
                          f"background: transparent; padding: 4px 0;")
        blay.addWidget(tag)

        self.aspect_rows = []
        for i, name in enumerate(info["aspects"]):
            row = AspectRow(i + 1, name, color=color, is_base=(i == 0))
            self.aspect_rows.append(row)
            blay.addWidget(row)
            if i < len(info["aspects"]) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setStyleSheet(f"color: {BORDER}; background: {BORDER}; max-height: 1px;")
                blay.addWidget(sep)

        root.addWidget(body)

    def _max_all(self):
        self.unlock_check.setChecked(True)
        for row in self.aspect_rows:
            row.set_value(5)

    def load(self, weapons_unlocked, weapon_unlocks):
        self.unlock_check.setChecked(bool(weapons_unlocked.get(self.weapon_key, False)))
        unlocks = weapon_unlocks.get(self.weapon_key, {})
        for row in self.aspect_rows:
            lvl = int(unlocks.get(float(row.index), 1 if row._is_base else 0))
            row.set_value(lvl)

    def save(self, weapons_unlocked, weapon_unlocks):
        weapons_unlocked[self.weapon_key] = self.unlock_check.isChecked()
        # Preserve any existing entries we don't know about, then overwrite ours
        existing = weapon_unlocks.get(self.weapon_key, {})
        unlocks = dict(existing)  # copy originals
        for row in self.aspect_rows:
            lvl = row.value()
            # Always store the value (even 0 removes it to keep save clean)
            if lvl > 0:
                unlocks[float(row.index)] = float(lvl)
            else:
                unlocks.pop(float(row.index), None)
        weapon_unlocks[self.weapon_key] = unlocks
        # Also mark weapon as touched/unlocked in WeaponsTouched if unlocking


# ── Badge widget ──────────────────────────────────────────────────────────────
class Badge(QWidget):
    def __init__(self, tag, value="—", parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 58)
        self.setStyleSheet(f"""
            Badge {{
                background: rgba(10,8,18,0.8);
                border: 1px solid {BORDER};
                border-top: 2px solid {GOLD_DIM};
                border-radius: 8px;
            }}
        """)
        v = QVBoxLayout(self)
        v.setContentsMargins(10, 6, 10, 6)
        v.setSpacing(2)
        self._top = QLabel(tag.upper())
        self._top.setStyleSheet(f"font-size: 8px; letter-spacing: 3px; color: {TEXT_DIM}; "
                                f"background: transparent;")
        self._top.setAlignment(Qt.AlignCenter)
        self._bot = QLabel(value)
        self._bot.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {GOLD}; "
                                f"background: transparent;")
        self._bot.setAlignment(Qt.AlignCenter)
        v.addWidget(self._top)
        v.addWidget(self._bot)

    def set_value(self, v):
        self._bot.setText(str(v))


# ── Main window ───────────────────────────────────────────────────────────────
class HadesEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.save_file: HadesSaveFile = None
        self.file_path: str = None

        self.setWindowTitle("PLUTO  ·  HadesEditor")
        self.setMinimumSize(960, 700)
        self.resize(1100, 780)
        self.setStyleSheet(QSS)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_title())
        root.addWidget(self._build_action_bar())
        root.addWidget(self._build_path_bar())

        self.tabs = QTabWidget()
        self.tabs.setEnabled(False)
        root.addWidget(self.tabs)

        self.tabs.addTab(self._tab_resources(),   "⚗   RECURSOS")
        self.tabs.addTab(self._tab_weapons(),     "⚔   ARMAS  &  ASPECTOS")
        self.tabs.addTab(self._tab_companions(),  "🐾   COMPAÑEROS  &  PROGRESIÓN")
        self.tabs.addTab(self._tab_items(),       "🙏   MIRROR  &  KEEPSAKES")
        self.tabs.addTab(self._tab_progress(),   "🏛   PROGRESO")

    # ── Sections ──────────────────────────────────────────────────────────────
    def _build_title(self):
        w = QWidget()
        w.setObjectName("titleBar")
        w.setFixedHeight(88)
        h = QHBoxLayout(w)
        h.setContentsMargins(28, 0, 28, 0)

        # left text
        v = QVBoxLayout()
        v.setSpacing(2)
        v.addStretch()
        title = QLabel("✦  HADESEDITOR  ✦")
        title.setObjectName("appTitle")
        sub = QLabel("H A D E S   S A V E   E D I T O R")
        sub.setObjectName("appSubtitle")
        v.addWidget(title)
        v.addWidget(sub)
        v.addStretch()
        h.addLayout(v)
        h.addStretch()

        self._badge_ver = Badge("VERSION")
        self._badge_run = Badge("RUNS")
        self._badge_loc = Badge("LOCATION")
        for b in (self._badge_ver, self._badge_run, self._badge_loc):
            h.addWidget(b)
            h.addSpacing(10)
        return w

    def _build_action_bar(self):
        w = QWidget()
        w.setObjectName("actionBar")
        w.setFixedHeight(54)
        h = QHBoxLayout(w)
        h.setContentsMargins(18, 8, 18, 8)
        h.setSpacing(10)

        self.btn_load = QPushButton("📂   Cargar Save")
        self.btn_load.setObjectName("btnPrimary")
        self.btn_load.clicked.connect(self._load)

        self.btn_save = QPushButton("💾   Guardar")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save)

        self.btn_max = QPushButton("✨   Maximizar Todo")
        self.btn_max.setObjectName("btnMax")
        self.btn_max.setEnabled(False)
        self.btn_max.clicked.connect(self._max_all)

        btn_exit = QPushButton("✕   Salir")
        btn_exit.setObjectName("btnDanger")
        btn_exit.clicked.connect(self.close)

        for b in (self.btn_load, self.btn_save, self.btn_max):
            h.addWidget(b)
        h.addStretch()
        h.addWidget(btn_exit)
        return w

    def _build_path_bar(self):
        w = QWidget()
        w.setObjectName("pathBar")
        w.setFixedHeight(26)
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0)
        h.setSpacing(8)
        k = QLabel("ARCHIVO")
        k.setObjectName("pathKey")
        self._path_lbl = QLabel("—  Ningún archivo cargado")
        self._path_lbl.setObjectName("pathValue")
        h.addWidget(k)
        h.addWidget(self._path_lbl)
        h.addStretch()
        return w

    # ── Tabs ──────────────────────────────────────────────────────────────────
    def _scroll_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"background: {BG_DARK};")
        inner = QWidget()
        inner.setStyleSheet(f"background: {BG_DARK};")
        scroll.setWidget(inner)
        return scroll, inner

    def _tab_resources(self):
        scroll, inner = self._scroll_tab()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 20, 24, 24)
        lay.setSpacing(20)

        grp = self._group("MONEDAS Y RECURSOS")
        grid = QGridLayout(grp)
        grid.setSpacing(14)

        resources = [
            ("🌑", "Darkness",     "darkness",     GOLD),
            ("💎", "Gems",         "gems",         "#60c0e0"),
            ("💠", "Diamonds",     "diamonds",     "#a080f0"),
            ("🍯", "Nectar",       "nectar",       "#e08020"),
            ("🍇", "Ambrosia",     "ambrosia",     "#c050a0"),
            ("🗝", "Chthonic Keys","chthonic_key", "#80a0c0"),
            ("🩸", "Titan Blood",  "titan_blood",  "#c03020"),
        ]
        self._res = {}
        for i, (icon, label, key, color) in enumerate(resources):
            card = ResourceCard(icon, label, color)
            self._res[key] = card
            grid.addWidget(card, i // 4, i % 4)

        lay.addWidget(grp)

        grp2 = self._group("MODOS DE JUEGO")
        h2 = QHBoxLayout(grp2)
        h2.setSpacing(32)
        self.chk_god  = self._fancy_check("⚡  GOD MODE",   GOLD)
        self.chk_hell = self._fancy_check("🔥  HELL MODE",  RED)
        h2.addWidget(self.chk_god)
        h2.addWidget(self.chk_hell)
        h2.addStretch()
        lay.addWidget(grp2)
        lay.addStretch()
        return scroll

    def _tab_weapons(self):
        scroll, inner = self._scroll_tab()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 16, 24, 24)
        lay.setSpacing(4)

        hint = QLabel(
            "✦  Haz click en los  pips  para cambiar el nivel directamente  "
            "•  Nivel 0 = bloqueado  •  Máximo nivel 5"
        )
        hint.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; letter-spacing: 1px; "
                           f"padding: 8px 0 14px 0; background: transparent;")
        lay.addWidget(hint)

        self._weapon_cards = []
        for i, info in enumerate(WEAPONS):
            card = WeaponCard(info)
            self._weapon_cards.append(card)
            lay.addWidget(card)
            if i < len(WEAPONS) - 1:
                lay.addWidget(OrnaDivider())

        lay.addStretch()
        return scroll

    def _tab_progress(self):
        scroll, inner = self._scroll_tab()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 20, 24, 24)
        lay.setSpacing(20)

        grp = self._group("ESTADÍSTICAS DE RUN")
        grid = QGridLayout(grp)
        grid.setSpacing(14)
        meta_res = [
            ("🏃", "Runs totales",        "runs",                "#80c080"),
            ("🌑", "Darkness (header)",   "active_meta_points",  GOLD),
            ("🏛", "Puntos de Santuario", "active_shrine_points","#a0b0f0"),
        ]
        self._meta = {}
        for i, (icon, label, key, color) in enumerate(meta_res):
            card = ResourceCard(icon, label, color)
            self._meta[key] = card
            grid.addWidget(card, 0, i)
        lay.addWidget(grp)

        grp2 = self._group("FLAGS DE JUEGO")
        h2 = QHBoxLayout(grp2)
        h2.setSpacing(28)
        self.chk_aspects = self._fancy_check("🗡  ASPECTOS DESBLOQUEADOS", "#c0a0f0")
        self.chk_gun     = self._fancy_check("⚡  RAIL DESBLOQUEADO (GUN)", "#8090d0")
        h2.addWidget(self.chk_aspects)
        h2.addWidget(self.chk_gun)
        h2.addStretch()
        lay.addWidget(grp2)
        lay.addStretch()
        return scroll

    def _tab_companions(self):
        scroll, inner = self._scroll_tab()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 20, 24, 24)
        lay.setSpacing(20)

        # ── NPCs / Companions ──
        NPCS = [
            ("NPC_Cerberus_01",        "🐺", "Cerberus",         "#e8a020"),
            ("NPC_Achilles_01",        "⚔", "Achilles",         "#e06040"),
            ("NPC_Nyx_01",             "🌙", "Nyx",              "#a060e0"),
            ("NPC_Hades_01",           "💀", "Hades",            "#c03020"),
            ("NPC_FurySister_01",      "😤", "Megaera",          "#d04060"),
            ("NPC_Thanatos_01",        "⚖", "Thanatos",         "#80b0e0"),
            ("NPC_Dusa_01",            "🐍", "Dusa",             "#60c080"),
            ("NPC_Orpheus_01",         "🎵", "Orfeo",            "#c090f0"),
            ("NPC_Eurydice_01",        "🌿", "Eurídice",         "#80e080"),
            ("NPC_Hypnos_01",          "💤", "Hypnos",           "#7090a0"),
            ("NPC_Sisyphus_01",        "🪨", "Sísifo",           "#a0b080"),
            ("NPC_Skelly_01",          "💀", "Skelly",           "#d0c0a0"),
            ("NPC_Patroclus_01",       "🛡", "Patroclo",         "#a0c0e0"),
            ("NPC_Charon_01",          "⛵", "Caronte",          "#c0a040"),
        ]
        grp_npc = self._group("RELACIONES DE PERSONAJES  (Nivel de afinidad: 0–max)")
        g_lay = QGridLayout(grp_npc)
        g_lay.setSpacing(10)
        self._npc_spin = {}
        for i, (key, icon, label, color) in enumerate(NPCS):
            cell = QWidget()
            cell.setStyleSheet(f"""
                QWidget {{
                    background: {BG_CARD};
                    border: 1px solid {BORDER};
                    border-radius: 7px;
                }}
            """)
            c_lay = QHBoxLayout(cell)
            c_lay.setContentsMargins(10, 6, 10, 6)
            c_lay.setSpacing(8)
            ico = QLabel(icon)
            ico.setStyleSheet(f"font-size: 20px; background: transparent; color: {color};")
            c_lay.addWidget(ico)
            lbl = QLabel(label)
            lbl.setStyleSheet(f"background: transparent; font-size: 12px; min-width: 80px; color: {TEXT};")
            c_lay.addWidget(lbl)
            c_lay.addStretch()
            spin = QSpinBox()
            spin.setRange(0, 99)
            spin.setFixedWidth(68)
            spin.setStyleSheet(f"""
                QSpinBox {{ background: {BG_INSET}; border: 1px solid {BORDER};
                            border-radius: 5px; color: {color}; font-weight: bold;
                            font-size: 14px; padding: 3px 6px; }}
                QSpinBox:focus {{ border: 1px solid {color}; }}
            """)
            c_lay.addWidget(spin)
            self._npc_spin[key] = spin
            g_lay.addWidget(cell, i // 2, i % 2)
        lay.addWidget(grp_npc)

        # ── Important Flags ──
        FLAGS = [
            ("AspectsUnlocked",   "🗡",  "Aspectos desbloqueados",  "#c0a0f0"),
            ("GunUnlocked",       "⚡",  "Rail (Exagryph) desbloqueado", "#8090d0"),
            ("FistUnlocked",      "✊",  "Puños (Malphon) desbloqueados", "#e08060"),
            ("SkellyUnlocked",    "💀",  "Skelly desbloqueado",     "#d0c090"),
            ("MetEurydice",       "🌿",  "Conociste a Eurídice",    "#70d070"),
            ("MetHades",          "👑",  "Conociste a Hades",       "#e05050"),
            ("AllowFlashback",    "💭",  "Flashbacks habilitados",  "#8090b0"),
            ("SwapMetaupgradesEnabled", "🔄", "Intercambio de Mirror On", "#60b0c0"),
        ]
        grp_flags = self._group("FLAGS DE DESBLOQUEO")
        fl_grid = QGridLayout(grp_flags)
        fl_grid.setSpacing(10)
        self._flag_checks = {}
        for i, (key, icon, label, color) in enumerate(FLAGS):
            chk = self._fancy_check(f"{icon}  {label}", color)
            self._flag_checks[key] = chk
            fl_grid.addWidget(chk, i // 2, i % 2)
        lay.addWidget(grp_flags)

        # ── Quest status ──
        QUESTS = [
            ("WeaponAspects",       "🗡",  "Aspectos de armas"),
            ("WeaponUnlocks",       "🔓",  "Desbloqueo de armas"),
            ("FirstClear",          "🏆",  "Primera victoria"),
            ("MeetOlympians",       "⚡",  "Conocer Olímpicos"),
            ("MeetChthonicGods",    "🌑",  "Conocer dioses ctónicos"),
            ("AresUpgrades",        "⚔",  "Mejoras de Ares"),
            ("AthenaUpgrades",      "🛡",  "Mejoras de Atenea"),
            ("AphroditeUpgrades",   "💕",  "Mejoras de Afrodita"),
            ("DionysusUpgrades",    "🍇",  "Mejoras de Dioniso"),
            ("DemeterUpgrades",     "❄",  "Mejoras de Deméter"),
            ("ArtemisUpgrades",     "🏹",  "Mejoras de Artemisa"),
            ("PoseidonUpgrades",    "🌊",  "Mejoras de Poseidón"),
            ("ZeusUpgrades",        "⚡",  "Mejoras de Zeus"),
            ("HermesUpgrades",      "🪶",  "Mejoras de Hermes"),
            ("OrpheusRelease",      "🎵",  "Liberación de Orfeo"),
            ("LegendaryUpgrades",   "✨",  "Mejoras legendarias"),
            ("CosmeticsSmall",      "🎨",  "Cosméticos básicos"),
            ("CodexSmall",          "📖",  "Códex básico"),
            ("MiniBossKills",       "💀",  "Matar mini-jefes"),
            ("KeepsakesQuest",      "🎁",  "Misión de recuerdos"),
        ]
        grp_q = self._group("MISIONES  (marca = completada / cobrada)")
        q_grid = QGridLayout(grp_q)
        q_grid.setSpacing(8)
        self._quest_checks = {}
        for i, (key, icon, label) in enumerate(QUESTS):
            chk = QCheckBox(f"{icon}  {label}")
            chk.setStyleSheet(f"""
                QCheckBox {{ color: {TEXT}; font-size: 12px; background: transparent; }}
                QCheckBox::indicator {{ width: 18px; height: 18px;
                    border: 2px solid {BORDER_LT}; border-radius: 4px;
                    background: {BG_INSET}; }}
                QCheckBox::indicator:checked {{ background: {GOLD_DIM};
                    border-color: {GOLD}; }}
            """)
            self._quest_checks[key] = chk
            q_grid.addWidget(chk, i // 3, i % 3)
        lay.addWidget(grp_q)
        lay.addStretch()
        return scroll

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _group(self, title):
        g = QGroupBox(title)
        return g

    def _fancy_check(self, text, color):
        c = QCheckBox(text)
        c.setStyleSheet(f"""
            QCheckBox {{
                font-size: 13px; font-weight: bold;
                letter-spacing: 1px; color: {color};
                background: transparent;
            }}
            QCheckBox::indicator {{
                width: 22px; height: 22px;
                border: 2px solid {color};
                border-radius: 6px;
                background: {BG_INSET};
            }}
            QCheckBox::indicator:checked {{
                background: {color};
                border-color: {color};
            }}
        """)
        return c

    def _hades_dir(self):
        d = os.path.expanduser("~/Library/Application Support/Supergiant Games/Hades")
        return d if os.path.isdir(d) else ""

    # ── Items tab (Mirror + Keepsakes) ────────────────────────────────────────
    def _tab_items(self):
        scroll, inner = self._scroll_tab()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 20, 24, 24)
        lay.setSpacing(20)

        # Mirror upgrades
        MIRROR = [
            ("HealthMetaUpgrade",             "❤",  "Death Defiance (vidas extra)",       10, "#c03030"),
            ("AmmoMetaUpgrade",               "🔵",  "Death Defiance extra carga",          6,  "#4080c0"),
            ("ExtraChanceMetaUpgrade",        "♻",  "Stubborn Defiance (sec. chance)",     1,  "#60a060"),
            ("ExtraChanceReplenishMetaUpgrade","♻", "Stubborn Defiance recarga",           1,  "#50c060"),
            ("StaminaMetaUpgrade",            "💨",  "Greater Reflex (dash extra)",         1,  "#80c0f0"),
            ("RareBoonDropMetaUpgrade",       "⭐",  "Rare Boon (aumento rareza)",          40, "#c0a030"),
            ("EpicBoonDropMetaUpgrade",       "💫",  "Epic Boon upgrade",                   40, "#a030c0"),
            ("GodEnhancementMetaUpgrade",     "⚡",  "Privileged Status (3er slot)",        1,  "#a0a0f0"),
            ("DuoRarityBoonDropMetaUpgrade",  "🔗",  "Duo Boon chance (Duplexidad)",        40, "#f09030"),
            ("BackstabMetaUpgrade",           "🗡",  "Knife Trick (daño por espalda)",      5,  "#e06020"),
            ("FirstStrikeMetaUpgrade",        "⚡",  "Fated Authority (primer golpe)",      5,  "#e0c020"),
            ("PerfectDashMetaUpgrade",        "✨",  "Fated Persuasion (dash evasivo)",     5,  "#30c0f0"),
            ("MoneyMetaUpgrade",              "💰",  "Tight Deadline (oro de combate)",     5,  "#c0c040"),
            ("DarknessHealMetaUpgrade",       "🌑",  "Dark Regeneration (vida de Darkness)",5, "#8040a0"),
            ("DoorHealMetaUpgrade",           "🚪",  "Thick Skin (vida al entrar sala)",    5,  "#309050"),
            ("InterestMetaUpgrade",           "👜",  "Chthonic Vitality (interés oro)",     5,  "#c0a040"),
            ("RerollMetaUpgrade",             "🎲",  "Fated Choice (rerolls)",              5,  "#6090d0"),
            ("ReloadAmmoMetaUpgrade",         "🔄",  "Death Defiance recarga",              5,  "#4090c0"),
            ("RunProgressRewardMetaUpgrade",  "🏆",  "Infernal Soul (bonus por avance)",    5,  "#d06030"),
        ]
        grp_mirror = self._group("MIRROR OF NIGHT  —  Mejoras permanentes")
        m_grid = QGridLayout(grp_mirror)
        m_grid.setSpacing(10)
        self._mirror_spin = {}
        for i, (key, icon, label, maxv, color) in enumerate(MIRROR):
            cell = QWidget()
            cell.setStyleSheet(f"""
                QWidget {{
                    background: {BG_CARD};
                    border: 1px solid {BORDER};
                    border-radius: 7px;
                }}
            """)
            c = QHBoxLayout(cell)
            c.setContentsMargins(10, 6, 10, 6)
            c.setSpacing(6)
            ico = QLabel(icon)
            ico.setStyleSheet(f"font-size: 18px; background: transparent; color: {color};")
            c.addWidget(ico)
            lbl = QLabel(label)
            lbl.setWordWrap(False)
            lbl.setStyleSheet(f"background: transparent; font-size: 11px; color: {TEXT}; min-width: 200px;")
            c.addWidget(lbl)
            c.addStretch()
            spin = QSpinBox()
            spin.setRange(0, maxv)
            spin.setFixedWidth(62)
            spin.setStyleSheet(f"""
                QSpinBox {{ background: {BG_INSET}; border: 1px solid {BORDER};
                            border-radius: 5px; color: {color}; font-weight: bold;
                            font-size: 13px; padding: 2px 5px; }}
                QSpinBox:focus {{ border: 1px solid {color}; }}
            """)
            c.addWidget(spin)
            lim = QLabel(f" / {maxv}")
            lim.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; background: transparent;")
            c.addWidget(lim)
            self._mirror_spin[key] = spin
            m_grid.addWidget(cell, i // 2, i % 2)
        lay.addWidget(grp_mirror)

        # Mapping Trait -> Gift NPC Key for unlocking
        KS_NPC = {
            "MaxHealthKeepsakeTrait": "NPC_Cerberus_01",
            "ForceArtemisBoonTrait": "ArtemisUpgrade",
            "ForceAphroditeBoonTrait": "AphroditeUpgrade",
            "ForceAresBoonTrait": "AresUpgrade",
            "ForceAthenaBoonTrait": "AthenaUpgrade",
            "ForceDionysusBoonTrait": "DionysusUpgrade",
            "ForceZeusBoonTrait": "ZeusUpgrade",
            "ForceHermesBoonTrait": "HermesUpgrade",
            "ForcePoseidonBoonTrait": "PoseidonUpgrade",
            "ForceDemeterBoonTrait": "DemeterUpgrade",
            "PerfectClearDamageBonusTrait": "NPC_Dusa_01",
            "BonusMoneyTrait": "NPC_Charon_01",
            "ReincarnationTrait": "NPC_Sisyphus_01",
            "MoveSpeedKeepsakeTrait": "NPC_Thanatos_01",
            "RapidBoonsKeepsakeTrait": "NPC_Orpheus_01",
            "TemporaryInvulnerabilityTrait": "NPC_Eurydice_01",
            "HealingItemKeepsakeTrait": "NPC_Skelly_01", # Skelly gives Lucky Tooth
            "ForceBlessedTrait": "NPC_Skelly_01",
            "RoomMoneyBonusTrait": "NPC_Patroclus_01",
            "ForceAchillesBoonTrait": "NPC_Achilles_01",
            "GodModeFasterLockPickTrait": "ChaosUpgrade", # Chaos doesn't have an upgrade key? Usually it's Gift[NPC_Chaos_01]
        }

        # Keepsakes — all Hades keepsakes by their KeepsakeChambers trait name
        KEEPSAKES = [
            ("MaxHealthKeepsakeTrait",         "🐶", "Old Spiked Collar",          "Cerberus",  "#e8a020", "NPC_Cerberus_01"),
            ("ForceArtemisBoonTrait",           "🏹", "Adamant Arrowhead",          "Artemisa",  "#60d060", "ArtemisUpgrade"),
            ("ForceAphroditeBoonTrait",         "🌹", "Eternal Rose",              "Afrodita",  "#f060a0", "AphroditeUpgrade"),
            ("ForceAresBoonTrait",              "⚔",  "Blood-Filled Vial",         "Ares",      "#c03020", "AresUpgrade"),
            ("ForceAthenaBoonTrait",            "🛡",  "Owl Pendant",               "Atenea",    "#60a0e0", "AthenaUpgrade"),
            ("ForceDionysusBoonTrait",          "🍇", "Overflowing Cup",           "Dioniso",   "#c050c0", "DionysusUpgrade"),
            ("ForceZeusBoonTrait",              "⚡",  "Thunder Signet",            "Zeus",      "#d0c020", "ZeusUpgrade"),
            ("ForceHermesBoonTrait",            "🪶", "Lambent Plume",             "Hermes",    "#d0d090", "HermesUpgrade"),
            ("ForcePoseidonBoonTrait",          "🌊", "Conch Shell",               "Poseidón",  "#3090d0", "PoseidonUpgrade"),
            ("ForceDemeterBoonTrait",           "❄",  "Pom Blossom",               "Deméter",   "#80b0d0", "DemeterUpgrade"),
            ("PerfectClearDamageBonusTrait",   "🐍", "Harpy Feather Duster",      "Dusa",      "#60c080", "NPC_Dusa_01"),
            ("BonusMoneyTrait",                "💰", "Charon's Obol",             "Caronte",   "#c0a040", "NPC_Charon_01"),
            ("ReincarnationTrait",             "💀", "Shattered Shackle",         "Sísifo",    "#909090", "NPC_Sisyphus_01"),
            ("MoveSpeedKeepsakeTrait",         "💨", "Pierced Butterfly",         "Thanatos",  "#80b0e0", "NPC_Thanatos_01"),
            ("RapidBoonsKeepsakeTrait",        "🎵", "Lyre of Orpheus",           "Orfeo",     "#c090f0", "NPC_Orpheus_01"),
            ("TemporaryInvulnerabilityTrait",  "🌿", "Evergreen Acorn",           "Eurídice",  "#80e080", "NPC_Eurydice_01"),
            ("HealingItemKeepsakeTrait",       "🍷", "Nectar / Bracer",           "Sísifo/Ach"," #a0b080", "NPC_Sisyphus_01"),
            ("ForceBlessedTrait",              "🦴", "Lucky Tooth",               "Skelly",    "#d0c090", "NPC_Skelly_01"),
            ("RoomMoneyBonusTrait",            "🛡",  "Black Shawl",               "Patroclo",  "#a0c0e0", "NPC_Patroclus_01"),
            ("ForceAchillesBoonTrait",         "⚔",  "Broken Spearpoint",         "Achilles",  "#e06040", "NPC_Achilles_01"),
        ]
        grp_ks = self._group("KEEPSAKES  —  Usos acumulados en salas (más = mayor nivel del recuerdo)")
        ks_grid = QGridLayout(grp_ks)
        ks_grid.setSpacing(8)
        self._ks_spin = {}
        self._ks_unlock = {}
        for i, (key, icon, label, source, color, npc_key) in enumerate(KEEPSAKES):
            cell = QWidget()
            cell.setStyleSheet(f"""
                QWidget {{
                    background: {BG_CARD};
                    border: 1px solid {BORDER};
                    border-radius: 7px;
                }}
            """)
            c = QHBoxLayout(cell)
            c.setContentsMargins(8, 4, 8, 4)
            c.setSpacing(6)
            
            chk = QCheckBox()
            chk.setToolTip("Desbloqueado")
            chk.setStyleSheet(f"QCheckBox::indicator {{ width: 16px; height: 16px; border: 1px solid {color}; border-radius: 3px; }} QCheckBox::indicator:checked {{ background: {color}; }}")
            c.addWidget(chk)
            self._ks_unlock[key] = (chk, npc_key)

            ico = QLabel(icon)
            ico.setStyleSheet(f"font-size: 16px; background: transparent; color: {color};")
            c.addWidget(ico)
            info_v = QVBoxLayout()
            info_v.setSpacing(0)
            lbl = QLabel(label)
            lbl.setStyleSheet(f"background: transparent; font-size: 12px; color: {TEXT}; font-weight: bold;")
            src = QLabel(source)
            src.setStyleSheet(f"background: transparent; font-size: 9px; color: {color}; letter-spacing: 1px;")
            info_v.addWidget(lbl)
            info_v.addWidget(src)
            c.addLayout(info_v)
            c.addStretch()
            
            self.stars = StarLevel(color)
            c.addWidget(self.stars)
            
            spin = QSpinBox()
            spin.setRange(0, 9999)
            spin.setFixedWidth(65)
            spin.setStyleSheet(f"""
                QSpinBox {{ background: {BG_INSET}; border: 1px solid {BORDER};
                            border-radius: 5px; color: {color}; font-weight: bold;
                            font-size: 12px; padding: 2px 4px; }}
                QSpinBox:focus {{ border: 1px solid {color}; }}
            """)
            c.addWidget(spin)
            
            # Sync stars and spin
            spin.valueChanged.connect(self.stars.set_value)
            self.stars.valueChanged.connect(spin.setValue)
            
            self._ks_spin[key] = spin
            ks_grid.addWidget(cell, i // 2, i % 2)
        lay.addWidget(grp_ks)
        lay.addStretch()
        return scroll

    # ── Logic ─────────────────────────────────────────────────────────────────
    def _load(self):
        opts = QFileDialog.Options()
        opts |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "Cargar Save de Hades", self._hades_dir(),
            "Hades Save Files (*.sav);;All Files (*)", options=opts
        )
        if not path:
            return
        try:
            self.save_file = HadesSaveFile.from_file(path)
            self.file_path = path
            self._populate()
            self.tabs.setEnabled(True)
            self.btn_save.setEnabled(True)
            self.btn_max.setEnabled(True)
            self._path_lbl.setText(path)
        except Exception as e:
            QMessageBox.critical(self, "Error al cargar", str(e))

    def _populate(self):
        sf = self.save_file
        gs = sf.lua_state._active_state.get("GameState", {})

        self._badge_ver.set_value(sf.version)
        self._badge_run.set_value(sf.runs)
        self._badge_loc.set_value(sf.location.replace("Location_", ""))

        for key, val in {
            "darkness":      sf.lua_state.darkness,
            "gems":          sf.lua_state.gems,
            "diamonds":      sf.lua_state.diamonds,
            "nectar":        sf.lua_state.nectar,
            "ambrosia":      sf.lua_state.ambrosia,
            "chthonic_key":  sf.lua_state.chthonic_key,
            "titan_blood":   sf.lua_state.titan_blood,
        }.items():
            self._res[key].set_value(val or 0)

        self.chk_god.setChecked(bool(sf.god_mode_enabled))
        self.chk_hell.setChecked(bool(sf.hell_mode_enabled))

        wu  = gs.get("WeaponsUnlocked", {})
        wul = gs.get("WeaponUnlocks", {})
        for card in self._weapon_cards:
            card.load(wu, wul)

        self._meta["runs"].set_value(sf.runs)
        self._meta["active_meta_points"].set_value(sf.active_meta_points)
        self._meta["active_shrine_points"].set_value(sf.active_shrine_points)

        flags = gs.get("Flags", {})
        self.chk_aspects.setChecked(bool(flags.get("AspectsUnlocked", False)))
        self.chk_gun.setChecked(bool(flags.get("GunUnlocked", False)))

        # Companions tab
        gift = gs.get("Gift", {})
        for key, spin in self._npc_spin.items():
            val = gift.get(key, {}).get("Value", 0) if isinstance(gift.get(key), dict) else 0
            spin.setValue(int(val))

        for key, chk in self._flag_checks.items():
            chk.setChecked(bool(flags.get(key, False)))

        quest = gs.get("QuestStatus", {})
        for key, chk in self._quest_checks.items():
            status = quest.get(key, "")
            chk.setChecked(status in ("CashedOut", "Completed"))

        # Items tab
        meta_ups = gs.get("MetaUpgrades", {})
        for key, spin in self._mirror_spin.items():
            spin.setValue(int(meta_ups.get(key, 0)))

        kc = gs.get("KeepsakeChambers", {})
        for key, spin in self._ks_spin.items():
            spin.setValue(int(kc.get(key, 0)))

        for key, (chk, npc_key) in self._ks_unlock.items():
            val = gift.get(npc_key, {}).get("Value", 0) if isinstance(gift.get(npc_key), dict) else 0
            chk.setChecked(val > 0)

    def _collect(self):
        sf = self.save_file
        gs = sf.lua_state._active_state.setdefault("GameState", {})

        sf.lua_state.darkness     = self._res["darkness"].value()
        sf.lua_state.gems         = self._res["gems"].value()
        sf.lua_state.diamonds     = self._res["diamonds"].value()
        sf.lua_state.nectar       = self._res["nectar"].value()
        sf.lua_state.ambrosia     = self._res["ambrosia"].value()
        sf.lua_state.chthonic_key = self._res["chthonic_key"].value()
        sf.lua_state.titan_blood  = self._res["titan_blood"].value()

        sf.god_mode_enabled  = self.chk_god.isChecked()
        sf.hell_mode_enabled = self.chk_hell.isChecked()

        wu  = gs.setdefault("WeaponsUnlocked", {})
        wul = gs.setdefault("WeaponUnlocks", {})
        for card in self._weapon_cards:
            card.save(wu, wul)

        sf.runs                 = int(self._meta["runs"].value())
        sf.active_meta_points   = int(self._meta["active_meta_points"].value())
        sf.active_shrine_points = int(self._meta["active_shrine_points"].value())

        flags = gs.setdefault("Flags", {})
        flags["AspectsUnlocked"] = self.chk_aspects.isChecked()
        flags["GunUnlocked"]     = self.chk_gun.isChecked()

        # Companions
        gift = gs.setdefault("Gift", {})
        for key, spin in self._npc_spin.items():
            if key not in gift or not isinstance(gift[key], dict):
                gift[key] = {"Value": float(spin.value()), "NewTraits": {}}
            else:
                gift[key]["Value"] = float(spin.value())

        for key, chk in self._flag_checks.items():
            flags[key] = chk.isChecked()

        quest = gs.setdefault("QuestStatus", {})
        for key, chk in self._quest_checks.items():
            if chk.isChecked():
                quest[key] = "CashedOut"
            else:
                quest.pop(key, None)

        # Mirror & Keepsakes
        meta_ups = gs.setdefault("MetaUpgrades", {})
        meta_state = gs.setdefault("MetaUpgradeState", {})
        for key, spin in self._mirror_spin.items():
            val = float(spin.value())
            meta_ups[key]   = val
            meta_state[key] = val

        kc = gs.setdefault("KeepsakeChambers", {})
        for key, spin in self._ks_spin.items():
            kc[key] = float(spin.value())

        for key, (chk, npc_key) in self._ks_unlock.items():
            if chk.isChecked():
                if npc_key not in gift or not isinstance(gift[npc_key], dict):
                    gift[npc_key] = {"Value": 1.0, "NewTraits": {}}
                elif gift[npc_key].get("Value", 0) == 0:
                    gift[npc_key]["Value"] = 1.0
            else:
                if npc_key in gift and isinstance(gift[npc_key], dict):
                    gift[npc_key]["Value"] = 0.0

    def _save(self):
        opts = QFileDialog.Options()
        opts |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Save de Hades",
            self.file_path or self._hades_dir(),
            "Hades Save Files (*.sav);;All Files (*)", options=opts
        )
        if not path:
            return
        try:
            self._collect()
            self.save_file.to_file(path)
            self.file_path = path
            self._path_lbl.setText(path)
            QMessageBox.information(self, "✓ Guardado", f"Archivo guardado en:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", str(e))

    def _max_all(self):
        reply = QMessageBox.question(
            self, "Maximizar Todo",
            "¿Maximizar todos los recursos y desbloquear todas las armas y aspectos?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        for card in self._res.values():
            card.set_value(99999)
        for wc in self._weapon_cards:
            wc._max_all()
        self.chk_aspects.setChecked(True)
        self.chk_gun.setChecked(True)
        # Max NPC affinity
        for spin in self._npc_spin.values():
            spin.setValue(10)
        # Unlock all flags
        for chk in self._flag_checks.values():
            chk.setChecked(True)
        # Complete all quests
        for chk in self._quest_checks.values():
            chk.setChecked(True)
        # Max mirror upgrades
        for key, spin in self._mirror_spin.items():
            spin.setValue(spin.maximum())
        # Max keepsake uses
        for spin in self._ks_spin.values():
            spin.setValue(500)


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = HadesEditor()
    win.show()
    sys.exit(app.exec_())
