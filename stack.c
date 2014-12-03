#include <Python.h>

typedef struct StackElement Elem;

struct StackElement {
    int val;
    Elem* next;
};

typedef struct {
    PyObject_HEAD
    Elem *top;
} Stack;


static void
Stack_dealloc(Stack *self) {
    Elem *current, *next;

    current = self->top;
    while (current) {
        next = current->next;
        free(current);
        current = next;
    }
    self->top = NULL;

    PyObject_Del(self);
}


PyObject *
Stack_push(Stack *self, PyObject *args) {
    int val;
    Elem *oldtop, *newtop;

    if (!(PyArg_ParseTuple(args, "i", &val))) {
        return NULL;
    }
    
    oldtop = self->top;
    newtop = (Elem*)malloc(sizeof(Elem));
    newtop->val = val;
    newtop->next = oldtop;
    
    self->top = newtop;

    Py_INCREF(Py_None); 
    return Py_None;
}

PyObject *
Stack_pop(Stack *self, PyObject *args) {
    if (self->top == NULL) {
        PyErr_SetString(PyExc_IndexError, "Empty stack");
        return NULL;
    }
    int val = self->top->val;
    Elem *oldtop, *newtop;
    oldtop = self->top;
    newtop = self->top->next;
    self->top = newtop;
    free(oldtop);
    return Py_BuildValue("i", val);
}
    
PyObject *
Stack_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {
    Stack *self;
    self = (Stack *)type->tp_alloc(type, 0);
    return (PyObject *)self;
}

static int
Stack_init (Stack *self, PyObject *args) {
    self->top = NULL;
    return 0;
}
    
static PyMethodDef Stack_methods[] = {
    {"push", (PyCFunction)Stack_push, METH_VARARGS, "Push to stack"},
    {"pop",  (PyCFunction)Stack_pop, METH_NOARGS, "Pop from stack"},
    {NULL}  /* Sentinel */
};

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

static PyTypeObject StackType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "stack.Stack",             /*tp_name*/
    sizeof(Stack),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)Stack_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "Stack object",            /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,		                   /* tp_iter */
    0,		                   /* tp_iternext */
    Stack_methods,             /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Stack_init,      /* tp_init */
    0,                         /* tp_alloc */
    Stack_new,                 /* tp_new */
};



PyMODINIT_FUNC
initstack(void) {
   // (void) Py_InitModule("stack", module_methods);  // not allows to define type

    PyObject* m;

    if (PyType_Ready(&StackType) < 0)
        return;

    m = Py_InitModule3("stack", module_methods,
                       "Example module that creates linked list based stack.");

    if (m == NULL)
      return;

    Py_INCREF(&StackType);  //type is just an object, so you shall increment refcounter to it
    PyModule_AddObject(m, "Stack", (PyObject *)&StackType);
}
