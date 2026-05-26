from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


def fade_in(widget: QWidget, duration: int = 400):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    anim.start()
    widget._fade_anim = anim


def fade_in_delayed(widget: QWidget, delay: int = 100, duration: int = 400):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    effect.setOpacity(0.0)
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    from PyQt6.QtCore import QTimer
    QTimer.singleShot(delay, anim.start)
    widget._fade_anim = anim


def slide_in_from_bottom(widget: QWidget, distance: int = 30, duration: int = 500):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    opacity_anim = QPropertyAnimation(effect, b"opacity")
    opacity_anim.setDuration(duration)
    opacity_anim.setStartValue(0.0)
    opacity_anim.setEndValue(1.0)
    opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    pos_anim = QPropertyAnimation(widget, b"pos")
    pos_anim.setDuration(duration)
    start_pos = widget.pos()
    pos_anim.setStartValue(QPoint(start_pos.x(), start_pos.y() + distance))
    pos_anim.setEndValue(start_pos)
    pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    group = QParallelAnimationGroup(widget)
    group.addAnimation(opacity_anim)
    group.addAnimation(pos_anim)
    group.start()
    widget._slide_anim = group


def float_animation(widget: QWidget, amplitude: int = 6, duration: int = 2000):
    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    start_pos = widget.pos()
    anim.setKeyValueAt(0, start_pos)
    anim.setKeyValueAt(0.5, QPoint(start_pos.x(), start_pos.y() - amplitude))
    anim.setKeyValueAt(1, start_pos)
    anim.setEasingCurve(QEasingCurve.Type.InOutSine)
    anim.setLoopCount(-1)
    anim.start()
    widget._float_anim = anim


def stagger_fade_in(widgets: list, interval: int = 80, duration: int = 350):
    for i, widget in enumerate(widgets):
        fade_in_delayed(widget, delay=i * interval, duration=duration)
