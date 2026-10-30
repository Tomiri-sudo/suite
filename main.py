import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, 
    QPushButton, QLineEdit, QVBoxLayout, 
    QDialog, QTabWidget, QLabel, QComboBox, 
    QCheckBox, QHBoxLayout, QDialogButtonBox
)
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt

# --- Localization Data ---
TRANSLATIONS = {
    "English": {
        "title": "Termux Calculator",
        "settings": "Settings",
        "about": "About",
        "theme": "Theme:",
        "dark": "Dark",
        "light": "Light",
        "numerals": "Numerals:",
        "decimal": "Decimal Separator:",
        "language": "Language:",
        "about_text": "<b>Termux Calculator v1.1.0</b><br>A simple and customizable PyQt6 calculator built for Termux on Android.<br><br>Developed with Python and Qt.",
        "close": "Close"
    },
    "Italian": {
        "title": "Calcolatrice Termux",
        "settings": "Impostazioni",
        "about": "Informazioni",
        "theme": "Tema:",
        "dark": "Scuro",
        "light": "Chiaro",
        "numerals": "Numeri:",
        "decimal": "Separatore decimale:",
        "language": "Lingua:",
        "about_text": "<b>Calcolatrice Termux v1.1.0</b><br>Una calcolatrice PyQt6 semplice e personalizzabile creata per Termux su Android.<br><br>Sviluppato con Python e Qt.",
        "close": "Chiudi"
    },
    "French": {
        "title": "Calculatrice Termux",
        "settings": "Paramètres",
        "about": "À propos",
        "theme": "Thème :",
        "dark": "Sombre",
        "light": "Clair",
        "numerals": "Chiffres :",
        "decimal": "Séparateur décimal :",
        "language": "Langue :",
        "about_text": "<b>Calculatrice Termux v1.1.0</b><br>Une calculatrice PyQt6 simple et personnalisable conçue pour Termux sous Android.<br><br>Développé avec Python et Qt.",
        "close": "Fermer"
    },
    "Simplified Chinese": {
        "title": "Termux 计算器",
        "settings": "设置",
        "about": "关于",
        "theme": "主题：",
        "dark": "深色",
        "light": "浅色",
        "numerals": "数字格式：",
        "decimal": "小数分隔符：",
        "language": "语言：",
        "about_text": "<b>Termux 计算器 v1.1.0</b><br>专为 Android 上的 Termux 构建的简单且可定制的 PyQt6 计算器。<br><br>使用 Python 和 Qt 开发。",
        "close": "关闭"
    },
    "Arabic": {
        "title": "آلة حاسبة Termux",
        "settings": "الإعدادات",
        "about": "حول",
        "theme": "المظهر:",
        "dark": "داكن",
        "light": "فاتح",
        "numerals": "الأرقام:",
        "decimal": "فاصل العشرية:",
        "language": "اللغة:",
        "about_text": "<b>آلة حاسبة Termux v1.1.0</b><br>آلة حاسبة PyQt6 بسيطة وقابلة للتخصيص مصممة لـ Termux على أندرويد.<br><br>تم التطوير بواسطة Python و Qt.",
        "close": "إغلاق"
    }
}

