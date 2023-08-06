import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "basics.h":
    object PyInit_3e1fb4a56016b6459bd70747a392b91a1a0af0fe117ede8a42a4caf1e8009c0d()
cdef extern from "quadtrees.h":
    object PyInit_c02489d6d561738a531357a95b81e505c94e219c57eba09059277d501af5a055()

cdef object get_definition_by_name(str name):
    if name == "line_intersect_2d.basics":
        return PyInit_3e1fb4a56016b6459bd70747a392b91a1a0af0fe117ede8a42a4caf1e8009c0d()
    elif name == "line_intersect_2d.quadtrees":
        return PyInit_c02489d6d561738a531357a95b81e505c94e219c57eba09059277d501af5a055()


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
    modules_set = {'line_intersect_2d.quadtrees', 'line_intersect_2d.basics'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
