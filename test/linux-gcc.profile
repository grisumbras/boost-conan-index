[settings]
arch=x86_64
build_type=Release
compiler=gcc
compiler.cppstd=17
compiler.libcxx=libstdc++11
compiler.version=13
os=Linux

[options]
boost-*:disabled_libraries=boost_numpy,boost_mpi,boost_mpi_python,boost_graph_parallel,boost_stacktrace_windbg,boost_stacktrace_windbg_cached
