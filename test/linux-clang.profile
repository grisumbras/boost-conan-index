[settings]
arch=x86_64
build_type=Release
compiler=clang
compiler.cppstd=17
compiler.libcxx=libstdc++11
compiler.version=18
os=Linux

[options]
boost-*:disabled_libraries=boost_numpy,boost_mpi,boost_mpi_python,boost_graph_parallel,boost_stacktrace_backtrace,boost_stacktrace_windbg,boost_stacktrace_windbg_cached

[conf]
tools.build:compiler_executables={"cpp": "clang++-18", "c": "clang-18"}
