import ctypes

ssl = ctypes.cdll.LoadLibrary("/usr/lib64/libssl3.so")

print(ssl.SSL_BadCertHook)

# nm -D ./libMyLib.so