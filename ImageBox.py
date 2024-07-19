'''
@Author:xu
@Time: 2024/17/5
@Function:Image Cropper with PySide2
pyinstaller --name=ImageBox -onefile --icon=icon.ico ImageBox.py
pyinstaller  --name=ImageBox --onefile --hidden-import=matplotlib.backends.backend_ps --icon=icon.ico ImageBox.py
'''

import sys
import cv2
from PySide2.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,QWidget,
                               QPushButton, QFileDialog, QLineEdit, QMessageBox)
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
import os 
from matplotlib.figure import Figure
class ImageCropper(QMainWindow):
    def __init__(self):
        super(ImageCropper, self).__init__()
        self.initUI()
        self.original_image = None
        self.cropped_image = None   #Box1
        self.cropped_image1 = None   #Box2
        self.point1 = None  # 左上角点
        self.point2 = None  # 右下角点
        self.format = '.eps'
        self.name = 'test'


    def initUI(self):

       
        self.setWindowTitle('ImageBox-v0.1')
        self.setGeometry(800, 100, 800, 600)

        # 垂直布局，用于添加label和编辑框组
        self.layout = QVBoxLayout()

        # 水平布局1，用于编辑框
        self.editLayout = QHBoxLayout()
        
        # 水平布局2，用于编辑框
        self.editLayout1 = QHBoxLayout()
        
        # 水平布局3，用于编辑框
        self.editLayout2 = QHBoxLayout()

        # 添加label到主布局
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        #输出信息
        self.outputInfo = QLineEdit(self)
        self.outputInfo.setReadOnly(True)
        self.layout.addWidget(self.outputInfo)

        #坐标信息1
        self.editX1 = QLineEdit()
        self.editY1 = QLineEdit()
        self.editWidth = QLineEdit()
        self.editHeight = QLineEdit()
        self.editX1.setPlaceholderText('X1')
        self.editY1.setPlaceholderText('Y1')
        self.editWidth.setPlaceholderText('Width')
        self.editHeight.setPlaceholderText('Height')
        self.editX1.setFixedSize(250, 30)
        self.editY1.setFixedSize(250, 30)
        self.editWidth.setFixedSize(250, 30)
        self.editHeight.setFixedSize(250, 30)
        self.editLayout.addWidget(self.editX1)
        self.editLayout.addWidget(self.editY1)
        self.editLayout.addWidget(self.editWidth)
        self.editLayout.addWidget(self.editHeight)
        self.layout.addLayout(self.editLayout)

        #坐标信息2
        self.editX2 = QLineEdit()
        self.editY2 = QLineEdit()
        self.editWidth2 = QLineEdit()
        self.editHeight2 = QLineEdit()
        self.editX2.setPlaceholderText('X2')
        self.editY2.setPlaceholderText('Y2')
        self.editWidth2.setPlaceholderText('Width')
        self.editHeight2.setPlaceholderText('Height')
        self.editX2.setFixedSize(250, 30)
        self.editY2.setFixedSize(250, 30)
        self.editWidth2.setFixedSize(250, 30)
        self.editHeight2.setFixedSize(250, 30)
        self.editLayout1.addWidget(self.editX2)
        self.editLayout1.addWidget(self.editY2)
        self.editLayout1.addWidget(self.editWidth2)
        self.editLayout1.addWidget(self.editHeight2)
        self.layout.addLayout(self.editLayout1)
        
        #输入信息-路径和名字-格式
        self.input_dir = QLineEdit()
        self.input_dir.setPlaceholderText('输入保存路径')
        self.input_dir.setFixedSize(350, 30)
        self.filename = QLineEdit()
        self.filename.setPlaceholderText('输入保存文件名(默认test)')
        self.filename.setFixedSize(350, 30)
        self.filemat = QLineEdit()
        self.filemat.setPlaceholderText('输入保存格式(默认.eps)')
        self.filemat.setFixedSize(350, 30)
        self.editLayout2.addWidget(self.input_dir)
        self.editLayout2.addWidget(self.filename)
        self.editLayout2.addWidget(self.filemat)
        self.layout.addLayout(self.editLayout2)

        #按钮load_image
        self.loadButton = QPushButton('加载图像', self)
        self.loadButton.clicked.connect(self.load_image)
        self.layout.addWidget(self.loadButton)

        #按钮Draw Rectangle
        self.drawButton = QPushButton('读取坐标', self)
        self.drawButton.clicked.connect(self.show_selection_window)
        self.layout.addWidget(self.drawButton)

        #按钮Crop Image
        self.cropButton = QPushButton('绘制矩形框', self)
        self.cropButton.clicked.connect(self.crop_image)
        self.layout.addWidget(self.cropButton)

        #按钮保存图像
        self.saveButton = QPushButton('保存图像', self)
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.save_image)
        self.layout.addWidget(self.saveButton)

        # 设置主布局到窗口
        self.setLayout(self.layout)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)


    def init_draw_rectangle(self):
        self.point1 = None
        self.point2 = None

    def show_selection_window(self):
        if self.original_image is None:
            QMessageBox.information(self, 'Error', "请先加载一张图片！")
            return
        else:
            self.init_draw_rectangle()
            self.selection_window = cv2.namedWindow('image')
            cv2.setMouseCallback('image', self.on_mouse)
            cv2.imshow('image', self.original_image)
            while True:
                cv2.waitKey(20)
                if self.point2:
                    break
            cv2.destroyAllWindows()

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point1 = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON:
            if self.point1:
                self.temp_image = self.original_image.copy()
                cv2.rectangle(self.temp_image, self.point1, (x, y), (255, 0, 0), 2)
                cv2.imshow('image', self.temp_image)
        elif event == cv2.EVENT_LBUTTONUP and self.point1:
            self.point2 = (x, y)
            self.cropped_image = self.original_image
            self.update_output_info()

    def update_output_info(self):
        min_x = min(self.point1[0], self.point2[0])
        min_y = min(self.point1[1], self.point2[1])
        width = abs(self.point1[0] - self.point2[0])
        height = abs(self.point1[1] - self.point2[1])
        self.saveButton.setEnabled(True)
        self.outputInfo.setText(f"Rectangle: X1: {min_x}, Y1: {min_y}, Width: {width}, Height: {height}")
        x1 = self.editX1.text()
        if x1 == "":
            self.editX1.setText(str(min_x))
            self.editY1.setText(str(min_y))
            self.editHeight.setText(str(height))
            self.editWidth.setText(str(width))
        else:
            self.editX2.setText(str(min_x))
            self.editY2.setText(str(min_y))
            self.editHeight2.setText(str(height))
            self.editWidth2.setText(str(width))

    def draw_rectangle(self, start_point, end_point):
        temp_image = self.original_image.copy()
        cv2.rectangle(temp_image, start_point, end_point, (0, 255, 0), 2)
        self.display_image(temp_image)

    def enable_save_crop(self):
        self.cropButton.setEnabled(True)
        self.saveButton.setEnabled(True)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                    "Image Files (*.png *.jpeg *.jpg *.bmp *.gif *.tif);;All Files (*)")
        if file_name:
            self.original_image = cv2.imread(file_name)
            if self.original_image is not None:
                self.display_image(self.original_image)
                self.drawButton.setEnabled(True)

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(convert_to_Qt_format)
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))

    def draw_outer_rectangle(self,image, color):
        """
        在图像的最外围绘制矩形框。

        参数:
        - image: 要绘制矩形框的图像。
        - color: 矩形框颜色的 RGB 值，类型为元组，例如 (255, 0, 0) 表示蓝色。
        """
        # 获取图像的高度和宽度
        height, width = image.shape[:2]

        # 定义矩形框的两个对角顶点
        top_left_corner = (0, 0)     # 图像的左上角
        bottom_right_corner = (width - 1, height - 1)  # 图像的右下角

        # 在图像上绘制矩形框
        cv2.rectangle(image, top_left_corner, bottom_right_corner, color, 2)  # 线条粗细设置为2

        return image

    def crop_image(self):
        try:
                x1 = int(self.editX1.text())
                y1 = int(self.editY1.text())
                width = int(self.editWidth.text())
                height = int(self.editHeight.text())

                # 绘制矩形框
                self.drawn_image = self.original_image.copy()
                cv2.rectangle(self.drawn_image, (x1, y1), (x1 + width, y1 + height), (0, 255, 0), 2) #绿色
               

                # 裁剪图像
                self.cropped_image = self.original_image[y1:y1 + height, x1:x1 + width]
                self.cropped_image = self.draw_outer_rectangle(self.cropped_image,(0, 255, 0))
                self.saveButton.setEnabled(True)


                # 检查第二个区域的坐标是否已经输入
                if self.editX2.text() and self.editY2.text():
                    # 裁剪第二个区域
                    x2 = int(self.editX2.text())
                    y2 = int(self.editY2.text())
                    width2 = int(self.editWidth2.text())
                    height2 = int(self.editHeight2.text())
                    cv2.rectangle(self.drawn_image, (x2, y2), (x2 + width2, y2 + height2), (255, 0, 0), 2)    #红色
                    self.cropped_image1 = self.original_image[y2:y2 + height2, x2:x2 + width2]
                    self.cropped_image1 = self.draw_outer_rectangle(self.cropped_image1,(255, 0, 0))
                    self.display_image(self.drawn_image)
                else:
                     self.display_image(self.drawn_image)
        except ValueError:
            QMessageBox.information(self, 'Error', "无效输入，请输入有效的值：整形.")

    def save_image_with_matplotlib(self,save_path, image):
        """
        使用matplotlib保存cv2读取的图像到指定路径，保持原始尺寸。
        
        参数:
        - image: cv2读取的图像，格式为NumPy数组。
        - save_path: 保存图像的文件路径，包括文件名和扩展名。
        """
        # 将BGR图像转换为RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 获取图像的尺寸
        height, width = image_rgb.shape[:2]
        
        # 创建一个matplotlib图形，其尺寸与图像相同
        fig = Figure(figsize=(width / 100, height / 100), dpi=300)
        # 添加一个子图
        ax = fig.add_subplot(111)
        
        # 显示图像
        ax.imshow(image_rgb)
        ax.axis('off')  # 隐藏坐标轴
        
        # 保存图像，不显示
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0.0)
        
        # 关闭图形，以释放资源
        plt.close(fig)

    def save_image(self):
        # 确保图像不为空
        if self.cropped_image is None:
            QMessageBox.information(self, 'Error', "No image to save.")
            return

        file_path = self.input_dir.text()
        if self.filename.text() != "":
            self.name = self.filename.text()

        if self.filemat.text() != "":
            self.format = self.filemat.text()

        # 检查保存路径
        if not file_path:
            options = QFileDialog.Options()
            directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Cropped Image", "",
                                                          options=options)
            if directory:
                self.input_dir.setText(directory)
            else:
                QMessageBox.information(self, 'Error', "没有选择保存路径，请再次选择或者手动输入路径！.")
                return
            file_path = directory

        # # 检查文件名和格式是否已输入
        # if not file_name or not file_format:
        #     if not file_name:
        #         QMessageBox.information(self, 'Error', "Please enter the file name to be saved.")
        #     if not file_format:
        #         QMessageBox.information(self, 'Error', "Please enter the format to be saved.")
        #     return

        # 构建保存路径
        drawn_file_path = os.path.join(file_path, self.name + self.format)
        cropped_file_path = os.path.join(file_path, f"{self.name}_crop1{self.format}")

        # 保存图像
        self.save_image_with_matplotlib(drawn_file_path, self.drawn_image)
        self.save_image_with_matplotlib(cropped_file_path, self.cropped_image)

        # 检查是否存在第二个裁剪图像
        if self.cropped_image1 is not None:
            cropped_file_path1 = os.path.join(file_path, f"{self.name}_crop2{self.format}")
            self.save_image_with_matplotlib(cropped_file_path1, self.cropped_image1)
            save_success_message = f'Images saved to: {drawn_file_path}, {cropped_file_path}, and {cropped_file_path1}'
        else:
            save_success_message = f'Images saved to: {drawn_file_path} and {cropped_file_path}'

        # 显示保存成功的消息
        QMessageBox.information(self, 'Save Successful', save_success_message)
# 主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    sys.exit(app.exec_())