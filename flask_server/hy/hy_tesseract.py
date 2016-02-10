import ctypes


def tesseract_detect(imcv):
    libtesseract_path = '/usr/local/lib/libtesseract.so.3'
    tesseract = ctypes.CDLL(libtesseract_path)

    class _TessBaseAPI(ctypes.Structure):
        pass

    TessBaseAPI = ctypes.POINTER(_TessBaseAPI)

    tesseract.TessBaseAPICreate.restype = TessBaseAPI

    tesseract.TessBaseAPIDelete.restype = None  # void
    tesseract.TessBaseAPIDelete.argtypes = [TessBaseAPI]

    tesseract.TessBaseAPIInit3.argtypes = [TessBaseAPI,
                                           ctypes.c_char_p,
                                           ctypes.c_char_p]

    tesseract.TessBaseAPISetImage.restype = None
    tesseract.TessBaseAPISetImage.argtypes = [TessBaseAPI,
                                              ctypes.c_void_p,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int]

    tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p
    tesseract.TessBaseAPIGetUTF8Text.argtypes = [TessBaseAPI]

    api = tesseract.TessBaseAPICreate()
    rc = tesseract.TessBaseAPIInit3(api, '', 'eng')
    if rc:
        tesseract.TessBaseAPIDelete(api)
        raise RuntimeError('tesseract init failed')

    h, w, d = imcv.shape
    tesseract.TessBaseAPISetImage(api, imcv.ctypes, w, h, d, w * d)
    text = tesseract.TessBaseAPIGetUTF8Text(api)
    return text.strip()
    # return text.strip().decode('utf-8')