EASTERN_ARABIC_MAP = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
WESTERN_ARABIC_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_calc = parent
        self.initUI()

    def initUI(self):
        lang = self.parent_calc.current_language
        t = TRANSLATIONS[lang]
        
        self.setWindowTitle(t["settings"])
        self.setFixedSize(350, 280)

        layout = QVBoxLayout(self)

        # Tabs Setup
        self.tabs = QTabWidget()
        
        # --- Tab 1: Settings ---
        settings_widget = QWidget()
        settings_layout = QGridLayout(settings_widget)

        self.theme_label = QLabel(t["theme"])
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([t["dark"], t["light"]])
        # Set current selection index based on parent state
        self.theme_combo.setCurrentIndex(0 if self.parent_calc.is_dark_theme else 1)

        self.numerals_label = QLabel(t["numerals"])
        self.numerals_combo = QComboBox()
        self.numerals_combo.addItems(["123 (Western)", "١٢٣ (Arabic)"])
        self.numerals_combo.setCurrentIndex(1 if self.parent_calc.use_eastern_numerals else 0)

        self.decimal_label = QLabel(t["decimal"])
        self.decimal_combo = QComboBox()
        self.decimal_combo.addItems([". (Dot)", ", (Comma)"])
        self.decimal_combo.setCurrentIndex(1 if self.parent_calc.decimal_separator == "," else 0)

        self.lang_label = QLabel(t["language"])
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(TRANSLATIONS.keys()))
        self.lang_combo.setCurrentText(lang)

        settings_layout.addWidget(self.theme_label, 0, 0)
        settings_layout.addWidget(self.theme_combo, 0, 1)
        settings_layout.addWidget(self.numerals_label, 1, 0)
        settings_layout.addWidget(self.numerals_combo, 1, 1)
        settings_layout.addWidget(self.decimal_label, 2, 0)
        settings_layout.addWidget(self.decimal_combo, 2, 1)
        settings_layout.addWidget(self.lang_label, 3, 0)
        settings_layout.addWidget(self.lang_combo, 3, 1)

        self.tabs.addTab(settings_widget, t["settings"])

        # --- Tab 2: About ---
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        self.about_label = QLabel(t["about_text"])
        self.about_label.setWordWrap(True)
        about_layout.addWidget(self.about_label)
        self.tabs.addTab(about_widget, t["about"])

        layout.addWidget(self.tabs)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.apply_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def apply_and_accept(self):
        # Extract configurations and pass them back to calculator instance
        is_dark = (self.theme_combo.currentIndex() == 0)
        use_eastern = (self.numerals_combo.currentIndex() == 1)
        dec_sep = "," if self.decimal_combo.currentIndex() == 1 else "."
        new_lang = self.lang_combo.currentText()

        self.parent_calc.update_preferences(is_dark, use_eastern, dec_sep, new_lang)
        self.accept()


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # Default Preferences
        self.current_language = "English"
        self.is_dark_theme = True
        self.use_eastern_numerals = False
        self.decimal_separator = "."
        
        self.initUI()
        self.apply_theme()

    def initUI(self):
        t = TRANSLATIONS[self.current_language]
        self.setWindowTitle(t["title"])
        self.setFixedSize(300, 420)

        v_layout = QVBoxLayout()

        # Display screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("font-size: 26px; padding: 10px; border-radius: 5px;")
        v_layout.addWidget(self.display)

        # Grid layout for buttons
        grid_layout = QGridLayout()

        # Button definitions (Labels stored separate from functional characters)
        self.buttons_map = [
            ('7', '7', 0, 0), ('8', '8', 0, 1), ('9', '9', 0, 2), ('/', '/', 0, 3),
            ('4', '4', 1, 0), ('5', '5', 1, 1), ('6', '6', 1, 2), ('*', '*', 1, 3),
            ('1', '1', 2, 0), ('2', '2', 2, 1), ('3', '3', 2, 2), ('-', '-', 2, 3),
            ('0', '0', 3, 0), ('.', '.', 3, 1), ('C', 'C', 3, 2), ('+', '+', 3, 3),
            ('=', '=', 4, 0, 1, 4)
        ]

        self.btn_objects = []
        for item in self.buttons_map:
            char_val = item[0]
            row = item[2]
            col = item[3]
            
            btn = QPushButton(char_val)
            btn.setStyleSheet("font-size: 18px; padding: 15px;")
            
            if len(item) > 4:
                grid_layout.addWidget(btn, row, col, item[4], item[5])
            else:
                grid_layout.addWidget(btn, row, col)

            btn.clicked.connect(self.on_button_click)
            self.btn_objects.append((btn, char_val))

        v_layout.addLayout(grid_layout)
        self.setLayout(v_layout)

        # Setup Shortcut Ctrl + ,
        self.shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        self.shortcut.activated.connect(self.open_settings)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def update_preferences(self, is_dark, use_eastern, dec_sep, new_lang):
        self.is_dark_theme = is_dark
        self.use_eastern_numerals = use_eastern
        self.decimal_separator = dec_sep
        self.current_language = new_lang
        
        self.apply_theme()
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        t = TRANSLATIONS[self.current_language]
        self.setWindowTitle(t["title"])

        # Update button numeral visuals if digit buttons
        num_map_target = EASTERN_ARABIC_MAP if self.use_eastern_numerals else WESTERN_ARABIC_MAP
        
        for btn, char_val in self.btn_objects:
            if char_val.isdigit():
                # Translate digit label visually
                btn.setText(char_val.translate(num_map_target))
            elif char_val == '.':
                # Update decimal button label to match separator choice
                btn.setText(self.decimal_separator)

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                QWidget { background-color: #1e1e1e; color: #ffffff; }
                QLineEdit { background-color: #2d2d2d; color: #ffffff; border: 1px solid #444; }
                QPushButton { background-color: #333333; color: #ffffff; border: 1px solid #555; border-radius: 4px; }
                QPushButton:pressed { background-color: #555555; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f0f0f0; color: #000000; }
                QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #ccc; }
                QPushButton { background-color: #e0e0e0; color: #000000; border: 1px solid #bbb; border-radius: 4px; }
                QPushButton:pressed { background-color: #cccccc; }
            """)

    def on_button_click(self):
        clicked_button = self.sender()
        text = clicked_button.text()
        current_display = self.display.text()

        # Handle Eastern Arabic to standard mapping conversion back if needed for internal eval
        if self.use_eastern_numerals:
            text = text.translate(WESTERN_ARABIC_MAP)
        if text == self.decimal_separator:
            text = "."

        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                # Replace comma with dot temporarily for python math evaluation if user typed comma
                eval_expr = current_display.translate(WESTERN_ARABIC_MAP).replace(',', '.')
                result = str(eval(eval_expr))
                
                if self.decimal_separator == ',':
                    result = result.replace('.', ',')
                if self.use_eastern_numerals:
                    result = result.translate(EASTERN_ARABIC_MAP)
                    
                self.display.setText(result)
            except Exception:
                self.display.setText("Error" if self.current_language == "English" else "Err")
        else:
            # Append clicked character (handling numeral translation display)
            display_char = text
            if self.use_eastern_numerals and display_char.isdigit():
                display_char = display_char.translate(EASTERN_ARABIC_MAP)
            elif display_char == '.' and self.decimal_separator == ',':
                display_char = ','

            self.display.setText(current_display + display_char)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
