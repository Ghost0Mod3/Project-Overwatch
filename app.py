"""
Project Overwatch
Application Entry Point
"""

import sys
import traceback

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox
)

from ui.main_window import MainWindow


REQUIRED_MAIN_WINDOW_METHODS = [
    "build_ui",
    "apply_theme",
    "configure_refresh_timer",
    "start_rss_refresh",
    "handle_rss_articles",
    "update_global_threats",
    "update_homeland_watch"
]


def validate_main_window():
    """
    Confirm that MainWindow contains every method required
    by the current Project Overwatch build.
    """

    missing_methods = [
        method_name
        for method_name in REQUIRED_MAIN_WINDOW_METHODS
        if not hasattr(
            MainWindow,
            method_name
        )
    ]

    if missing_methods:
        missing_text = "\n".join(
            f"  - {method_name}"
            for method_name in missing_methods
        )

        raise RuntimeError(
            "ui/main_window.py is incomplete.\n\n"
            "Missing MainWindow methods:\n"
            f"{missing_text}\n\n"
            "Replace ui/main_window.py with the complete "
            "coordinated version."
        )


def install_exception_handler():
    """
    Display unexpected application errors in PowerShell
    and in a visible message box.
    """

    def handle_exception(
        exception_type,
        exception_value,
        exception_traceback
    ):
        error_text = "".join(
            traceback.format_exception(
                exception_type,
                exception_value,
                exception_traceback
            )
        )

        print(
            "\n[PROJECT OVERWATCH ERROR]\n"
            f"{error_text}",
            file=sys.stderr
        )

        try:
            QMessageBox.critical(
                None,
                "Project Overwatch Error",
                error_text
            )

        except Exception:
            pass

    sys.excepthook = handle_exception


def create_application():
    """
    Create and configure the Qt application.
    """

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Project Overwatch"
    )

    app.setApplicationDisplayName(
        "Project Overwatch"
    )

    app.setOrganizationName(
        "Project Overwatch"
    )

    app.setStyle(
        "Fusion"
    )

    app.setQuitOnLastWindowClosed(
        True
    )

    return app


def main():
    install_exception_handler()

    app = create_application()

    try:
        validate_main_window()

        window = MainWindow()

        window.show()

        window.raise_()
        window.activateWindow()

        return app.exec()

    except Exception as error:
        error_text = "".join(
            traceback.format_exception(
                type(error),
                error,
                error.__traceback__
            )
        )

        print(
            "\n[PROJECT OVERWATCH STARTUP ERROR]\n"
            f"{error_text}",
            file=sys.stderr
        )

        QMessageBox.critical(
            None,
            "Project Overwatch Startup Error",
            error_text
        )

        return 1


if __name__ == "__main__":
    sys.exit(
        main()
    )