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
    object PyInit_12af15024bbafda8e53491d0b6d5e3cc0352b6a59823c4edb73d134ffe1128a4()
cdef extern from "chunks/maker.h":
    object PyInit_60b2b63f90c637bb1e935d0d37237d549d0686fcb9d1769976a23853e90d1144()
cdef extern from "chunks/normal.h":
    object PyInit_97da121c18fe7573f283c2007e24dbc047a65fb276b4cbe88678457f9ddc6783()
cdef extern from "chunks/gzip.h":
    object PyInit_b136eb0884c2cffced7753c0fb893ba3312ae346074f82e9f630b8e0c968aea9()
cdef extern from "chunks/direct.h":
    object PyInit_0a2b4481d701c22e5537a08bfcb2c60c0be69134d30a96226ee3048887c298b2()
cdef extern from "exceptions.h":
    object PyInit_5f2ffe889c0ab03ec31d214c729fcb92235cc04154efb3e38c9eb0e86fac867c()
cdef extern from "database.h":
    object PyInit_e76ce57daeb8b4d5fc5375653d9ccff9b31812beacd0260f1813c78b14713d45()
cdef extern from "varlen.h":
    object PyInit_3a8bd2a833f1a03434391bbff5428dfb72be8ec5f691c3743ada176773952ee0()
cdef extern from "iterators.h":
    object PyInit_c6c8b0a272a1d9c80107b85270d4666d54f5bb90f7ba8289e46997ff2ca86e5d()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.series":
        return PyInit_7afb288fca928067f93f40fa944309888e2f0152d2e87451808e0c30bf281a97()
    elif name == "tempsdb.chunks.base":
        return PyInit_12af15024bbafda8e53491d0b6d5e3cc0352b6a59823c4edb73d134ffe1128a4()
    elif name == "tempsdb.chunks.maker":
        return PyInit_60b2b63f90c637bb1e935d0d37237d549d0686fcb9d1769976a23853e90d1144()
    elif name == "tempsdb.chunks.normal":
        return PyInit_97da121c18fe7573f283c2007e24dbc047a65fb276b4cbe88678457f9ddc6783()
    elif name == "tempsdb.chunks.gzip":
        return PyInit_b136eb0884c2cffced7753c0fb893ba3312ae346074f82e9f630b8e0c968aea9()
    elif name == "tempsdb.chunks.direct":
        return PyInit_0a2b4481d701c22e5537a08bfcb2c60c0be69134d30a96226ee3048887c298b2()
    elif name == "tempsdb.exceptions":
        return PyInit_5f2ffe889c0ab03ec31d214c729fcb92235cc04154efb3e38c9eb0e86fac867c()
    elif name == "tempsdb.database":
        return PyInit_e76ce57daeb8b4d5fc5375653d9ccff9b31812beacd0260f1813c78b14713d45()
    elif name == "tempsdb.varlen":
        return PyInit_3a8bd2a833f1a03434391bbff5428dfb72be8ec5f691c3743ada176773952ee0()
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
    modules_set = {'tempsdb.series', 'tempsdb.chunks.direct', 'tempsdb.chunks.gzip', 'tempsdb.iterators', 'tempsdb.chunks.base', 'tempsdb.chunks.normal', 'tempsdb.exceptions', 'tempsdb.varlen', 'tempsdb.database', 'tempsdb.chunks.maker'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
