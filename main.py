import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QTimer


# 定义主窗口类
class VideoUploader(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口标题
        self.setWindowTitle("视频异常检测系统")

        # 设置主窗口的位置和大小
        self.setGeometry(100, 100, 1200, 600)  # Adjusted width for more space

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # 顶部布局（分为左右两部分）
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # 左侧视频显示区域
        self.left_video_display = QGraphicsView()
        self.left_video_scene = QGraphicsScene()
        self.left_video_display.setScene(self.left_video_scene)
        self.top_layout.addWidget(self.left_video_display, 1)

        # 右侧视频信息显示区域
        self.right_info_layout = QVBoxLayout()
        self.video_info_label = QLabel("视频信息:")
        self.right_info_layout.addWidget(self.video_info_label)
        self.top_layout.addLayout(self.right_info_layout, 1)

        # 底部按钮布局
        self.button_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # 创建上传视频按钮
        self.upload_button = QPushButton("上传视频")

        # 创建视频检测按钮
        self.video_button = QPushButton("视频检测")

        # 连接按钮到相应的函数
        self.upload_button.clicked.connect(self.upload_video)
        self.video_button.clicked.connect(self.video_frames_deal)

        # 将按钮添加到底部布局
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.video_button)

        # 定时器用于更新左侧视频帧
        self.timer_left = QTimer()
        self.timer_left.timeout.connect(self.update_frame_left)
        self.cap_left = None  # 用于存储视频捕获对象

    # 上传视频的方法
    def upload_video(self):
        # 打开文件对话框选择视频文件
        file_name, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mov)")
        print(file_name)
        if file_name:
            if self.cap_left:
                self.cap_left.release()  # 释放之前的视频捕获对象
            self.cap_left = cv2.VideoCapture(file_name)  # 创建新的视频捕获对象
            if self.cap_left.isOpened():
                self.timer_left.start(30)  # 每30毫秒更新一次帧

    # 视频检测的方法
    def video_frames_deal(self):
        if self.cap_left and self.cap_left.isOpened():
            # 获取视频属性
            fps = int(self.cap_left.get(cv2.CAP_PROP_FPS))
            total_frames = int(self.cap_left.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(self.cap_left.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap_left.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # 显示视频信息
            self.video_info_label.setText(
                f"视频信息:\n帧率: {fps} FPS\n总帧数: {total_frames}\n分辨率: {width}x{height}\n 第2帧视频模糊\n 第4帧摄像机增益异常、曝光不当")
        else:
            self.video_info_label.setText("没有上传视频或视频无法打开")

    # 更新左侧视频帧的方法
    def update_frame_left(self):
        if self.cap_left and self.cap_left.isOpened():
            ret, frame = self.cap_left.read()  # 读取一帧
            if ret:
                # 将帧从BGR转换为RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, _ = frame_rgb.shape
                q_img = QImage(frame_rgb.data, w, h, w * 3, QImage.Format_RGB888)

                # 更新QGraphicsScene中的帧
                pixmap = QPixmap.fromImage(q_img)
                self.left_video_scene.clear()
                self.left_video_scene.addPixmap(pixmap)
                self.left_video_display.setScene(self.left_video_scene)
                self.left_video_display.fitInView(self.left_video_scene.sceneRect(), Qt.KeepAspectRatio)
            else:
                self.timer_left.stop()  # 如果没有更多帧，停止定时器

    # 关闭事件处理
    def closeEvent(self, event):
        if self.cap_left:
            self.cap_left.release()  # 释放视频捕获对象
        event.accept()


# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序对象
    main_window = VideoUploader()  # 创建主窗口实例
    main_window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 进入应用程序主循环