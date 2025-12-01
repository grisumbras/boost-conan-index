[settings]
arch=armv8
build_type=Release
compiler=gcc
compiler.cppstd=17
compiler.libcxx=libstdc++11
compiler.version=15
os=Macos

[options]
boost-*:disabled_libraries=boost_numpy,boost_mpi,boost_mpi_python,boost_graph_parallel,boost_stacktrace_backtrace,boost_stacktrace_from_exception,boost_stacktrace_windbg,boost_stacktrace_windbg_cached

[conf]
tools.build:compiler_executables={"cpp": "g++-15", "c": "gcc-15"}
boost-*:tools.build:defines=["_GNU_SOURCE"]
&:tools.build:defines=["_GNU_SOURCE"]
