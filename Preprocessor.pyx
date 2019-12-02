# distutils: language = c++

from Preprocessor cimport Segmenter

from libcpp.vector cimport vector
from libcpp.string cimport string

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.

cdef class Preprocessor:
	cdef Segmenter c_segmenter  # Hold a C++ instance which we're wrapping

	def __cinit__(self):
		self.c_segmenter = Segmenter()

	def segment(self, vector[string] filename):
		return self.c_segmenter.segment(filename)

	# Attribute access
	@property
	def num_chars(self):
		return self.c_segmenter.num_chars
	@num_chars.setter
	def num_chars(self, vector[int] num_chars):
		self.c_segmenter.num_chars = num_chars
