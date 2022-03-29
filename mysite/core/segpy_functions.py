import os

import sys
import traceback
import numpy as np
from segpy.binary_reel_header import BinaryReelHeader
from segpy.datatypes import SegYType
from segpy.field_types import IntFieldMeta
from segpy.header import field
from segpy.reader import create_reader


# Standard SEG-Y does not support 16-bit unsigned integer values in headers.
# This section customises SEG-Y to support them.

class UInt16(int,
            metaclass=IntFieldMeta,
            min_value=0,       # Use the full-range for unsigned
            max_value=65535,   # 16-bit integers
            seg_y_type=SegYType.NNINT16):   # The underlying NNINT16 type is actually read as an unsigned type.
    """16-bit unsigned integer."""
    pass


# Subclass the standard reel header to specialize one of its fields to have a type of UInt16.

class CustomBinaryReelHeader(BinaryReelHeader):

    num_samples = field(
        UInt16, offset=3221, default=0, documentation=
        """Number of samples per data trace. Mandatory for all types of data.
        Note: The sample interval and number of samples in the Binary File Header should be for the primary set of
        seismic data traces in the file."""
    )


def report_segy(in_filename):
    with in_filename as in_file:

        # Create a reader using the CustomBinaryReelHeader format.
        segy_reader = create_reader(
            in_file,
            binary_reel_header_format=CustomBinaryReelHeader)

        print()
        print("Filename:             ", segy_reader.filename)
        print("SEG Y revision:       ", segy_reader.revision)
        print("Number of traces:     ", segy_reader.num_traces())
        print("Data format:          ",
              segy_reader.data_sample_format_description)
        print("Dimensionality:       ", segy_reader.dimensionality)

        try:
            print("Number of CDPs:       ", segy_reader.num_cdps())
        except AttributeError:
            pass

        try:
            print("Number of inlines:    ", segy_reader.num_inlines())
            print("Number of crosslines: ", segy_reader.num_xlines())
        except AttributeError:
            pass

        print("=== BEGIN TEXTUAL REEL HEADER ===")
        for line in segy_reader.textual_reel_header:
            print(line[3:])
        print("=== END TEXTUAL REEL HEADER ===")
        print()
        print("=== BEGIN EXTENDED TEXTUAL HEADER ===")
        print(segy_reader.extended_textual_header)
        print("=== END EXTENDED TEXTUAL_HEADER ===")
def getILXLranges(segy_reader):
    total_inL=segy_reader.num_inlines() #total number of inlines
    total_xL=segy_reader.num_xlines() #total number of xlines
    inL_range = segy_reader.inline_numbers() #inline range
    xL_range = segy_reader.xline_numbers() #xline range
    inL = np.array(inL_range) # Inline numbers
    xL = np.array(xL_range) #xL numbers
    trace_num = segy_reader.num_traces() #Total number of traces
    prevx=(0,0)
    for ix in segy_reader.inline_xline_numbers(): 
        if(ix[0]==68) :  
            print(ix,end=', ')  
        if(prevx[0]==ix[0]) :   
            pass
        else:
            print(ix,end=', ')        
            index = segy_reader.trace_index(ix)
            print(index,end='||')
            prevx=ix
    return inL,xL,trace_num
def getInline(segy_reader,il_no):
    total_xL=segy_reader.num_xlines() #total number of xlines
    xL_range = segy_reader.xline_numbers() #xline range
    inline=[]
    print(il_no,end='************')
    for ix in segy_reader.inline_xline_numbers(): 
        if (ix[0]==il_no):
            index = segy_reader.trace_index(ix)
            samples = segy_reader.trace_samples(index)
            print(ix,end=', ') 
            print(index,end='||')
            print(np.array(samples))
            
            # inline.append(samples)
            # print('yes ',ix, end='::')
    # for xl_no in xL_range:
    #     try:
    #         index = segy_reader.trace_index((il_no,xl_no))
    #         inline = segy_reader.trace_samples(index)
    #         inline.append(inline)
    #         print('yes ',xl_no, end='::')
    #     except:
    #         pass
    return inline