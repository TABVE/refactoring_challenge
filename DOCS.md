Refactor
--------
Had some issues with setting up poetry, wasted probably around 30 minutes with that. In order to get things working there I used AI and online documentation.

After installing poetry I started with writing tests, making sure everything was pinned. After that I could start refactoring. Happy with the introduction of the `Forcing`and `Reach` classes, but not happy with the numerical part. Unfortunately, I did not manage to get rid of the very large function, we can discuss in the interview how to approach that.

Things that are still not done:
- Mypy error related to type of a patch, I have to look this up
- Mypy error related to type of a tmp_path, I have to look this up





Profiling output
----------------
I've profiled with ~20000 forcings, this is the result.
```
> poetry run python -m cProfile .\src\deltares_model\cli.py
         4024 function calls (3969 primitive calls) in 0.008 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     10/1    0.000    0.000    0.008    0.008 {built-in method builtins.exec}
        1    0.000    0.000    0.008    0.008 cli.py:1(<module>)
     11/3    0.000    0.000    0.008    0.003 <frozen importlib._bootstrap>:1349(_find_and_load)
     11/3    0.000    0.000    0.007    0.002 <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
     11/4    0.000    0.000    0.006    0.001 <frozen importlib._bootstrap>:911(_load_unlocked)
      9/4    0.000    0.000    0.005    0.001 <frozen importlib._bootstrap_external>:993(exec_module)
     23/7    0.000    0.000    0.005    0.001 <frozen importlib._bootstrap>:480(_call_with_frames_removed)
        1    0.000    0.000    0.003    0.003 water_model.py:1(<module>)
       11    0.000    0.000    0.003    0.000 <frozen importlib._bootstrap>:1240(_find_spec)
        9    0.000    0.000    0.003    0.000 <frozen importlib._bootstrap_external>:1066(get_code)
        9    0.000    0.000    0.003    0.000 <frozen importlib._bootstrap_external>:1524(find_spec)
        9    0.000    0.000    0.003    0.000 <frozen importlib._bootstrap_external>:1495(_get_spec)
       27    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1597(find_spec)
      137    0.001    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:96(_path_join)
        9    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1187(get_data)
        1    0.000    0.000    0.001    0.001 utils.py:1(<module>)
        1    0.000    0.000    0.001    0.001 {built-in method builtins.__import__}
        9    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:755(_compile_bytecode)
       51    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:140(_path_stat)
        9    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
       51    0.001    0.000    0.001    0.000 {built-in method nt.stat}
        9    0.001    0.000    0.001    0.000 {built-in method _io.open_code}
       11    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap>:806(module_from_spec)
    39/37    0.001    0.000    0.001    0.000 {built-in method builtins.__build_class__}
```

As you can see it's allready very fast, therefore not chosen to update any functions. I've done this plenty of times.