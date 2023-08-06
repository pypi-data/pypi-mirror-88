import os
from itertools import islice
import numpy as np

from nextnanopy.utils.datasets import Variable, Coord
from nextnanopy.utils.mycollections import DictList
from nextnanopy.utils.formatting import best_str_to_name_unit
from nextnanopy.utils.misc import get_filename, message_decorator
from nextnanopy import defaults

import pyvista as pv

_msgs = defaults.messages['load_output']
load_message = lambda method: message_decorator(method, init_msg=_msgs[0], end_msg=_msgs[1])


class Output(object):

    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.metadata = {}
        self.coords = DictList()
        self.variables = DictList()

    @property
    def folder(self):
        return os.path.split(self.fullpath)[0]

    @property
    def filename_only(self):
        return get_filename(self.fullpath, ext=False)

    @property
    def filename(self):
        return get_filename(self.fullpath, ext=True)

    @property
    def extension(self):
        return os.path.splitext(self.fullpath)[-1]

    @property
    def data(self):
        dl = DictList()
        dl.update(self.coords)
        dl.update(self.variables)
        return dl

    @load_message
    def load(self):
        pass

    def get_coord(self, key):
        return self.coords[key]

    def get_variable(self, key):
        return self.variables[key]

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, item, value):
        if item in self.coords.keys():
            self.coords[item] = value
        if item in self.variables.keys():
            self.variables[item] = value

    def __delitem__(self, item):
        if item in self.coords.keys():
            del self.coords[item]
        if item in self.variables.keys():
            del self.variables[item]

    def __repr__(self):
        out = []
        out.append(f'{self.__class__.__name__}')
        out.append(f'fullpath: {self.fullpath}')
        out.append(f'Coordinates: {len(self.coords)} datasets')
        for key, coord in self.coords.items():
            out.append(f'\t{str(coord)}')
        out.append(f'Variables: {len(self.variables)} datasets')
        for key, var in self.variables.items():
            out.append(f'\t{str(var)}')
        out = '\n'.join(out)
        return out

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        try:
            result = self.data.__getitem__(self._iter_index)
        except (IndexError, KeyError):
            raise StopIteration
        self._iter_index += 1
        return result


class DataFileTemplate(Output):
    """
        This class stores the data from any kind of nextnano data files with the
        same structure.
        The stored data contains coordinates (.coords) and dependent variables (.variables).
        Each coordinate or variable would contain attributes like name, unit and value.
        For more information, see their specific documentation.

        The initialization of the class will execute the load method.

        ...

        Parameters
        ----------
        fullpath : str
            path to the file.


        Attributes
        ----------
        fullpath : str
            path to the file (default: None)
        coords : DictList
            Coord objects (default: DictList())
        variables : DictList
            Variable objects (default: DictList())
        data : DictList
            coords and variables together
        metadata : dict
            extra information
        filename : str
            name with the file extension
        filename_only :
            name without the file extension
        extension : str
            file extension
        folder : str
            folder of the fullpath
        product : str
            flag about nextnano product to help to find the best loading routine


        Methods
        -------
        load(fullpath)
            load a data file

        get_coord(name)
            equivalent to self.coords[name]

        get_variable(name)
            equivalent to self.variables[name]

    """

    def __init__(self, fullpath, product=None):
        super().__init__(fullpath)
        self.product = product
        self.load()

    @load_message
    def load(self):
        """
        Find the loader and update the stored information with the loaded data
        """
        loader = self.get_loader()
        df = loader(self.fullpath)
        self.update_with_datafile(df)
        del df

    def update_with_datafile(self, datafile):
        """
        Copy .metadata, .coords and .variables of the specified datafile
        Copy other attributes like .vtk if there is any.

        Parameters
        ----------
        datafile : nextnano.outputs.DataFileTemplate object
        """

        self.metadata.update(datafile.metadata)
        self.coords.update(datafile.coords)
        self.variables.update(datafile.variables)
        if hasattr(datafile, 'vtk'):
            self.vtk = datafile.vtk

    def get_loader(self):
        pass


class DataFile(DataFileTemplate):
    def __init__(self, fullpath, product=None):
        super().__init__(fullpath, product=product)

    def get_loader(self):
        if self.product:
            loader = defaults.get_DataFile(self.product)
        else:
            print('[Warning] nextnano product is not specified: nextnano++, nextnano3, nextnano.NEGF or nextnano.MSB')
            print('[Warning] Autosearching for the best loading method. Note: The result may not be correct')
            loader = self.find_loader()
        return loader

    def find_loader(self):
        from nextnanopy.nnp.outputs import DataFile as DataFile_nnp
        from nextnanopy.nn3.outputs import DataFile as DataFile_nn3
        from nextnanopy.negf.outputs import DataFile as DataFile_negf
        from nextnanopy.msb.outputs import DataFile as DataFile_msb

        Dats = [DataFile_nn3, DataFile_nnp, DataFile_negf, DataFile_msb]
        for Dati in Dats:
            try:
                df = Dati(self.fullpath)
                if '' in df.variables.keys():
                    continue
                else:
                    break
            except:
                pass
        loader = Dati
        return loader


