"""
==CHANGELOG==
* done: packaging as a module
==CHANGELOG==
"""
import os, stat, shutil, time
def _glob(root='', relpath=''):
    for f in os.scandir(os.path.join(root, relpath)):
        fn = os.path.join(relpath, f.name)
        yield fn, f.stat()
        if f.is_dir():
            yield from _glob(root, fn)
def backup(src, dest, fake=False, exclude=[]):
    log = lambda *args: print('%8.1fs  %s' % (time.time() - t0, ' '.join(args)))
    donothing = lambda *args, **kwargs: None
    makedirs = donothing if fake else (lambda d: os.makedirs(d, exist_ok=True))
    copy = donothing if fake else shutil.copyfile
    remove = donothing if fake else lambda f: os.remove(f) if os.path.exists(f) else None
    rmtree = donothing if fake else lambda f: shutil.rmtree(f, onerror=lambda func, path, _: (os.chmod(path, stat.S_IWRITE), func(path))) if os.path.exists(f) else None
    utime = donothing if fake else os.utime
    getlist = lambda path, withexcluded=True: { f[0]: (f[1].st_size, f[1].st_mtime_ns, stat.S_ISDIR(f[1].st_mode)) for f in _glob(path) if withexcluded or all(pattern not in f[0].lower() for pattern in exclude) }
    t0 = time.time()
    src, dest = os.path.abspath(src), os.path.abspath(dest)    
    log('Scanning source...', src)
    SRCFILES = getlist(src, withexcluded=False)     # ex: {'path\to\hello.txt': (1432, 1607205608000000000, False), ...}
    log('Scanning destination...', dest)
    DSTFILES = getlist(dest)
    log('Starting backup...')
    for f in DSTFILES:
        if f not in SRCFILES:
            log('Removing', f)
            if DSTFILES[f][2]:  # dir
                rmtree(os.path.join(dest, f))
            else:
                remove(os.path.join(dest, f))
    for f in SRCFILES:
        if f not in DSTFILES or ((DSTFILES[f] != SRCFILES[f]) and not SRCFILES[f][2]):  # (not in dest) or (size or mtime changed, but not a directory)
            if SRCFILES[f][2]:  # dir
                log('Creating', f)        
                makedirs(os.path.join(dest, f))
            else:
                log('Copying ', f)
                copy(os.path.join(src, f), os.path.join(dest, f))
                utime(os.path.join(dest, f), ns=(SRCFILES[f][1], SRCFILES[f][1]))
    log('Backup finished.')