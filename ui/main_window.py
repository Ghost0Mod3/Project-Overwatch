"""Project Overwatch main dashboard with RSS region filters and live search."""

import sys
from datetime import datetime
from email.utils import parsedate_to_datetime

from PySide6.QtCore import QObject, QThread, QTimer, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication, QComboBox, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QVBoxLayout, QWidget,
)

from feeds.rss_fetcher import RSSFetcher
from ui.map_widget import MapWidget


class RSSWorker(QObject):
    articles_ready = Signal(list)
    error = Signal(str)
    finished = Signal()

    @Slot()
    def run(self):
        try:
            self.articles_ready.emit(RSSFetcher().get_articles())
        except Exception as error:
            self.error.emit(str(error))
        finally:
            self.finished.emit()


class MainWindow(QMainWindow):
    REFRESH_INTERVAL_MS = 180_000
    ROTATION_INTERVAL_MS = 10_000
    ROTATING_ARTICLES_PER_PAGE = 8
    MAX_VISIBLE_ARTICLES = 100

    EVENT_CODES = {
        "MISSILE": "MSL", "DRONE": "UAV", "CYBER": "CYB",
        "NAVAL": "NAV", "AIR": "AIR", "GROUND": "GRD",
        "DIPLOMATIC": "DIP", "HOMELAND": "HML", "NEWS": "INT",
    }
    EVENT_WEIGHTS = {
        "MISSILE": 30, "DRONE": 24, "AIR": 22, "GROUND": 20,
        "NAVAL": 18, "CYBER": 16, "HOMELAND": 14,
        "DIPLOMATIC": 4, "NEWS": 0,
    }
    SIGNAL_COLORS = {
        "CRITICAL": "#ff3344", "HIGH": "#ff6b35",
        "ELEVATED": "#ffb000", "GUARDED": "#ffe600",
        "LOW": "#39ff14", "NO SIGNAL": "#597066",
    }
    REGION_ALIASES = {
        "UKRAINE": {"ukraine", "ukrainian", "kyiv", "zelensky", "crimea", "donetsk", "kharkiv"},
        "RUSSIA": {"russia", "russian", "moscow", "kremlin"},
        "NATO": {"nato", "north atlantic treaty organization"},
        "BLACK SEA": {"black sea", "crimea", "sevastopol"},
        "TAIWAN": {"taiwan", "taiwanese", "taipei"},
        "TAIWAN STRAIT": {"taiwan strait"},
        "CHINA": {"china", "chinese", "beijing"},
        "SOUTH CHINA SEA": {"south china sea", "spratly", "paracel", "scarborough shoal"},
        "PHILIPPINES": {"philippines", "philippine", "manila"},
        "MIDDLE EAST": {"middle east", "israel", "gaza", "iran", "iraq", "syria", "lebanon", "yemen"},
        "ISRAEL": {"israel", "israeli", "tel aviv", "jerusalem"},
        "GAZA": {"gaza", "hamas", "palestinian"},
        "IRAN": {"iran", "iranian", "tehran"},
        "YEMEN": {"yemen", "yemeni", "houthi"},
        "RED SEA": {"red sea", "houthi", "bab al-mandab"},
        "UNITED STATES": {"united states", "u.s.", "american", "washington"},
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Overwatch")
        self.resize(1400, 900)
        self.rss_thread = None
        self.rss_worker = None
        self.rss_refresh_in_progress = False
        self.current_articles = []
        self.filtered_articles = []
        self.active_region_filter = "ALL REPORTS"
        self.search_query = ""
        self.article_rotation_index = 0
        self.last_feed_update = None
        self.build_ui()
        self.apply_theme()
        self.configure_refresh_timer()
        self.configure_headline_rotation_timer()
        QTimer.singleShot(100, self.start_rss_refresh)

    def build_ui(self):
        central = QWidget()
        main = QVBoxLayout(central)
        main.setContentsMargins(12, 12, 12, 12)
        main.setSpacing(8)

        header = QLabel("PROJECT OVERWATCH")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(header)

        top = QHBoxLayout()
        events_box = QGroupBox("ACTIVE EVENTS")
        events_layout = QVBoxLayout(events_box)

        controls = QHBoxLayout()
        self.region_filter = QComboBox()
        self.region_filter.setObjectName("regionFilter")
        self.region_filter.addItem("ALL REPORTS", "ALL REPORTS")
        self.region_filter.currentIndexChanged.connect(self.on_region_filter_changed)
        controls.addWidget(self.region_filter, 1)

        self.search_box = QLineEdit()
        self.search_box.setObjectName("feedSearch")
        self.search_box.setPlaceholderText("SEARCH REPORTS: headline, source, region, topic...")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self.on_search_changed)
        controls.addWidget(self.search_box, 2)
        events_layout.addLayout(controls)

        self.event_list = QListWidget()
        self.event_list.itemClicked.connect(self.open_article_link)
        self.event_list.addItem("[ SYSTEM ] Intelligence feed startup pending")
        events_layout.addWidget(self.event_list)

        global_box = QGroupBox("GLOBAL THREATS")
        global_layout = QVBoxLayout(global_box)
        self.ukraine_label = self.make_monitor("● UKRAINE: AWAITING DATA")
        self.taiwan_label = self.make_monitor("● TAIWAN: AWAITING DATA")
        self.middle_east_label = self.make_monitor("● MIDDLE EAST: AWAITING DATA")
        self.china_sea_label = self.make_monitor("● SOUTH CHINA SEA: AWAITING DATA")
        self.global_threat_labels = [self.ukraine_label, self.taiwan_label, self.middle_east_label, self.china_sea_label]
        for label in self.global_threat_labels:
            global_layout.addWidget(label)
        global_layout.addStretch()
        top.addWidget(events_box, 3)
        top.addWidget(global_box, 1)
        main.addLayout(top, 1)

        bottom = QHBoxLayout()
        map_box = QGroupBox("GLOBAL OPERATIONS MAP")
        map_layout = QVBoxLayout(map_box)
        map_layout.setContentsMargins(8, 14, 8, 8)
        self.map_widget = MapWidget()
        map_layout.addWidget(self.map_widget)

        homeland_box = QGroupBox("HOMELAND WATCH")
        homeland_layout = QVBoxLayout(homeland_box)
        self.cyber_label = self.make_monitor("● CYBER: AWAITING DATA")
        self.infrastructure_label = self.make_monitor("● INFRASTRUCTURE: AWAITING DATA")
        self.border_label = self.make_monitor("● BORDER SECURITY: AWAITING DATA")
        self.public_safety_label = self.make_monitor("● PUBLIC SAFETY: AWAITING DATA")
        self.energy_label = self.make_monitor("● ENERGY GRID: AWAITING DATA")
        self.transportation_label = self.make_monitor("● TRANSPORTATION: AWAITING DATA")
        self.homeland_labels = [self.cyber_label, self.infrastructure_label, self.border_label, self.public_safety_label, self.energy_label, self.transportation_label]
        for label in self.homeland_labels:
            homeland_layout.addWidget(label)
        homeland_layout.addStretch()
        bottom.addWidget(map_box, 3)
        bottom.addWidget(homeland_box, 1)
        main.addLayout(bottom, 2)
        self.setCentralWidget(central)
        self.statusBar().showMessage("SYSTEM ONLINE | FEEDS STANDBY | TACTICAL MAP ONLINE")

    def make_monitor(self, text):
        label = QLabel(text)
        label.setObjectName("monitorLabel")
        label.setWordWrap(True)
        return label

    def configure_refresh_timer(self):
        self.rss_refresh_timer = QTimer(self)
        self.rss_refresh_timer.setInterval(self.REFRESH_INTERVAL_MS)
        self.rss_refresh_timer.timeout.connect(self.start_rss_refresh)
        self.rss_refresh_timer.start()

    def configure_headline_rotation_timer(self):
        self.headline_rotation_timer = QTimer(self)
        self.headline_rotation_timer.setInterval(self.ROTATION_INTERVAL_MS)
        self.headline_rotation_timer.timeout.connect(self.rotate_headlines)
        self.headline_rotation_timer.start()

    @Slot()
    def start_rss_refresh(self):
        if self.rss_refresh_in_progress:
            return
        self.rss_refresh_in_progress = True
        if not self.current_articles:
            self.event_list.clear()
            self.event_list.addItem("[ SYSTEM ] Connecting to intelligence feeds...")
        self.statusBar().showMessage("SYSTEM ONLINE | REFRESHING FEEDS | TACTICAL MAP ONLINE")
        self.rss_thread = QThread(self)
        self.rss_worker = RSSWorker()
        self.rss_worker.moveToThread(self.rss_thread)
        self.rss_thread.started.connect(self.rss_worker.run)
        self.rss_worker.articles_ready.connect(self.handle_rss_articles)
        self.rss_worker.error.connect(self.handle_rss_error)
        self.rss_worker.finished.connect(self.rss_thread.quit)
        self.rss_worker.finished.connect(self.rss_worker.deleteLater)
        self.rss_thread.finished.connect(self.handle_rss_refresh_finished)
        self.rss_thread.finished.connect(self.rss_thread.deleteLater)
        self.rss_thread.start()

    @Slot(list)
    def handle_rss_articles(self, articles):
        self.current_articles = articles
        self.article_rotation_index = 0
        self.last_feed_update = datetime.now().astimezone()
        if not articles:
            self.event_list.clear()
            self.event_list.addItem("[ WARNING ] No RSS articles were received")
            return
        self.update_global_threats(articles)
        self.update_homeland_watch(articles)
        self.rebuild_region_filter()
        self.apply_active_filters()
        self.render_article_list()
        self.update_status_message()

    def rebuild_region_filter(self):
        previous = self.active_region_filter
        counts = {}
        for article in self.current_articles:
            region = str(article.get("region", "")).strip().upper()
            if region and region != "GLOBAL":
                counts[region] = counts.get(region, 0) + 1
        ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        self.region_filter.blockSignals(True)
        self.region_filter.clear()
        self.region_filter.addItem(f"ALL REPORTS ({len(self.current_articles)})", "ALL REPORTS")
        for region, count in ordered:
            self.region_filter.addItem(f"{region} ({count})", region)
        index = self.region_filter.findData(previous)
        if index < 0:
            index = 0
            self.active_region_filter = "ALL REPORTS"
        self.region_filter.setCurrentIndex(index)
        self.region_filter.blockSignals(False)

    @Slot(int)
    def on_region_filter_changed(self, index):
        self.active_region_filter = str(self.region_filter.itemData(index) or "ALL REPORTS")
        self.article_rotation_index = 0
        self.apply_active_filters()
        self.render_article_list()
        self.update_status_message()

    @Slot(str)
    def on_search_changed(self, text):
        self.search_query = str(text).strip().casefold()
        self.article_rotation_index = 0
        self.apply_active_filters()
        self.render_article_list()
        self.update_status_message()

    def apply_active_filters(self):
        selected = self.active_region_filter.upper()
        terms = self.REGION_ALIASES.get(selected, {selected.casefold()})
        matches, seen = [], set()

        for article in self.current_articles:
            region = str(article.get("region", "")).strip().upper()
            text = self.searchable_article_text(article)

            region_match = (
                selected == "ALL REPORTS"
                or region == selected
                or any(term in text for term in terms)
            )
            search_match = (
                not self.search_query
                or self.search_query in text
            )
            if not region_match or not search_match:
                continue

            key = self.article_key(article)
            if key in seen:
                continue
            seen.add(key)
            matches.append(article)

        self.filtered_articles = sorted(matches, key=self.safe_article_score, reverse=True)

    def searchable_article_text(self, article):
        fields = (
            article.get("title", ""), article.get("summary", ""),
            article.get("source", ""), article.get("region", ""),
            article.get("category", ""), article.get("event_type", ""),
        )
        return " ".join(str(value) for value in fields).casefold()

    @Slot()
    def rotate_headlines(self):
        if len(self.filtered_articles) <= 1:
            return
        rotating_count = len(self.filtered_articles) - 1
        self.article_rotation_index = (self.article_rotation_index + self.ROTATING_ARTICLES_PER_PAGE) % rotating_count
        self.render_article_list()

    def render_article_list(self):
        self.event_list.clear()
        if not self.filtered_articles:
            self.event_list.addItem("[ FILTER ] No matching reports")
            return
        self.event_list.addItem(self.build_article_item(self.filtered_articles[0], True))
        remaining = self.filtered_articles[1:self.MAX_VISIBLE_ARTICLES]
        if not remaining:
            return
        count = min(self.ROTATING_ARTICLES_PER_PAGE, len(remaining))
        for offset in range(count):
            index = (self.article_rotation_index + offset) % len(remaining)
            self.event_list.addItem(self.build_article_item(remaining[index]))

    def build_article_item(self, article, pinned=False):
        score = self.safe_article_score(article)
        event_type = str(article.get("event_type", "NEWS")).upper()
        code = self.EVENT_CODES.get(event_type, "INT")
        prefix = "[ PINNED URGENT ]" if pinned else f"[ {code} ]"
        timestamp = self.format_timestamp(article)
        title = article.get("title", "Untitled report")
        source = article.get("source", "Unknown source")
        region = article.get("region", "GLOBAL")
        link = article.get("link", "")
        item = QListWidgetItem(f"{prefix} [ {score:03d} ] {timestamp} | {title} :: {source} :: {region} :: {'OPEN LINK' if link else 'NO LINK'}")
        item.setData(Qt.ItemDataRole.UserRole, link)
        item.setToolTip("Click to open the report in your browser.")
        if pinned:
            item.setForeground(Qt.GlobalColor.red)
        return item

    @Slot(object)
    def open_article_link(self, item):
        link = item.data(Qt.ItemDataRole.UserRole)
        if link:
            QDesktopServices.openUrl(QUrl(str(link)))

    def format_timestamp(self, article):
        raw = article.get("published") or article.get("updated") or ""
        parsed = None
        if raw:
            try:
                parsed = parsedate_to_datetime(str(raw))
            except (TypeError, ValueError, OverflowError):
                pass
        if parsed is None:
            parsed = self.last_feed_update or datetime.now().astimezone()
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone()
        return parsed.strftime("%m/%d/%Y %I:%M %p")

    def update_status_message(self):
        search_text = self.search_box.text().strip()
        search_status = f" | SEARCH: {search_text}" if search_text else ""
        self.statusBar().showMessage(
            f"SYSTEM ONLINE | {len(self.filtered_articles)}/{len(self.current_articles)} REPORTS"
            f" | REGION: {self.active_region_filter}{search_status}"
            " | ROTATION 10 SEC | REFRESH 3 MIN | TACTICAL MAP ONLINE"
        )

    def update_global_threats(self, articles):
        rules = [
            (self.ukraine_label, "UKRAINE", {"UKRAINE", "CRIMEA", "BLACK SEA", "RUSSIA", "NATO"}, self.REGION_ALIASES["UKRAINE"]),
            (self.taiwan_label, "TAIWAN", {"TAIWAN", "TAIWAN STRAIT"}, self.REGION_ALIASES["TAIWAN"]),
            (self.middle_east_label, "MIDDLE EAST", {"MIDDLE EAST", "ISRAEL", "GAZA", "IRAN", "IRAQ", "YEMEN", "RED SEA"}, self.REGION_ALIASES["MIDDLE EAST"]),
            (self.china_sea_label, "SOUTH CHINA SEA", {"SOUTH CHINA SEA", "PHILIPPINES"}, self.REGION_ALIASES["SOUTH CHINA SEA"]),
        ]
        for label, name, regions, terms in rules:
            matches = [a for a in articles if str(a.get("region", "")).upper() in regions or any(t in self.searchable_article_text(a) for t in terms)]
            self.set_signal(label, name, matches)

    def update_homeland_watch(self, articles):
        rules = [
            (self.cyber_label, "CYBER", {"cyberattack", "ransomware", "malware", "data breach"}),
            (self.infrastructure_label, "INFRASTRUCTURE", {"critical infrastructure", "pipeline", "water system"}),
            (self.border_label, "BORDER SECURITY", {"border security", "border patrol", "border crossing"}),
            (self.public_safety_label, "PUBLIC SAFETY", {"public safety", "domestic threat", "terrorism"}),
            (self.energy_label, "ENERGY GRID", {"power grid", "power outage", "power plant"}),
            (self.transportation_label, "TRANSPORTATION", {"airport security", "rail disruption", "port security"}),
        ]
        for label, name, terms in rules:
            matches = []
            for article in articles:
                region = str(article.get("region", "")).upper()
                text = self.searchable_article_text(article)
                if region == "UNITED STATES" and any(term in text for term in terms):
                    matches.append(article)
            self.set_signal(label, name, matches)

    def set_signal(self, label, name, articles):
        score = self.calculate_signal_score(articles)
        level = self.get_signal_level(score)
        color = self.SIGNAL_COLORS[level]
        label.setText(f"● {name}: {level}\n  SIGNAL {score} | {len(articles)} REPORTS")
        label.setStyleSheet(f"color:{color}; background:#031008; border-left:3px solid {color}; padding:10px;")

    def calculate_signal_score(self, articles):
        total = 0
        for index, article in enumerate(sorted(articles, key=self.safe_article_score, reverse=True)[:12]):
            event_type = str(article.get("event_type", "NEWS")).upper()
            total += int((min(self.safe_article_score(article), 150) + self.EVENT_WEIGHTS.get(event_type, 0)) * max(0.30, 1.0-index*0.06))
        return total + min(len(articles)*2, 30)

    def get_signal_level(self, score):
        if score >= 700: return "CRITICAL"
        if score >= 450: return "HIGH"
        if score >= 250: return "ELEVATED"
        if score >= 100: return "GUARDED"
        if score > 0: return "LOW"
        return "NO SIGNAL"

    def safe_article_score(self, article):
        try:
            return max(0, int(article.get("score", 0)))
        except (TypeError, ValueError):
            return 0

    def article_key(self, article):
        return str(article.get("link") or article.get("title", "")).strip().casefold()

    @Slot(str)
    def handle_rss_error(self, message):
        self.statusBar().showMessage(f"FEED ERROR | {message} | RETRY IN 3 MIN")

    @Slot()
    def handle_rss_refresh_finished(self):
        self.rss_refresh_in_progress = False
        self.rss_worker = None
        self.rss_thread = None

    def apply_theme(self):
        self.setStyleSheet("""
        QMainWindow, QWidget { background:#000; color:#00ff66; font-family:Consolas, monospace; font-size:13px; }
        QLabel#header { color:#39ff14; border:1px solid #00aa44; font-size:27px; font-weight:bold; letter-spacing:4px; padding:14px; }
        QGroupBox { background:#020805; color:#39ff14; border:1px solid #00aa44; border-radius:4px; margin-top:12px; padding-top:14px; font-weight:bold; }
        QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 6px; background:#000; }
        QLabel#monitorLabel { color:#00ff66; background:#031008; border-left:3px solid #00cc55; padding:10px; margin:2px; }
        QListWidget { background:#010604; color:#00ff66; border:1px solid #006b2d; padding:4px; }
        QListWidget::item { border-bottom:1px solid #063317; padding:8px; }
        QListWidget::item:selected { background:#073b1c; color:#aaffc4; }
        QComboBox#regionFilter, QLineEdit#feedSearch { background:#010604; color:#39ff14; border:1px solid #00883a; padding:7px 10px; font-weight:bold; }
        QComboBox#regionFilter:focus, QLineEdit#feedSearch:focus { border:1px solid #39ff14; }
        QComboBox#regionFilter QAbstractItemView { background:#010604; color:#00ff66; selection-background-color:#073b1c; }
        QGraphicsView { background:#000; border:1px dashed #007f36; }
        QStatusBar { background:#010604; color:#00aa44; border-top:1px solid #006b2d; }
        QToolTip { background:#031008; color:#39ff14; border:1px solid #00aa44; }
        """)

    def closeEvent(self, event):
        self.rss_refresh_timer.stop()
        self.headline_rotation_timer.stop()
        if self.rss_thread is not None and self.rss_thread.isRunning():
            self.rss_thread.quit()
            self.rss_thread.wait(5000)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
