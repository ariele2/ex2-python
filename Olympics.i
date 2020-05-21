%module Olympics
%include "typemaps.i"
%include "Olympics.h"
%{
#include "Olympics.h"
typedef struct olympics* Olympics;
%}

Olympics OlympicsCreate();

TODO : insert more code here. add missing functions.

void OlympicsDestroy(Olympics o);
