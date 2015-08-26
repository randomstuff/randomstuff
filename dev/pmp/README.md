# Poor man's profiler

These are simple wrapper scripts which can be used to generate (or exploit)
sample profiles of applications based on the
[poor man's profiler](http://poormansprofiler.org/).

## The tools

* <b>pmp-gdb</b> uses GDB to generate backtraces.

* <b>pmp-elfutil</b>, uses [elfutils](https://fedorahosted.org/elfutils/) stack.
  This seems to be much faster.

## Other tools

Visualisation tools:

* [FlameGraph](http://www.brendangregg.com/flamegraphs.html)

Alternative solutions:

* linux perf
* systemtap
* oprofile
* dtrace