class AvsAscii(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    @property
    def fld(self):
        filename = self.filename_only + '.fld'
        return os.path.join(self.folder, filename)

    def load(self):
        self.load_raw_metadata()
        self.load_metadata()
        self.load_variables()
        self.load_coords()

    def load_raw_metadata(self):
        info = []
        with open(self.fld, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                line = line.strip()
                try:
                    float(line)
                    break
                except:
                    if line == '':
                        continue
                    if line[0] != '#':
                        info.append(line)
        return info

    def load_metadata(self):
        info = self.load_raw_metadata()
        key_int = ['ndim', 'dim1', 'dim2', 'dim3', 'nspace', 'veclen']
        key_str = ['data', 'field']
        metadata = {}
        metadata['labels'] = []
        metadata['units'] = []
        metadata['variables'] = []
        metadata['coords'] = []
        metadata['dims'] = []
        for line in info:
            key, value = line.split(maxsplit=1)
            if value[0] == '=':
                value = value.replace('=', '')
                value = value.strip()
                if key in key_int:
                    value = int(value)
                    metadata[key] = value
                elif key == 'label':
                    labels = value.split()
                    for label in labels:
                        label, unit = best_str_to_name_unit(label, default_unit=None)
                        metadata['labels'].append(label)
                        metadata['units'].append(unit)
                else:
                    value = str(value)
                    metadata[key] = value

                if key[:3] == 'dim':
                    metadata['dims'].append(metadata[key])

            else:
                if key == 'variable':
                    vm = values_metadata(line)
                    vm['file'] = os.path.join(self.folder, vm['file'])
                    vm['size'] = np.prod(metadata['dims'])
                    metadata['variables'].append(vm)
                elif key == 'coord':
                    vm = values_metadata(line)
                    vm['file'] = os.path.join(self.folder, vm['file'])
                    num = vm['num']
                    vm['size'] = metadata[f'dim{num}']
                    metadata['coords'].append(vm)

        self.metadata = metadata
        return metadata

    def load_variables(self):
        meta = self.metadata
        variables = DictList()
        for vmeta, label, unit in zip(meta['variables'], meta['labels'], meta['units']):
            values = load_values(file=vmeta['file'],
                                 filetype=vmeta['filetype'],
                                 skip=vmeta['skip'],
                                 offset=vmeta['offset'],
                                 stride=vmeta['stride'],
                                 size=vmeta['size'])
            values = reshape_values(values, *meta['dims'])
            var = Variable(name=label, value=values, unit=unit, metadata=vmeta)
            variables[var.name] = var
        self.variables = variables
        return variables

    def load_coords(self):
        meta = self.metadata
        coords = DictList()
        for vmeta in meta['coords']:
            values = load_values(file=vmeta['file'],
                                 filetype=vmeta['filetype'],
                                 skip=vmeta['skip'],
                                 offset=vmeta['offset'],
                                 stride=vmeta['stride'],
                                 size=vmeta['size'])
            ax = coord_axis(vmeta['num'])
            unit = 'nm'
            var = Coord(name=ax, value=values, unit=unit, dim=vmeta['num'] - 1, metadata=vmeta)
            coords[var.name] = var
        self.coords = coords
        return coords


class Vtk(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.vtk = pv.read(self.fullpath)
        self.load_coords()
        self.load_variables()

    def load_coords(self):
        for i, coord in enumerate(['x', 'y', 'z']):
            if not hasattr(self.vtk, coord):
                continue
            value = getattr(self.vtk, coord)
            if value.size == 1:
                continue
            self.coords[coord] = Coord(name=coord, value=value, unit=None, dim=i)

    def load_variables(self):
        for _name in self.vtk.array_names:
            name, unit = best_str_to_name_unit(_name, default_unit=None)
            value = np.array(self.vtk[_name]).reshape(self.vtk.dimensions, order='F').squeeze()
            self.variables[name] = Variable(name=name, value=value, unit=unit)


def coord_axis(dim):
    dim = str(dim)
    axes = {'1': 'x', '2': 'y', '3': 'z'}
    return axes[dim]


def values_metadata(line):
    """ Return a dict for: kind, num, file, filetype, skip, offset, stride"""
    metadata = {}
    kind, num, rest = line.split(maxsplit=2)
    metadata['kind'] = kind
    metadata['num'] = int(num)
    raw_rest = rest.split('=')
    raw_rest = [r.strip().split() for r in raw_rest]
    rest = []
    for ri in raw_rest:
        rest.extend(ri)
    keys = rest[0::2]
    values = rest[1::2]
    for key, value in zip(keys, values):
        key = key.strip()
        value = value.strip()
        if key in ['num', 'skip', 'offset', 'stride']:
            value = int(value)
        metadata[key] = value
    return metadata


def load_values(file, filetype='ascii', skip=0, offset=0, stride=1, size=None):
    """ Return flat array of floating values """
    stop = skip + size if size != None else None
    with open(file, 'r') as f:
        lines = islice(f, skip, stop, 1)
        values = [line.replace('\n', '').strip().split()[offset] for line in lines]
    return np.array(values, dtype=float)


def reshape_values(values, *dims):
    dims = np.flip(dims)
    shape = tuple([dim for dim in dims])
    values = np.reshape(values, shape)
    return np.transpose(values)
