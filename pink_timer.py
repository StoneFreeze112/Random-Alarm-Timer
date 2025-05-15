import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt, QTime, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class PinkTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.music_folder_path = None
        self.timer_duration_seconds = 0
        self.remaining_seconds = 0
        self.is_timer_running = False
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pink Timer Deluxe")
        self.setGeometry(300, 300, 450, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Timer Display
        self.timer_display_label = QLabel("00:00", self)
        self.timer_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_display_label.setFont(QFont("Arial", 60, QFont.Weight.Bold))
        self.timer_display_label.setObjectName("timerDisplay")
        main_layout.addWidget(self.timer_display_label)

        # Preset Timer Buttons
        presets_layout = QHBoxLayout()
        self.preset_buttons = []
        for minutes in [2, 10, 15]:
            btn = QPushButton(f"{minutes} min", self)
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda checked, m=minutes: self.start_timer_action(m))
            presets_layout.addWidget(btn)
            self.preset_buttons.append(btn)
        main_layout.addLayout(presets_layout)

        # Separator Line
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line1)

        # Music Folder Selection
        music_folder_layout = QVBoxLayout()
        music_folder_layout.setSpacing(5)
        self.select_folder_button = QPushButton("📂 Select Music Folder", self)
        self.select_folder_button.setFixedHeight(40)
        self.select_folder_button.clicked.connect(self.select_music_folder)
        music_folder_layout.addWidget(self.select_folder_button)

        self.folder_path_label = QLabel("No music folder selected.", self)
        self.folder_path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.folder_path_label.setWordWrap(True)
        self.folder_path_label.setFixedHeight(30)
        music_folder_layout.addWidget(self.folder_path_label)
        main_layout.addLayout(music_folder_layout)

        # Separator Line
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)

        # Control Button (Stop/Reset)
        self.stop_reset_button = QPushButton("⏹️ Stop / Reset", self)
        self.stop_reset_button.setFixedHeight(45)
        self.stop_reset_button.clicked.connect(self.stop_reset_action)
        self.stop_reset_button.setEnabled(False)
        main_layout.addWidget(self.stop_reset_button)

        # Status Label
        self.status_label = QLabel("Set a timer or select a music folder.", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedHeight(25)
        main_layout.addWidget(self.status_label)

        # QTimer for countdown
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

        # Connect media player signals
        self.media_player.mediaStatusChanged.connect(self.check_music_finished)

        self.apply_pink_theme()
        self.reset_ui_state(initial=True)

    def apply_pink_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFF0F5; /* LavenderBlush */
            }
            QLabel {
                color: #5D4037; /* Brownish-pink */
            }
            QLabel#timerDisplay {
                color: #D81B60; /* Hot Pink */
            }
            QPushButton {
                background-color: #FFC0CB; /* Pink */
                color: #4A235A; /* Dark Purple */
                border: 1px solid #FFB6C1; /* LightPink */
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFB6C1; /* LightPink */
            }
            QPushButton:pressed {
                background-color: #FF69B4; /* HotPink */
            }
            QPushButton:disabled {
                background-color: #F8BBD0; /* Lighter Pink */
                color: #C8A2C8; /* Light lilac */
            }
            QFrame[frameShape="5"] {
                color: #FFB6C1; /* LightPink */
            }
        """)

    def select_music_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            self.music_folder_path = folder
            display_path = os.path.basename(folder) if len(folder) <= 30 else "..." + folder[-27:]
            self.folder_path_label.setText(f"Folder: {display_path}")
            self.folder_path_label.setToolTip(folder)
            self.status_label.setText("Music folder selected. Ready to set timer.")
        else:
            self.folder_path_label.setText("No music folder selected.")
            self.status_label.setText("Music folder selection cancelled.")

    def start_timer_action(self, minutes):
        if not self.music_folder_path:
            QMessageBox.warning(self, "No Folder", "Please select a music folder first.")
            return

        if self.is_timer_running or self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.stop_reset_action()

        self.timer_duration_seconds = minutes * 60
        self.remaining_seconds = self.timer_duration_seconds
        self.is_timer_running = True

        self.update_timer_display()
        self.countdown_timer.start(1000)

        self.status_label.setText(f"Timer set for {minutes} minutes. Running...")
        self.stop_reset_button.setEnabled(True)
        self.select_folder_button.setEnabled(False)
        for btn in self.preset_buttons:
            btn.setEnabled(False)

    def update_countdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_display()
        else:
            self.countdown_timer.stop()
            self.is_timer_running = False
            self.handle_timer_finish()

    def update_timer_display(self):
        time_obj = QTime(0, 0, 0).addSecs(self.remaining_seconds)
        self.timer_display_label.setText(time_obj.toString("mm:ss"))

    def handle_timer_finish(self):
        self.timer_display_label.setText("🎉 Go! 🎉")
        self.play_random_music()

    def play_random_music(self):
        if not self.music_folder_path or not os.path.isdir(self.music_folder_path):
            self.status_label.setText("Error: Music folder not found or invalid.")
            self.reset_ui_state()
            return

        try:
            mp3_files = [f for f in os.listdir(self.music_folder_path) if f.lower().endswith(".mp3")]
            if not mp3_files:
                QMessageBox.warning(self, "No MP3 Files", "No MP3 files found in the selected folder.")
                self.reset_ui_state()
                return

            random_file = random.choice(mp3_files)
            full_song_path = os.path.join(self.music_folder_path, random_file)

            self.media_player.setSource(QUrl.fromLocalFile(full_song_path))
            self.media_player.play()

            self.status_label.setText(f"Playing: {random_file[:30]}{'...' if len(random_file)>30 else ''}")
            self.stop_reset_button.setText("🔇 Stop Music")
            self.stop_reset_button.setEnabled(True)

        except Exception as e:
            self.status_label.setText(f"Error playing music: {str(e)}")
            self.reset_ui_state()

    def check_music_finished(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.stop()
            self.status_label.setText("Music finished. Timer complete.")
            self.reset_ui_state()

    def stop_music(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.stop()
        self.status_label.setText("Music stopped.")

    def stop_reset_action(self):
        if self.is_timer_running:
            self.countdown_timer.stop()
            self.is_timer_running = False
            self.status_label.setText("Timer stopped and reset.")

        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.stop_music()

        self.reset_ui_state()

    def reset_ui_state(self, initial=False):
        self.remaining_seconds = 0
        self.update_timer_display()
        self.select_folder_button.setEnabled(True)
        for btn in self.preset_buttons:
            btn.setEnabled(True)
        self.stop_reset_button.setEnabled(False)
        self.stop_reset_button.setText("⏹️ Stop / Reset")
        if initial:
            self.status_label.setText("Set a timer or select a music folder.")
        elif not self.is_timer_running and self.media_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.status_label.setText("Ready for new timer.")

    def closeEvent(self, event):
        self.media_player.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_app = PinkTimerApp()
    timer_app.show()
    sys.exit(app.exec())
