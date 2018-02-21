class OCRResponseWord:
    def __init__(self, textValue,boundingBoxValue ):
        self.boundingBox = boundingBoxValue
        self.text = textValue
