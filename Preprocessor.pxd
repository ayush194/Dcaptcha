# distutils: sources = Segmenter.cpp

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "Segmenter.cpp":
	pass

cdef extern from "Segmenter.h":
	cdef cppclass Segmenter:
		vector[int] num_chars
		Segmenter() except +
		vector[vector[float]] segment(vector[string])