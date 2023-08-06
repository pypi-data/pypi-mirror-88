import numpy as _np


class Field(object):
    """
    Base class used for common writing procedures for BDSIM field format.

    This does not support arbitrary loop ordering - only the originally intended
    xyzt.
    """
    def __init__(self, array=_np.array([]), columns=[], flip=True, doublePrecision=False):
        self.data            = array
        self.columns         = columns
        self.header          = {}
        self.flip            = flip
        self.doublePrecision = doublePrecision       

    def Write(self, fileName):
        f = open(fileName, 'w')
        for key,value in self.header.items():
            f.write(str(key)+'> '+ str(value) + '\n')

        if self.doublePrecision:
            colStrings = ['%23s' % s for s in self.columns]
        else:
            colStrings = ['%14s' % s for s in self.columns]
        colStrings[0] = colStrings[0].strip() # don't pad the first column title
        # a '!' denotes the column header line
        f.write('! '+ '\t'.join(colStrings)+'\n')
        
        # flatten all but last dimension - 3 field components
        nvalues = _np.shape(self.data)[-1] # number of values in last dimension

        if self.flip:
            # [x,y,z,t,values] -> [t,z,y,x,values] for 4D
            # [x,y,z,values]   -> [z,y,x,values]   for 3D
            # [x,y,values]     -> [y,x,values]     for 2D
            # [x,values]       -> [x,values]       for 1D
            if (self.data.ndim == 2):
                pass # do nothin for 1D
            inds = list(range(self.data.ndim))       # indices for dimension [0,1,2] etc
            # keep the last value the same but reverse all indices before then
            inds[:(self.data.ndim - 1)] = reversed(inds[:(self.data.ndim - 1)])
            datal = _np.transpose(self.data, inds)
        else:
            datal = self.data

        datal = datal.reshape(-1,nvalues)
        for value in datal:
            if self.doublePrecision:
                strings   = ['%.16E' % x for x in value]
                stringsFW = ['%23s' % s for s in strings]
            else:
                strings   = ['%.8E' % x for x in value]
                stringsFW = ['%14s' % s for s in strings]
            f.write('\t'.join(stringsFW) + '\n')

        f.close()


class Field1D(Field):
    """
    Utility class to write a 1D field map array to BDSIM field format.

    The array supplied should be 2 dimensional. Dimensions are:
    (x,value) where value has 4 elements [x,fx,fy,fz]. So a 120 long
    array would have np.shape of (120,4).
    
    This can be used for both electric and magnetic fields.

    Example::
    
    >>> a = Field1D(data)
    >>> a.Write('outputFileName.dat')

    """
    def __init__(self, data, doublePrecision=False, column='X'):
        columns = [column,'Fx','Fy','Fz']
        super(Field1D, self).__init__(data,columns,doublePrecision=doublePrecision)
        self.header[column.lower() + 'min'] = _np.min(self.data[:,0])
        self.header[column.lower() + 'max'] = _np.max(self.data[:,0])
        self.header['n' + column.lower()]   = _np.shape(self.data)[0]

class Field2D(Field):
    """
    Utility class to write a 2D field map array to BDSIM field format.

    The array supplied should be 3 dimensional. Dimensions are:
    (x,y,value) where value has 5 elements [x,y,fx,fy,fz].  So a 100x50 (x,y)
    grid would have np.shape of (100,50,5).

    Example::
    
    >>> a = Field2D(data) # data is a prepared array
    >>> a.Write('outputFileName.dat')

    The 'flip' boolean allows an array with (y,x,value) dimension order
    to be written as (x,y,value).

    The 'doublePrecision' boolean controls whether the field and spatial
    values are written to 16 s.f. (True) or 8 s.f. (False - default).

    """
    def __init__(self, data, flip=True, doublePrecision=False, firstColumn='X', secondColumn='Y'):
        columns = [firstColumn, secondColumn, 'Fx', 'Fy', 'Fz']
        super(Field2D, self).__init__(data,columns,flip,doublePrecision)
        inds = [0,1] if flip else [1,0]
        fcl = firstColumn.lower()
        scl = secondColumn.lower()
        self.header[fcl+'min'] = _np.min(self.data[:,:,0])
        self.header[fcl+'max'] = _np.max(self.data[:,:,0])
        self.header['n'+fcl]   = _np.shape(self.data)[inds[0]]
        self.header[scl+'min'] = _np.min(self.data[:,:,1])
        self.header[scl+'max'] = _np.max(self.data[:,:,1])
        self.header['n'+scl]   = _np.shape(self.data)[inds[1]]

