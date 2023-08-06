import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "series.h":
    object PyInit_7d0fecfc9808752467fd88d2737cfbc1650ae9deff9f21a42120969441cdf359()
cdef extern from "exceptions.h":
    object PyInit_5f2ffe889c0ab03ec31d214c729fcb92235cc04154efb3e38c9eb0e86fac867c()
cdef extern from "database.h":
    object PyInit_a9acd7511c3d2f9f2383069e70dd7a2d505db8948a415a8fa9711244565087f7()
cdef extern from "varlen.h":
    object PyInit_38aa320e0da0cc0e22310fb3265cf4ee24a1441f605d55a248b4f11a8f61ddfb()
cdef extern from "chunks.h":
    object PyInit_d4f67dcfa7b4d08b98b9d5d3af2efd695ea72fa41d633e6d0e31c3aa29eda318()
cdef extern from "iterators.h":
    object PyInit_fcef35070ee4a699b63429732f01059b9ff3fbefe3517d0de1fd24d46351eca6()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.series":
        return PyInit_7d0fecfc9808752467fd88d2737cfbc1650ae9deff9f21a42120969441cdf359()
    elif name == "tempsdb.exceptions":
        return PyInit_5f2ffe889c0ab03ec31d214c729fcb92235cc04154efb3e38c9eb0e86fac867c()
    elif name == "tempsdb.database":
        return PyInit_a9acd7511c3d2f9f2383069e70dd7a2d505db8948a415a8fa9711244565087f7()
    elif name == "tempsdb.varlen":
        return PyInit_38aa320e0da0cc0e22310fb3265cf4ee24a1441f605d55a248b4f11a8f61ddfb()
    elif name == "tempsdb.chunks":
        return PyInit_d4f67dcfa7b4d08b98b9d5d3af2efd695ea72fa41d633e6d0e31c3aa29eda318()
    elif name == "tempsdb.iterators":
        return PyInit_fcef35070ee4a699b63429732f01059b9ff3fbefe3517d0de1fd24d46351eca6()


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
    modules_set = {'tempsdb.varlen', 'tempsdb.exceptions', 'tempsdb.iterators', 'tempsdb.database', 'tempsdb.chunks', 'tempsdb.series'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
