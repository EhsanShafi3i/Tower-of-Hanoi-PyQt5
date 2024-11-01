import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog, QMessageBox, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPixmap

class TowerOfHanoi(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.reset()

    def setup_ui(self):
        self.setWindowTitle("Tower of Hanoi - PyQt5")
        self.resize(800, 500)

        self.timer = QTimer()
        self.timer.timeout.connect(self.move_step)

        self.move_count_label = QLabel("Moves: 0", self)
        self.move_count_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        button_size = (150, 40)

        self.start_button = QPushButton("Start Animation", self)
        self.start_button.setFixedSize(*button_size)
        self.start_button.setStyleSheet("font-size: 16px;")
        self.start_button.clicked.connect(self.start_animation)

        self.speed_up_button = QPushButton("Speed Up", self)
        self.speed_up_button.setFixedSize(*button_size)
        self.speed_up_button.setStyleSheet("font-size: 16px;")
        self.speed_up_button.clicked.connect(self.speed_up_animation)

        self.slow_down_button = QPushButton("Slow Down", self)
        self.slow_down_button.setFixedSize(*button_size)
        self.slow_down_button.setStyleSheet("font-size: 16px;")
        self.slow_down_button.clicked.connect(self.slow_down_animation)

        self.finish_button = QPushButton("Finish", self)
        self.finish_button.setFixedSize(*button_size)
        self.finish_button.setStyleSheet("font-size: 16px;")
        self.finish_button.clicked.connect(self.finish_animation)

        self.creator_label = QLabel("Created by Ehsan Shafiei", self)
        self.creator_label.setStyleSheet("font-size: 12px; color: gray;")

        self.copyright_icon = QLabel(self)
        self.set_copyright_icon()

        layout = QVBoxLayout()
        layout.addWidget(self.move_count_label)
        layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.speed_up_button)
        button_layout.addWidget(self.slow_down_button)
        button_layout.addWidget(self.finish_button)
        layout.addLayout(button_layout)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(self.creator_label)
        footer_layout.addWidget(self.copyright_icon)
        layout.addLayout(footer_layout)

        self.setLayout(layout)

    def speed_up_animation(self):
        current_interval = self.timer.interval()
        self.timer.setInterval(max(100, current_interval // 2))
    def slow_down_animation(self):

        current_interval = self.timer.interval()
        self.timer.setInterval(current_interval * 2) 

    def finish_animation(self):
        self.timer.stop()
        while self.steps:
            self.move_step()
        QMessageBox.information(self, "Animation Finished", f"The Tower of Hanoi animation is complete!\nTotal Moves: {self.move_count}")
        self.reset()

    def set_copyright_icon(self):

        self.copyright_icon.setPixmap(QPixmap("path_to_copyright_logo.png").scaled(20, 20))

    def reset(self):

        self.disks, ok = QInputDialog.getInt(self, "Number of Disks", "Enter the number of disks:")
        if not ok or self.disks < 1:
            sys.exit()

        self.steps = []
        self.source = list(range(self.disks, 0, -1))
        self.temp = []
        self.dest = []

        self.move_count = 0
        self.move_count_label.setText("Moves: 0")

        self.solve_hanoi(self.disks, self.source, self.dest, self.temp)

        self.start_button.setEnabled(True)
        self.update()

    def start_animation(self):

        self.start_button.setEnabled(False)
        self.timer.start(500)

    def move_step(self):
    
        if not self.steps:
            self.timer.stop()
            QMessageBox.information(self, "Animation Finished", f"The Tower of Hanoi animation is complete!\nTotal Moves: {self.move_count}")
            self.reset()
            return
        source, dest = self.steps.pop(0)
        dest.append(source.pop())
        self.move_count += 1
        self.move_count_label.setText(f"Moves: {self.move_count}")
        self.update()

    def solve_hanoi(self, n, source, dest, temp):

        if n == 1:
            self.steps.append((source, dest))
        else:
            self.solve_hanoi(n - 1, source, temp, dest)
            self.steps.append((source, dest))
            self.solve_hanoi(n - 1, temp, dest, source)

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.draw_towers(qp)
        qp.end()

    def draw_towers(self, qp):
        window_width = self.width()
        window_height = self.height()

        tower_width = int(window_width * 0.02)
        tower_height = int(window_height * 0.5)
        base_height = int(window_height * 0.8)
        disk_height = int(window_height * 0.04)

        color_list = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255),
                      QColor(255, 255, 0), QColor(255, 0, 255), QColor(0, 255, 255),
                      QColor(255, 128, 0), QColor(128, 0, 255)]

        tower_positions = [int(window_width * 0.2), int(window_width * 0.5), int(window_width * 0.8)]

        qp.setBrush(QColor(100, 100, 100))
        for x in tower_positions:
            qp.drawRect(int(x - (tower_width // 2)), int(base_height - tower_height), tower_width, tower_height)

        for tower, x in zip([self.source, self.temp, self.dest], tower_positions):
            for i, disk in enumerate(tower):
                qp.setBrush(color_list[disk % len(color_list)])
                disk_width = int(window_width * 0.04 * disk)
                disk_x = int(x - (disk_width // 2))
                disk_y = int(base_height - (i + 1) * disk_height)
                qp.drawRect(disk_x, disk_y, disk_width, disk_height)

    def speed_up_animation(self):
        current_interval = self.timer.interval()
        self.timer.setInterval(max(100, current_interval // 2))
    def finish_animation(self):
        self.timer.stop()
        while self.steps:
            self.move_step()
        QMessageBox.information(self, "Animation Finished", f"The Tower of Hanoi animation is complete!\nTotal Moves: {self.move_count}")
        self.reset()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TowerOfHanoi()
    window.show()
    sys.exit(app.exec_())
