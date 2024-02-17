import numpy as np
from PySide6.QtGui import QVector2D
from PySide6.QtOpenGL import QOpenGLBuffer


class SpriteInfo():

    def getInfo(self, doc, spriteNames):
        docObject = doc.object()
        metaObject = docObject["meta"]
        sizeObject = metaObject["size"]
        atlasW = sizeObject["w"]
        atlasH = sizeObject["h"]

        vertPositions = []
        texCoords = []
        spriteSizes = []
        framesObject = docObject["frames"]

        for spriteName in spriteNames:
            vertPositions.extend([
                -0.5, 0.5,
                -0.5, -0.5,
                0.5, 0.5,
                0.5, -0.5])

            spriteObject = framesObject[spriteName]
            frameObject = spriteObject["frame"]
            tx = frameObject["x"] / atlasW
            ty = frameObject["y"] / atlasH
            tw = frameObject["w"] / atlasW
            th = frameObject["h"] / atlasH
            texCoords.extend([
                tx, ty,
                tx, ty + th,
                tx + tw, ty,
                tx + tw, ty + th])

            spriteW = frameObject["w"]
            spriteH = frameObject["h"]
            spriteSizes.append(QVector2D(spriteW, spriteH))

        vertPositions = np.array(vertPositions, dtype=np.float32)
        vertPosBuffer = QOpenGLBuffer()
        vertPosBuffer.create()
        vertPosBuffer.bind()
        vertPosBuffer.allocate(vertPositions, len(vertPositions) * 4)

        texCoords = np.array(texCoords, dtype=np.float32)
        texCoordBuffer = QOpenGLBuffer()
        texCoordBuffer.create()
        texCoordBuffer.bind()
        texCoordBuffer.allocate(texCoords, len(texCoords) * 4)

        return {
            "vertPosBuffer": vertPosBuffer,
            "texCoordBuffer": texCoordBuffer,
            "spriteSizes": spriteSizes }
