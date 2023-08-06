import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "series.h":
    object PyInit_5de2e12c8194e6ca2989670355a70bf3f28a5d1167116ba5d97b66f033661a0b()
cdef extern from "exceptions.h":
    object PyInit_cef20dc283efc447ee23691a4d0ab067bedf65a64e5ba7936708cd36bf648d91()
cdef extern from "database.h":
    object PyInit_ada920300484dabee75193368c4059a0b745ece3c7301fc14c9e57273360468e()
cdef extern from "chunks.h":
    object PyInit_eb553f88617ca55105a6985882a5232dfcdaa47427a0dcb2c46eee5c254e0fc6()
cdef extern from "iterators.h":
    object PyInit_0db87687fb4b0b1a21a5e7d6eef2d9c0c6d039191d38d18653bcdee105894792()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.series":
        return PyInit_5de2e12c8194e6ca2989670355a70bf3f28a5d1167116ba5d97b66f033661a0b()
    elif name == "tempsdb.exceptions":
        return PyInit_cef20dc283efc447ee23691a4d0ab067bedf65a64e5ba7936708cd36bf648d91()
    elif name == "tempsdb.database":
        return PyInit_ada920300484dabee75193368c4059a0b745ece3c7301fc14c9e57273360468e()
    elif name == "tempsdb.chunks":
        return PyInit_eb553f88617ca55105a6985882a5232dfcdaa47427a0dcb2c46eee5c254e0fc6()
    elif name == "tempsdb.iterators":
        return PyInit_0db87687fb4b0b1a21a5e7d6eef2d9c0c6d039191d38d18653bcdee105894792()


cdef class CythonPackageLoader:
    cdef PyModuleDef* definition
    cdef object def_o
    cdef str name

    def __init__(self, name):
        self.def_o = get_definition_by_name(name)
        self.definition = <PyModuleDef*>self.def_o
        self.name = name
        Py_INCREF(self.def_o)

    def load_module(self, fullname):
        raise ImportError

    def create_module(self, spec):
        if spec.name != self.name:
            raise ImportError()
        return PyModule_FromDefAndSpec(self.definition, spec)

    def exec_module(self, module):
        PyModule_ExecDef(module, self.definition)


class CythonPackageMetaPathFinder:
    def __init__(self, modules_set):
        self.modules_set = modules_set

    def find_module(self, fullname, path):
        if fullname not in self.modules_set:
            return None
        return CythonPackageLoader(fullname)

    def invalidate_caches(self):
        pass

def bootstrap_cython_submodules():
    modules_set = {'tempsdb.exceptions', 'tempsdb.series', 'tempsdb.iterators', 'tempsdb.database', 'tempsdb.chunks'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
