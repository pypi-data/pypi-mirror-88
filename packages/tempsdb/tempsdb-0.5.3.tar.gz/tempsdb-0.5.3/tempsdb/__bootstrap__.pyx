import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "series.h":
    object PyInit_7afb288fca928067f93f40fa944309888e2f0152d2e87451808e0c30bf281a97()
cdef extern from "chunks/base.h":
    object PyInit_99422333cd8708efb4391a9e0b7fc168564601a038dcea1f15a5cf47b7ceae80()
cdef extern from "chunks/maker.h":
    object PyInit_60b2b63f90c637bb1e935d0d37237d549d0686fcb9d1769976a23853e90d1144()
cdef extern from "chunks/normal.h":
    object PyInit_97da121c18fe7573f283c2007e24dbc047a65fb276b4cbe88678457f9ddc6783()
cdef extern from "chunks/gzip.h":
    object PyInit_d1d80be7109a475e475eed08e0303adfe7c74206f22e75dc755fd748e3077328()
cdef extern from "chunks/direct.h":
    object PyInit_0a2b4481d701c22e5537a08bfcb2c60c0be69134d30a96226ee3048887c298b2()
cdef extern from "exceptions.h":
    object PyInit_5f2ffe889c0ab03ec31d214c729fcb92235cc04154efb3e38c9eb0e86fac867c()
cdef extern from "database.h":
    object PyInit_120c43af2a8663eff400d26cab2c96631053edf180f1370fe86bdb94e0959f36()
cdef extern from "varlen.h":
    object PyInit_7deb7099d3cc374a1b95f98a4a2a4c2e045119619209445be28bf3f9da13b648()
cdef extern from "iterators.h":
    object PyInit_c6c8b0a272a1d9c80107b85270d4666d54f5bb90f7ba8289e46997ff2ca86e5d()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.series":
        return PyInit_7afb288fca928067f93f40fa944309888e2f0152d2e87451808e0c30bf281a97()
    elif name == "tempsdb.chunks.base":
        return PyInit_99422333cd8708efb4391a9e0b7fc168564601a038dcea1f15a5cf47b7ceae80()
    elif name == "tempsdb.chunks.maker":
        return PyInit_60b2b63f90c637bb1e935d0d37237d549d0686fcb9d1769976a23853e90d1144()
    elif name == "tempsdb.chunks.normal":
        return PyInit_97da121c18fe7573f283c2007e24dbc047a65fb276b4cbe88678457f9ddc6783()
    elif name == "tempsdb.chunks.gzip":
        return PyInit_d1d80be7109a475e475eed08e0303adfe7c74206f22e75dc755fd748e3077328()
    elif name == "tempsdb.chunks.direct":
        return PyInit_0a2b4481d701c22e5537a08bfcb2c60c0be69134d30a96226ee3048887c298b2()
    elif name == "tempsdb.exceptions":
        return PyInit_5f2ffe889c0ab03ec31d214c729fcb92235cc04154efb3e38c9eb0e86fac867c()
    elif name == "tempsdb.database":
        return PyInit_120c43af2a8663eff400d26cab2c96631053edf180f1370fe86bdb94e0959f36()
    elif name == "tempsdb.varlen":
        return PyInit_7deb7099d3cc374a1b95f98a4a2a4c2e045119619209445be28bf3f9da13b648()
    elif name == "tempsdb.iterators":
        return PyInit_c6c8b0a272a1d9c80107b85270d4666d54f5bb90f7ba8289e46997ff2ca86e5d()


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
    modules_set = {'tempsdb.iterators', 'tempsdb.chunks.normal', 'tempsdb.series', 'tempsdb.varlen', 'tempsdb.chunks.maker', 'tempsdb.chunks.base', 'tempsdb.exceptions', 'tempsdb.database', 'tempsdb.chunks.direct', 'tempsdb.chunks.gzip'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
