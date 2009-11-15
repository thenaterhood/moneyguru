# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-08
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from __future__ import division

from itertools import combinations
from math import radians, sin

from PyQt4.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt4.QtGui import QWidget, QPainter, QFont, QPen, QColor, QBrush, QLinearGradient

def pointInCircle(center, radius, angle):
    # Returns the point at the edge of a circle with specified center/radius/angle
    # a/sin(A) = b/sin(B) = c/sin(C) = 2R
    # the start point is (center.x + radius, center.y) and goes counterclockwise
    # (this was based on the objc implementation, but since the Ys are upside down in Qt, we have
    # to switch the Ys here as well)
    angle = angle % 360
    C = radians(90)
    A = radians(angle % 90)
    B = C - A
    c = radius
    ratio = c / sin(C)
    b = ratio * sin(B)
    a = ratio * sin(A)
    if angle > 270:
        return QPointF(center.x() + a, center.y() + b)
    elif angle > 180:
        return QPointF(center.x() - b, center.y() + a)
    elif angle > 90:
        return QPointF(center.x() - a, center.y() - b)
    else:
        return QPointF(center.x() + b, center.y() - a)

def rectFromCenter(center, size):
    # Returns a QRectF centered on `center` with size `size`
    x = center.x() - size.width() / 2
    y = center.y() - size.height() / 2
    return QRectF(QPointF(x, y), size)

def pullRectIn(rect, container):
    if container.contains(rect):
        return
    if rect.top() < container.top():
        rect.moveTop(container.top())
    elif rect.bottom() > container.bottom():
        rect.moveBottom(container.bottom())
    if rect.left() < container.left():
        rect.moveLeft(container.left())
    elif rect.right() > container.right():
        rect.moveRight(container.right())

class Legend(object):
    PADDING = 2 # the padding between legend text and the rectangle behind it
    
    def __init__(self, text, color, angle):
        self.text = text
        self.color = color
        self.angle = angle
        self.basePoint = None
        self.textRect = None
        self.labelRect = None
    
    def computeLabelRect(self):
        padding = self.PADDING
        self.labelRect = self.textRect.adjusted(-padding, -padding, padding*2, padding*2)
    
    def computeTextRect(self):
        padding = self.PADDING
        self.textRect = self.labelRect.adjusted(padding, padding, -padding*2, -padding*2)
    

