import glm
import math
def getRotationMatrices(rotX, rotY, rotZ):
    rotXMatrix = glm.mat4(1.0)
    rotXMatrix[1][1] = math.cos(rotX)
    rotXMatrix[1][2] = math.sin(rotX)
    rotXMatrix[2][1] = -math.sin(rotX)
    rotXMatrix[2][2] = math.cos(rotX)
    rotYMatrix = glm.mat4(1.0)
    rotYMatrix[0][0] = math.cos(rotY)
    rotYMatrix[0][2] = -math.sin(rotY)
    rotYMatrix[2][0] = math.sin(rotY)
    rotYMatrix[2][2] = math.cos(rotY)
    rotZMatrix = glm.mat4(1.0)
    rotZMatrix[0][0] = math.cos(rotZ)
    rotZMatrix[0][1] = math.sin(rotZ)
    rotZMatrix[1][0] = -math.sin(rotZ)
    rotZMatrix[1][1] = math.cos(rotZ)
    return rotXMatrix * rotYMatrix * rotZMatrix


def createRotationMatrix(matrix, value):
    matrix[0][0] = math.cos(value)
    matrix[0][1] = math.sin(value)
    matrix[1][0] = -math.sin(value)
    matrix[1][1] = math.cos(value)
    return matrix