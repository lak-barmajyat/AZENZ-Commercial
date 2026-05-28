from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import QSize, Qt

def create_uniform_icon(image_path, target_size=18, icon_size=16):
    """
    Creates a perfectly uniform, centered icon with fixed outer margins.
    - target_size: The full canvas square size (e.g., 24px)
    - icon_size: The actual size of the image inside (e.g., 16px)
    """
    # 1. Load the original image file
    original = QPixmap(image_path)
    
    # 2. Scale the image down uniformly to your inner icon size
    # scaled = original.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    # 3. Create a blank transparent bounding box square
    canvas = QPixmap(QSize(target_size, target_size))
    canvas.fill(Qt.transparent)
    
    # 4. Paint the scaled image exactly into the center of the canvas
    painter = QPainter(canvas)
    x_offset = (target_size - original.width()) // 2
    y_offset = (target_size - original.height()) // 2
    painter.drawPixmap(x_offset, y_offset, original)
    painter.end()
    
    return QIcon(canvas)


def get_colored_icon(icon_source, color_name, size=QSize(24, 24)):
    """
    Recolors an icon's pixels while preserving transparency.
    Accepts a QIcon, QPixmap, or a string file path.
    """
    # 1. Extract a QPixmap depending on what type of input was passed
    if isinstance(icon_source, QIcon):
        pixmap = icon_source.pixmap(size)
    elif isinstance(icon_source, str):
        pixmap = QPixmap(icon_source)
    elif isinstance(icon_source, QPixmap):
        pixmap = QPixmap(icon_source) # Create a copy to protect original
    else:
        return QIcon()

    # Safety check if the image failed to load or extract
    if pixmap.isNull():
        return QIcon()

    # 2. Apply the color using the alpha channel mask
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color_name))
    painter.end()
    
    return QIcon(pixmap)
