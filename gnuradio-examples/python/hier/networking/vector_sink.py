#!/usr/bin/env python
#
# Copyright 2006 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
from gnuradio.eng_option import eng_option
from optparse import OptionParser

class vector_sink(gr.hier_block2):
    def __init__(self, src, port, pkt_size):
        gr.hier_block2.__init__(self, 
                                "vector_sink",	        # Block type 
                                gr.io_signature(0,0,0), # Input signature
                                gr.io_signature(0,0,0)) # Output signature

        udp = gr.udp_source(gr.sizeof_float, src, port, pkt_size)
        
        self.define_component("src", udp)
        self.define_component("dst", gr.file_sink(gr.sizeof_float, "received.dat"))

        self.connect("src", 0, "dst", 0)	

if __name__ == "__main__":
    parser = OptionParser(option_class=eng_option)
    parser.add_option("", "--src-name", type="string", default="localhost",
                      help="local host name (domain name or IP address)")
    parser.add_option("", "--src-port", type="int", default=65500,
                      help="port value to listen to for connection")
    parser.add_option("", "--packet-size", type="int", default=1471,
                      help="packet size.")
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help()
        raise SystemExit, 1
    
    # Create an instance of a hierarchical block
    top_block = vector_sink(options.src_name, options.src_port, options.packet_size)
    
    # Create an instance of a runtime, passing it the top block
    runtime = gr.runtime(top_block)
    
    try:    
        # Run forever
        runtime.run()
    except KeyboardInterrupt:
        # Ctrl-C exits
        pass
    