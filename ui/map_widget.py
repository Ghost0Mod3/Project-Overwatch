"""
Project Overwatch
Native Offline Tactical World Map
"""

import json
import math
from pathlib import Path

from PySide6.QtCore import (
    QPointF,
    QTimer,
    Qt
)

from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPen
)

from PySide6.QtWidgets import (
    QFrame,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsPathItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView
)


class MapWidget(QGraphicsView):

    MAP_WIDTH = 2000
    MAP_HEIGHT = 1000

    def __init__(self, parent=None):
        super().__init__(parent)

        # ------------------------------------------
        # Scene
        # ------------------------------------------

        self.map_scene = QGraphicsScene(self)

        self.setScene(
            self.map_scene
        )

        self.setSceneRect(
            0,
            0,
            self.MAP_WIDTH,
            self.MAP_HEIGHT
        )

        # ------------------------------------------
        # Appearance
        # ------------------------------------------

        self.setBackgroundBrush(
            QBrush(
                QColor("#000000")
            )
        )

        self.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True
        )

        self.setRenderHint(
            QPainter.RenderHint.TextAntialiasing,
            True
        )

        # ------------------------------------------
        # Pan and zoom
        # ------------------------------------------

        self.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.minimum_scale = 0.1
        self.maximum_scale = 8.0
        self.has_fitted_view = False

        # ------------------------------------------
        # Map data
        # ------------------------------------------

        self.project_root = (
            Path(__file__).resolve().parent.parent
        )

        self.geojson_path = (
            self.project_root
            / "resources"
            / "world.geojson"
        )

        # ------------------------------------------
        # Animated hotspot data
        # ------------------------------------------

        self.animated_pulses = []
        self.pulse_phase = 0.0

        self.build_map()

        self.pulse_timer = QTimer(self)

        self.pulse_timer.timeout.connect(
            self.update_hotspot_pulses
        )

        # Roughly 30 frames per second.
        self.pulse_timer.start(
            33
        )

    # ==================================================
    # BUILD MAP
    # ==================================================

    def build_map(self):
        self.map_scene.clear()

        self.animated_pulses.clear()
        self.pulse_phase = 0.0

        self.draw_background()
        self.draw_grid()
        self.draw_world_trace()
        self.draw_reference_lines()
        self.draw_hotspots()
        self.draw_overlay_text()

    # ==================================================
    # BACKGROUND
    # ==================================================

    def draw_background(self):
        self.map_scene.setBackgroundBrush(
            QBrush(
                QColor("#000000")
            )
        )

    # ==================================================
    # COORDINATE GRID
    # ==================================================

    def draw_grid(self):
        minor_pen = QPen(
            QColor("#062814"),
            1
        )

        minor_pen.setCosmetic(
            True
        )

        major_pen = QPen(
            QColor("#075f2a"),
            1
        )

        major_pen.setCosmetic(
            True
        )

        major_pen.setStyle(
            Qt.PenStyle.DashLine
        )

        # Longitude lines
        for longitude in range(
            -180,
            181,
            15
        ):
            x, _ = self.geo_to_scene(
                longitude,
                0
            )

            is_major = (
                longitude % 45 == 0
            )

            line = QGraphicsLineItem(
                x,
                0,
                x,
                self.MAP_HEIGHT
            )

            line.setPen(
                major_pen
                if is_major
                else minor_pen
            )

            line.setZValue(
                -90
            )

            self.map_scene.addItem(
                line
            )

            if is_major:
                self.add_longitude_label(
                    longitude,
                    x
                )

        # Latitude lines
        for latitude in range(
            -90,
            91,
            15
        ):
            _, y = self.geo_to_scene(
                0,
                latitude
            )

            is_major = (
                latitude % 30 == 0
            )

            line = QGraphicsLineItem(
                0,
                y,
                self.MAP_WIDTH,
                y
            )

            line.setPen(
                major_pen
                if is_major
                else minor_pen
            )

            line.setZValue(
                -90
            )

            self.map_scene.addItem(
                line
            )

            if is_major:
                self.add_latitude_label(
                    latitude,
                    y
                )

    def add_longitude_label(
        self,
        longitude,
        x
    ):
        if longitude == 0:
            label_text = "0°"

        elif longitude > 0:
            label_text = (
                f"{longitude}°E"
            )

        else:
            label_text = (
                f"{abs(longitude)}°W"
            )

        label = self.create_map_text(
            label_text,
            size=8,
            color="#00883a"
        )

        label.setPos(
            x + 4,
            7
        )

        label.setZValue(
            90
        )

        self.map_scene.addItem(
            label
        )

    def add_latitude_label(
        self,
        latitude,
        y
    ):
        if latitude == 0:
            label_text = "0°"

        elif latitude > 0:
            label_text = (
                f"{latitude}°N"
            )

        else:
            label_text = (
                f"{abs(latitude)}°S"
            )

        label = self.create_map_text(
            label_text,
            size=8,
            color="#00883a"
        )

        label.setPos(
            7,
            y + 3
        )

        label.setZValue(
            90
        )

        self.map_scene.addItem(
            label
        )

    # ==================================================
    # WORLD GEOJSON TRACE
    # ==================================================

    def draw_world_trace(self):
        """
        Load resources/world.geojson and draw all country
        polygons with neon-green outlines.
        """

        if not self.geojson_path.exists():
            self.draw_missing_map_message()
            return

        try:
            with self.geojson_path.open(
                "r",
                encoding="utf-8"
            ) as geojson_file:

                geojson_data = json.load(
                    geojson_file
                )

        except OSError as error:
            self.draw_map_error_message(
                f"Unable to read world.geojson: {error}"
            )

            return

        except json.JSONDecodeError as error:
            self.draw_map_error_message(
                f"Invalid GeoJSON: {error}"
            )

            return

        features = geojson_data.get(
            "features",
            []
        )

        if not features:
            self.draw_map_error_message(
                "world.geojson contains no features."
            )

            return

        for feature in features:
            geometry = feature.get(
                "geometry"
            )

            if not geometry:
                continue

            geometry_type = geometry.get(
                "type",
                ""
            )

            coordinates = geometry.get(
                "coordinates",
                []
            )

            if geometry_type == "Polygon":
                self.draw_polygon_geometry(
                    coordinates
                )

            elif geometry_type == "MultiPolygon":
                for polygon_coordinates in coordinates:
                    self.draw_polygon_geometry(
                        polygon_coordinates
                    )

    def draw_polygon_geometry(
        self,
        polygon_coordinates
    ):
        """
        Convert one GeoJSON polygon into a Qt painter path.
        """

        country_path = QPainterPath()

        country_path.setFillRule(
            Qt.FillRule.OddEvenFill
        )

        for ring in polygon_coordinates:
            self.add_ring_to_path(
                country_path,
                ring
            )

        if country_path.isEmpty():
            return

        country_item = QGraphicsPathItem(
            country_path
        )

        country_pen = QPen(
            QColor("#00dd55"),
            1.35
        )

        # Keep line width consistent while zooming.
        country_pen.setCosmetic(
            True
        )

        country_item.setPen(
            country_pen
        )

        country_item.setBrush(
            QBrush(
                QColor(
                    0,
                    38,
                    18,
                    75
                )
            )
        )

        country_item.setZValue(
            -30
        )

        self.map_scene.addItem(
            country_item
        )

    def add_ring_to_path(
        self,
        path,
        ring
    ):
        """
        Add a single GeoJSON coordinate ring to a Qt path.

        Large jumps in longitude are split at the international
        date line to prevent lines crossing the whole map.
        """

        if len(ring) < 3:
            return

        current_segment = []
        previous_longitude = None

        for coordinate in ring:
            if len(coordinate) < 2:
                continue

            try:
                longitude = float(
                    coordinate[0]
                )

                latitude = float(
                    coordinate[1]
                )

            except (
                TypeError,
                ValueError
            ):
                continue

            crossed_date_line = (
                previous_longitude is not None
                and abs(
                    longitude
                    - previous_longitude
                ) > 180
            )

            if crossed_date_line:
                self.append_segment_to_path(
                    path,
                    current_segment,
                    close_segment=False
                )

                current_segment = []

            current_segment.append(
                (
                    longitude,
                    latitude
                )
            )

            previous_longitude = longitude

        self.append_segment_to_path(
            path,
            current_segment,
            close_segment=True
        )

    def append_segment_to_path(
        self,
        path,
        segment,
        close_segment
    ):
        """
        Convert a longitude/latitude segment into scene points.
        """

        if len(segment) < 2:
            return

        first_longitude = segment[0][0]
        first_latitude = segment[0][1]

        first_x, first_y = self.geo_to_scene(
            first_longitude,
            first_latitude
        )

        path.moveTo(
            QPointF(
                first_x,
                first_y
            )
        )

        for longitude, latitude in segment[1:]:
            x, y = self.geo_to_scene(
                longitude,
                latitude
            )

            path.lineTo(
                QPointF(
                    x,
                    y
                )
            )

        if (
            close_segment
            and len(segment) >= 3
        ):
            path.closeSubpath()

    # ==================================================
    # REFERENCE LINES
    # ==================================================

    def draw_reference_lines(self):
        equator_pen = QPen(
            QColor("#19ff70"),
            1.3
        )

        equator_pen.setCosmetic(
            True
        )

        equator_pen.setStyle(
            Qt.PenStyle.DashLine
        )

        prime_pen = QPen(
            QColor("#00aa44"),
            1.3
        )

        prime_pen.setCosmetic(
            True
        )

        prime_pen.setStyle(
            Qt.PenStyle.DashLine
        )

        # Equator
        _, equator_y = self.geo_to_scene(
            0,
            0
        )

        equator_line = QGraphicsLineItem(
            0,
            equator_y,
            self.MAP_WIDTH,
            equator_y
        )

        equator_line.setPen(
            equator_pen
        )

        equator_line.setZValue(
            -20
        )

        self.map_scene.addItem(
            equator_line
        )

        # Prime meridian
        prime_x, _ = self.geo_to_scene(
            0,
            0
        )

        prime_line = QGraphicsLineItem(
            prime_x,
            0,
            prime_x,
            self.MAP_HEIGHT
        )

        prime_line.setPen(
            prime_pen
        )

        prime_line.setZValue(
            -20
        )

        self.map_scene.addItem(
            prime_line
        )

    # ==================================================
    # HOTSPOTS
    # ==================================================

    def draw_hotspots(self):
        """
        Prototype hotspot values used to test visualization.

        These values are not live threat assessments.
        """

        hotspots = [
            {
                "name": "UKRAINE",
                "latitude": 49.0,
                "longitude": 32.0,
                "intensity": 95
            },
            {
                "name": "MIDDLE EAST",
                "latitude": 31.5,
                "longitude": 35.0,
                "intensity": 88
            },
            {
                "name": "TAIWAN",
                "latitude": 23.7,
                "longitude": 121.0,
                "intensity": 72
            },
            {
                "name": "WASHINGTON D.C.",
                "latitude": 38.9072,
                "longitude": -77.0369,
                "intensity": 38
            }
        ]

        for hotspot in hotspots:
            self.add_hotspot(
                name=hotspot["name"],
                latitude=hotspot["latitude"],
                longitude=hotspot["longitude"],
                intensity=hotspot["intensity"]
            )

    def add_hotspot(
        self,
        name,
        latitude,
        longitude,
        intensity
    ):
        x, y = self.geo_to_scene(
            longitude,
            latitude
        )

        hotspot_color = self.get_hotspot_color(
            intensity
        )

        # ------------------------------------------
        # Animated pulse rings
        # ------------------------------------------

        ring_count = 4

        for ring_index in range(
            ring_count
        ):
            starting_progress = (
                ring_index
                / ring_count
            )

            minimum_diameter = 18.0

            maximum_diameter = (
                62.0
                + float(intensity) * 0.35
            )

            starting_diameter = (
                minimum_diameter
                + (
                    maximum_diameter
                    - minimum_diameter
                )
                * starting_progress
            )

            ring = QGraphicsEllipseItem(
                x - starting_diameter / 2,
                y - starting_diameter / 2,
                starting_diameter,
                starting_diameter
            )

            ring_color = QColor(
                hotspot_color
            )

            ring_color.setAlpha(
                150
            )

            ring_pen = QPen(
                ring_color,
                2
            )

            ring_pen.setCosmetic(
                True
            )

            ring.setPen(
                ring_pen
            )

            fill_color = QColor(
                hotspot_color
            )

            fill_color.setAlpha(
                10
            )

            ring.setBrush(
                QBrush(
                    fill_color
                )
            )

            ring.setOpacity(
                1.0
                - starting_progress
            )

            ring.setZValue(
                30
            )

            self.map_scene.addItem(
                ring
            )

            self.animated_pulses.append(
                {
                    "item": ring,
                    "x": x,
                    "y": y,
                    "minimum_diameter": minimum_diameter,
                    "maximum_diameter": maximum_diameter,
                    "offset": starting_progress,
                    "color": hotspot_color
                }
            )

        # ------------------------------------------
        # Hotspot center
        # ------------------------------------------

        core = QGraphicsEllipseItem(
            x - 5,
            y - 5,
            10,
            10
        )

        core.setBrush(
            QBrush(
                QColor(
                    hotspot_color
                )
            )
        )

        core.setPen(
            QPen(
                QColor("#ffffff"),
                1
            )
        )

        core.setToolTip(
            f"{name}\n"
            f"INTENSITY: {intensity}\n"
            f"LATITUDE: {latitude:.4f}\n"
            f"LONGITUDE: {longitude:.4f}"
        )

        core.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

        core.setZValue(
            50
        )

        self.map_scene.addItem(
            core
        )

        # ------------------------------------------
        # Hotspot label
        # ------------------------------------------

        label = self.create_map_text(
            f"{name} [{intensity}]",
            size=8,
            color=hotspot_color,
            bold=True
        )

        label.setPos(
            x + 12,
            y - 13
        )

        label.setZValue(
            60
        )

        self.map_scene.addItem(
            label
        )

    def get_hotspot_color(
        self,
        intensity
    ):
        if intensity >= 85:
            return "#ff3344"

        if intensity >= 65:
            return "#ff8c00"

        if intensity >= 45:
            return "#ffe600"

        return "#39ff14"

    # ==================================================
    # HOTSPOT ANIMATION
    # ==================================================

    def update_hotspot_pulses(self):
        self.pulse_phase += 0.012

        if self.pulse_phase >= 1.0:
            self.pulse_phase -= 1.0

        for pulse in self.animated_pulses:
            ring = pulse["item"]

            if ring.scene() is None:
                continue

            progress = (
                self.pulse_phase
                + pulse["offset"]
            ) % 1.0

            eased_progress = (
                0.5
                - 0.5
                * math.cos(
                    progress
                    * math.pi
                )
            )

            minimum_diameter = pulse[
                "minimum_diameter"
            ]

            maximum_diameter = pulse[
                "maximum_diameter"
            ]

            diameter = (
                minimum_diameter
                + (
                    maximum_diameter
                    - minimum_diameter
                )
                * eased_progress
            )

            x = pulse["x"]
            y = pulse["y"]

            ring.setRect(
                x - diameter / 2,
                y - diameter / 2,
                diameter,
                diameter
            )

            opacity = max(
                0.05,
                1.0 - progress
            )

            ring.setOpacity(
                opacity
            )

            pen_width = max(
                0.8,
                2.6
                - progress * 1.4
            )

            pulse_color = QColor(
                pulse["color"]
            )

            pulse_color.setAlpha(
                int(
                    210
                    * opacity
                )
            )

            pulse_pen = QPen(
                pulse_color,
                pen_width
            )

            pulse_pen.setCosmetic(
                True
            )

            ring.setPen(
                pulse_pen
            )

    # ==================================================
    # OVERLAY TEXT
    # ==================================================

    def draw_overlay_text(self):
        title = self.create_map_text(
            "OVERWATCH GLOBAL THREAT TOPOGRAPHY",
            size=13,
            color="#39ff14",
            bold=True
        )

        title.setPos(
            22,
            self.MAP_HEIGHT - 48
        )

        title.setZValue(
            100
        )

        self.map_scene.addItem(
            title
        )

        controls = self.create_map_text(
            "DRAG: PAN  |  WHEEL: ZOOM  |  DOUBLE-CLICK: RESET",
            size=8,
            color="#00aa44"
        )

        controls.setPos(
            self.MAP_WIDTH - 440,
            self.MAP_HEIGHT - 40
        )

        controls.setZValue(
            100
        )

        self.map_scene.addItem(
            controls
        )

    def create_map_text(
        self,
        text,
        size=8,
        color="#00ff66",
        bold=False
    ):
        text_item = QGraphicsSimpleTextItem(
            str(text)
        )

        font_weight = (
            QFont.Weight.Bold
            if bold
            else QFont.Weight.Normal
        )

        text_item.setFont(
            QFont(
                "Consolas",
                size,
                font_weight
            )
        )

        text_item.setBrush(
            QBrush(
                QColor(
                    color
                )
            )
        )

        return text_item

    # ==================================================
    # ERROR MESSAGES
    # ==================================================

    def draw_missing_map_message(self):
        message = self.create_map_text(
            "WORLD MAP DATA NOT FOUND\n"
            "ADD resources/world.geojson",
            size=18,
            color="#ff8c00",
            bold=True
        )

        message.setPos(
            650,
            440
        )

        message.setZValue(
            100
        )

        self.map_scene.addItem(
            message
        )

    def draw_map_error_message(
        self,
        error_text
    ):
        message = self.create_map_text(
            "WORLD MAP DATA ERROR\n"
            f"{error_text}",
            size=14,
            color="#ff3344",
            bold=True
        )

        message.setPos(
            350,
            440
        )

        message.setZValue(
            100
        )

        self.map_scene.addItem(
            message
        )

    # ==================================================
    # COORDINATE CONVERSION
    # ==================================================

    def geo_to_scene(
        self,
        longitude,
        latitude
    ):
        longitude = max(
            -180.0,
            min(
                180.0,
                float(longitude)
            )
        )

        latitude = max(
            -90.0,
            min(
                90.0,
                float(latitude)
            )
        )

        x = (
            longitude
            + 180.0
        ) / 360.0 * self.MAP_WIDTH

        y = (
            90.0
            - latitude
        ) / 180.0 * self.MAP_HEIGHT

        return x, y

    def scene_to_geo(
        self,
        x,
        y
    ):
        longitude = (
            float(x)
            / self.MAP_WIDTH
            * 360.0
            - 180.0
        )

        latitude = (
            90.0
            - float(y)
            / self.MAP_HEIGHT
            * 180.0
        )

        return (
            latitude,
            longitude
        )

    # ==================================================
    # VIEW CONTROLS
    # ==================================================

    def wheelEvent(
        self,
        event
    ):
        current_scale = (
            self.transform().m11()
        )

        if event.angleDelta().y() > 0:
            zoom_factor = 1.20

        else:
            zoom_factor = (
                1.0
                / 1.20
            )

        proposed_scale = (
            current_scale
            * zoom_factor
        )

        if (
            self.minimum_scale
            <= proposed_scale
            <= self.maximum_scale
        ):
            self.scale(
                zoom_factor,
                zoom_factor
            )

        event.accept()

    def mouseDoubleClickEvent(
        self,
        event
    ):
        self.reset_map_view()
        event.accept()

    def reset_map_view(self):
        self.resetTransform()

        self.fitInView(
            self.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

    def resizeEvent(
        self,
        event
    ):
        super().resizeEvent(
            event
        )

        if not self.has_fitted_view:
            self.reset_map_view()
            self.has_fitted_view = True