class PieChartView(QWidget):
    PADDING = 4
    TITLE_FONT_FAMILY = "Lucida Grande"
    TITLE_FONT_SIZE = 15
    LEGEND_FONT_FAMILY = "Lucida Grande"
    LEGEND_FONT_SIZE = 11
    LINE_WIDTH = 1
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.dataSource = None
        COLORS = [
            (93, 188, 86),
            (60, 91, 206),
            (182, 24, 31),
            (233, 151, 9),
            (149, 33, 233),
            (128, 128, 128),
        ]
        
        gradients = []
        for r, g, b in COLORS:
            gradient = QLinearGradient(0, 0, 0, 1)
            gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
            color = QColor(r, g, b)
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, color.lighter())
            gradients.append(gradient)
        self.gradients = gradients
        
        self.titleFont = QFont(self.TITLE_FONT_FAMILY, self.TITLE_FONT_SIZE, QFont.Bold)
        self.legendFont = QFont(self.LEGEND_FONT_FAMILY, self.LEGEND_FONT_SIZE, QFont.Normal)
    
    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        if self.dataSource is None:
            return
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing|QPainter.TextAntialiasing)
        painter.fillRect(self.rect(), Qt.white)
        ds = self.dataSource
        
        # view dimensions
        viewWidth = self.width()
        viewHeight = self.height()
        
        # title dimensions
        painter.setFont(self.titleFont)
        fm = painter.fontMetrics()
        titleText = ds.title
        titleHeight = fm.height()
        titleAscent = fm.ascent()
        titleWidth = fm.width(titleText)
        
        # circle coords
        maxWidth = viewWidth - (self.PADDING * 2)
        maxHeight = viewHeight - titleHeight - (self.PADDING * 2)
        # circleBounds is the area in which the circle is allwed to be drawn (important for legend text)
        circleBounds = QRectF(self.PADDING, self.PADDING + titleHeight, maxWidth, maxHeight)
        circleSize = min(maxWidth, maxHeight)
        radius = circleSize / 2
        center = circleBounds.center()
        # cirectRect is the area that the pie drawing use for bounds
        circleRect = QRectF(center.x() - radius, center.y() - radius, circleSize, circleSize)
        
        # draw title
        painter.setFont(self.titleFont)
        titleX = (viewWidth - titleWidth) / 2
        titleY = self.PADDING + titleAscent
        painter.drawText(QPointF(titleX, titleY), titleText)
        
        # draw pie
        totalAmount = sum(amount for _, amount in ds.data)
        startAngle = 0
        legends = []
        for (legendText, amount), gradient in zip(ds.data, self.gradients):
            fraction = amount / totalAmount
            angle = fraction * 360
            painter.setBrush(QBrush(gradient))
            # pie slices have to be drawn with 1/16th of an angle as argument
            painter.drawPie(circleRect, startAngle*16, angle*16)
            # stops is a QVector<QPair<qreal, QColor>>. We chose the dark color of the gardient.
            legendColor = gradient.stops()[0][1]
            legendAngle = startAngle + (angle / 2)
            legend = Legend(text=legendText, color=legendColor, angle=legendAngle)
            legends.append(legend)
            startAngle += angle
        
        # compute legend rects
        painter.setFont(self.legendFont)
        fm = painter.fontMetrics()
        legendHeight = fm.height()
        
        # base rects
        for legend in legends:
            legend.basePoint = pointInCircle(center, radius, legend.angle)
            legendWidth = fm.width(legend.text)
            legend.textRect = rectFromCenter(legend.basePoint, QSizeF(legendWidth, legendHeight))
            legend.computeLabelRect()
        
        # make sure they're inside circleBounds
        for legend in legends:
            pullRectIn(legend.labelRect, circleBounds)
        
        # now, the tricky part: Make sure the labels are not over one another. It's not always
        # possible, and doing it properly can get very complicated. What we're doing here is to 
        # first to compare every rect with the next one, and if they intersect, we move the highest
        # one further up. After that, it's possible that intersects still exist, but they'd me more
        # on the X axis, so we compare each rect with every other, and we move them apart on the X
        # axis as much as we can (within circleBounds). This is not perfect because in some cases
        # it moves labels on the Y axis when it would be prettier to move them on the X axis, but
        # handling those cases would likely make the code significantly more complex.
        for legend1, legend2 in zip(legends, legends[1:]):
            rect1, rect2 = legend1.labelRect, legend2.labelRect
            if not rect1.intersects(rect2):
                continue
            # Here, we use legend.basePoint.y() rather than rect.top() to determine which rect is
            # the highest because rect1 might already have been pushed up earlier, and end up being
            # the highest, when in fact it's rect2 that "deserves" to be the highest.
            p1, p2 = legend1.basePoint, legend2.basePoint
            highest, lowest = (rect1, rect2) if p1.y() < p2.y() else (rect2, rect1)
            highest.moveBottom(lowest.top()-1)
        
        for legend1, legend2 in combinations(legends, 2):
            rect1, rect2 = legend1.labelRect, legend2.labelRect
            if not rect1.intersects(rect2):
                continue
            leftr, rightr = (rect1, rect2) if rect1.left() < rect2.left() else (rect2, rect1)
            leftr.moveRight(rightr.left()-1)
            pullRectIn(leftr, circleBounds)
            if not leftr.intersects(rightr):
                continue
            rightr.moveLeft(leftr.right()+1)
            pullRectIn(rightr, circleBounds) # at this point, if we still have inter, we don't care
        
        # draw legends
        painter.setBrush(QBrush(Qt.white))
        for legend in legends:
            pen = QPen(legend.color)
            pen.setWidth(self.LINE_WIDTH)
            painter.setPen(pen)
            painter.drawRect(legend.labelRect) # The label behind the text
            painter.setPen(QPen(Qt.black))
            legend.computeTextRect()
            painter.drawText(legend.textRect, 0, legend.text) # the text
    