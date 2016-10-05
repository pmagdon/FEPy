__author__ = 'PAUL MAGDON'

#Copied from SpectralPython
class Image(object):
    '''Import.Image is the common base class for multispectral image objects.'''

    def __init__(self, x=None, metadata=None):
       # self.bands = BandInfo()
        self.set_params(params, metadata)

    def set_params(self, params, metadata):
        try:
            self.nbands = params.nbands
            self.nrows = params.nrows
            self.ncols = params.ncols
            self.dtype = params.dtype

            if not metadata:
                self.metadata = {}
            else:
                self.metadata = metadata
        except:
            raise

    def params(self):
        '''Return an object containing the raster parameters.'''
        class P:
            pass
        p = P()
        p.nbands = self.nbands
        p.nrows = self.nrows
        p.ncols = self.ncols
        p.metadata = self.metadata
        p.dtype = self.dtype

        return p

    def __repr__(self):
        return self.__str__()
