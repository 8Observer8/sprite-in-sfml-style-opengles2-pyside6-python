from OpenGL.GL import *
from PySide6.QtCore import QFile, QIODevice, QJsonDocument
from PySide6.QtGui import QImage, QMatrix4x4, QVector3D
from PySide6.QtOpenGL import (QOpenGLShader, QOpenGLShaderProgram,
                              QOpenGLTexture, QOpenGLWindow)

from sprite import Sprite
from sprite_info import SpriteInfo


class OpenGLWindow(QOpenGLWindow):

    def __init__(self):
        super().__init__()
        self.setTitle("OpenGL ES 2.0, PySide6, Python")
        self.resize(350, 350)

    def initializeGL(self):
        glClearColor(0.02, 0.61, 0.85, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.program = QOpenGLShaderProgram(self)
        self.program.create()
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Vertex,
            "assets/shaders/texture.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Fragment,
            "assets/shaders/texture.frag")
        self.program.link()

        self.texture = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.texture.create()
        self.texture.setData(QImage("assets/sprites/texture.png"))
        self.texture.setMinMagFilters(QOpenGLTexture.Filter.Nearest,
            QOpenGLTexture.Filter.Nearest)
        self.texture.setWrapMode(QOpenGLTexture.WrapMode.ClampToEdge)

        file = QFile("assets/sprites/texture.json")
        file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        content = file.readAll()
        file.close()
        doc = QJsonDocument.fromJson(content)
        spriteNames = ["simple_level.png", "enemy_walk_1.png", "mario_dead.png",
            "coin.png", "mario_run_0.png"]
        spriteInfo = SpriteInfo().getInfo(doc, spriteNames)

        self.sprite = Sprite(self.program, spriteNames, spriteInfo, self.texture)

        self.projMatrix = QMatrix4x4()
        self.viewMatrix = QMatrix4x4()
        self.viewMatrix.lookAt(QVector3D(0, 0, 1), QVector3D(0, 0, 0),
            QVector3D(0, 1, 0))

    def resizeGL(self, w, h):
        aspect = w / h
        self.projMatrix.setToIdentity()
        if (w > h):
            self.projMatrix.ortho(0, 128 * aspect, 0, 128, 1, -1)
        else:
            self.projMatrix.ortho(0, 128, 0, 128 / aspect, 1, -1)
        self.projViewMatrix = self.projMatrix * self.viewMatrix

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.sprite.setTextureRect("simple_level.png")
        self.sprite.setPosition(0 + 64, 0 + 64)
        self.sprite.draw(self.projViewMatrix)

        self.sprite.setTextureRect("enemy_walk_1.png")
        self.sprite.setPosition(16 * 1 + 64, -16 * 2 + 8 + 64)
        self.sprite.draw(self.projViewMatrix)

        self.sprite.setTextureRect("mario_dead.png")
        self.sprite.setPosition(0 + 64, 0 + 64)
        self.sprite.draw(self.projViewMatrix);

        self.sprite.setTextureRect("coin.png")
        self.sprite.setPosition(16 * 3 + 8 + 64, 16 * 1 + 8 + 64)
        self.sprite.draw(self.projViewMatrix)

        self.sprite.setTextureRect("mario_run_0.png")
        self.sprite.setPosition(16 * 2 + 8 + 64, 16 * 1 + 8 + 64)
        self.sprite.draw(self.projViewMatrix)

    def closeEvent(self, event):
        self.texture.destroy()
