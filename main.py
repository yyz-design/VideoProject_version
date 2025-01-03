import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoUploader(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("视频上传器")
        self.setGeometry(200, 200, 800, 600)

        # 外部布局（主布局）：上下布局
        main_layout = QVBoxLayout()

        # 上方布局（结果呈现区）：左右布局
        result_layout = QHBoxLayout()

        # 创建左侧视频预览区
        self.video_widget = QVideoWidget(self)
        result_layout.addWidget(self.video_widget, 3)  # 左侧视频预览区占3/4的空间

        # 创建右侧检测结果区
        self.result_label = QLabel("检测结果将在此显示", self)
        self.result_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label, 1)  # 右侧结果呈现区占1/4的空间

        # 将上方的结果呈现区添加到主布局
        main_layout.addLayout(result_layout)

        # 下方按钮区（垂直排列按钮）
        button_layout = QVBoxLayout()

        # 上传视频按钮
        self.upload_button = QPushButton("上传视频")
        self.upload_button.clicked.connect(self.upload_video)
        button_layout.addWidget(self.upload_button)

        # 视频检测按钮
        self.detect_button = QPushButton("视频检测")
        self.detect_button.clicked.connect(self.detect_video)
        button_layout.addWidget(self.detect_button)

        # 将按钮区添加到主布局
        main_layout.addLayout(button_layout)

        # 设置主布局
        self.setLayout(main_layout)

        # 创建一个媒体播放器对象
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)  # 设置视频输出到 QVideoWidget

    def upload_video(self):
        # 打开文件对话框，选择视频文件
        video_file, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mkv)")
        if video_file:
            # 打印视频文件路径
            print(f"加载的视频文件路径: {video_file}")

            # 设置播放器的媒体内容为选择的视频文件
            media = QMediaContent(QUrl.fromLocalFile(video_file))
            self.media_player.setMedia(media)

            # 检查视频是否准备好
            if not self.media_player.isVideoAvailable():
                print("视频文件无法加载或没有准备好，无法播放。")
                print(f"错误信息: {self.media_player.errorString()}")
            else:
                self.media_player.play()

    def detect_video(self):
        # 假设检测逻辑
        print("视频检测已启动！")
        # 在此可以加入视频检测的代码，展示检测结果
        # 例如：调用其他函数或显示检测信息到界面
        self.result_label.setText("检测结果：\n\n视频中检测到运动与物体识别结果。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoUploader()
    window.show()
    sys.exit(app.exec_())
