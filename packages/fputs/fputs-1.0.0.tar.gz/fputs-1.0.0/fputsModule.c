#include <Python.h>

static PyObject *PyfputsMethod(PyObject *self, PyObject *args) {
	char *data, *filename = NULL;
	int bytesCopied = -1;

	if(!PyArg_ParseTuple(args, "ss", &data, &filename)) {
		return NULL;
	}

	FILE *fp = fopen(filename, "w");
	bytesCopied = fputs(data, fp);
	fclose(fp);

	return PyLong_FromLong(bytesCopied);
}

// Declares the Method properties and docstring
static PyMethodDef FputsMethods[] = {
	{"fputs", PyfputsMethod, METH_VARARGS, "Python Interface for fputs C library function"},
	{NULL, NULL, 0, NULL}
};

// Declares the Module properties and docstring
static struct PyModuleDef fputsmodule = {
	PyModuleDef_HEAD_INIT,
	"fputs",
	"Python Interface for fputs C library function",
	-1,
	FputsMethods
};

// A function to initialize the module using the struct defined above
PyMODINIT_FUNC PyInit_fputs(void) {
	return PyModule_Create(&fputsmodule);
};
