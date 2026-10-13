"""Qt desktop window. Thin shell over the pipeline."""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget

from age_progression_studio.core.pipeline import AgeProgressionPipeline
from age_progression_studio.utils.image_io import load_image, save_image


class StudioWindow(QMainWindow):
    def __init__(self, pipeline: AgeProgressionPipeline) -> None:
        super().__init__()
        self.pipeline = pipeline
        self.setWindowTitle("AI Age Progression Studio")
        self.resize(960, 720)
        self._src = None
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        self.age = QSlider()
        self.age.setMinimum(1)
        self.age.setMaximum(90)
        self.age.setValue(45)
        self.preview = QLabel("drop a face to begin")
        pick = QPushButton("Open face…")
        pick.clicked.connect(self._pick)
        run = QPushButton("Generate")
        run.clicked.connect(self._run)
        for w in (pick, self.preview, self.age, run):
            layout.addWidget(w)
        self.setCentralWidget(root)

    def _pick(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Face", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if path:
            self._src = load_image(Path(path))
            self.preview.setText(Path(path).name)

    def _run(self) -> None:
        if self._src is None:
            return
        out = self.pipeline.run(self._src, target_age=self.age.value())
        dest, _ = QFileDialog.getSaveFileName(self, "Save", "aged.png", "PNG (*.png)")
        if dest:
            save_image(Path(dest), out)


def launch_window(pipeline: AgeProgressionPipeline, args) -> int:
    app = QApplication(sys.argv)
    win = StudioWindow(pipeline)
    win.show()
    return app.exec()