class Field3D(Field):
    """
    Utility class to write a 3D field map array to BDSIM field format.

    The array supplied should be 4 dimensional. Dimensions are:
    (x,y,z,value) where value has 6 elements [x,y,z,fx,fy,fz].  So a 100x50x30 
    (x,y,z) grid would have np.shape of (100,50,30,6).
    
    Example::
    
    >>> a = Field3D(data) # data is a prepared array
    >>> a.Write('outputFileName.dat')

    The 'flip' boolean allows an array with (z,y,x,value) dimension order to
    be written as (x,y,z,value).

    The 'doublePrecision' boolean controls whether the field and spatial
    values are written to 16 s.f. (True) or 8 s.f. (False - default).

    """
    def __init__(self, data, flip=True, doublePrecision=False, firstColumn='X', secondColumn='Y', thirdColumn='Z'):
        columns = [firstColumn,secondColumn,thirdColumn,'Fx','Fy','Fz']
        super(Field3D, self).__init__(data,columns,flip,doublePrecision)
        inds = [0,1,2] if flip else [2,1,0]
        fcl = firstColumn.lower()
        scl = secondColumn.lower()
        tcl = thirdColumn.lower()
        self.header[fcl+'min'] = _np.min(self.data[:,:,:,0])
        self.header[fcl+'max'] = _np.max(self.data[:,:,:,0])
        self.header['n'+fcl]   = _np.shape(self.data)[inds[0]]
        self.header[scl+'min'] = _np.min(self.data[:,:,:,1])
        self.header[scl+'max'] = _np.max(self.data[:,:,:,1])
        self.header['n'+scl]   = _np.shape(self.data)[inds[1]]
        self.header[tcl+'min'] = _np.min(self.data[:,:,:,2])
        self.header[tcl+'max'] = _np.max(self.data[:,:,:,2])
        self.header['n'+tcl]   = _np.shape(self.data)[inds[2]]

class Field4D(Field):
    """
    Utility class to write a 4D field map array to BDSIM field format.

    The array supplied should be 5 dimensional. Dimensions are:
    (t,y,z,x,value) where value has 7 elements [x,y,z,t,fx,fy,fz]. So a 100x50x30x10
    (x,y,z,t) grid would have np.shape of (10,30,50,100,7).
    
    Example::
    
    >>> a = Field4D(data) # data is a prepared array
    >>> a.Write('outputFileName.dat')

    The 'flip' boolean allows an array with (t,z,y,x,value) dimension order to
    be written as (x,y,z,t,value).

    The 'doublePrecision' boolean controls whether the field and spatial
    values are written to 16 s.f. (True) or 8 s.f. (False - default).

    """
    def __init__(self, data, flip=True, doublePrecision=False):
        columns = ['X','Y','Z','T','Fx','Fy','Fz']
        super(Field4D, self).__init__(data,columns,flip,doublePrecision)
        inds = [0,1,2,3] if flip else [3,2,1,0]
        self.header['xmin'] = _np.min(self.data[:,:,:,:,0])
        self.header['xmax'] = _np.max(self.data[:,:,:,:,0])
        self.header['nx']   = _np.shape(self.data)[inds[0]]
        self.header['ymin'] = _np.min(self.data[:,:,:,:,1])
        self.header['ymax'] = _np.max(self.data[:,:,:,:,1])
        self.header['ny']   = _np.shape(self.data)[inds[1]]
        self.header['zmin'] = _np.min(self.data[:,:,:,:,2])
        self.header['zmax'] = _np.max(self.data[:,:,:,:,2])
        self.header['nz']   = _np.shape(self.data)[inds[2]]
        self.header['tmin'] = _np.min(self.data[:,:,:,:,3])
        self.header['tmax'] = _np.max(self.data[:,:,:,:,3])
        self.header['nt']   = _np.shape(self.data)[inds[3]]
