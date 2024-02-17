from OpenGL.GL import *
from PySide6.QtGui import QMatrix4x4


class Sprite:

    def __init__(self, program, spriteNames, spriteInfo, texture):
        self.program = program
        self.spriteNames = spriteNames
        self.vertPosBuffer = spriteInfo["vertPosBuffer"]
        self.texCoordBuffer = spriteInfo["texCoordBuffer"]
        self.spriteSizes = spriteInfo["spriteSizes"]
        self.texture = texture
        self.mvpMatrix = QMatrix4x4()
        self.modelMatrix = QMatrix4x4()
        self.x = 0
        self.y = 0
        self.w = self.spriteSizes[0].x()
        self.h = self.spriteSizes[0].y()
        self.drawingIndex = 0

        self.program.bind()
        self.aPositionLocation = self.program.attributeLocation("aPosition")
        self.aTexCoordLocation = self.program.attributeLocation("aTexCoord")
        self.uMvpMatrixLocation = self.program.uniformLocation("uMvpMatrix")

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setSize(self, w, h):
        self.w = w
        self.h = h

    def setTextureRect(self, spriteName):
        index = self.spriteNames.index(spriteName)
        self.w = self.spriteSizes[index].x()
        self.h = self.spriteSizes[index].y()
        self.drawingIndex = index * 4

    def bind(self):
        self.program.bind()
        self.texture.bind()

        self.vertPosBuffer.bind()
        self.program.setAttributeBuffer(self.aPositionLocation, GL_FLOAT, 0, 2)
        self.program.enableAttributeArray(self.aPositionLocation)

        self.texCoordBuffer.bind()
        self.program.setAttributeBuffer(self.aTexCoordLocation, GL_FLOAT, 0, 2)
        self.program.enableAttributeArray(self.aTexCoordLocation)

    def draw(self, projViewMatrix):
        self.bind()
        self.modelMatrix.setToIdentity()
        self.modelMatrix.translate(self.x, self.y)
        self.modelMatrix.scale(self.w, self.h, 1)
        self.mvpMatrix = projViewMatrix * self.modelMatrix
        self.program.setUniformValue(self.uMvpMatrixLocation, self.mvpMatrix)
        glDrawArrays(GL_TRIANGLE_STRIP, self.drawingIndex, 4)
