# diskbackup

**diskbackup** is a very simple backup tool. Main features:

* The directory `dest` will be a clone of `src` (and its subdirectories). New files or modified files will be copied, and files in `dest` which are not in `src` will be removed.

* The backup is incremental: only new or modified files will be copied. `filename` + `file size` + `modification time` are used to do the comparison between source and destination files.

* Supports exclude patterns

* Follows symbolic links

* Works when the `dest` is a network shared folder (tested on Windows)

* The source code is ~50 lines of code: you don't even need to scroll in your text editor to read the code, it takes only one page ;)

## Installation and usage

You need Python 3.6+, and to do:

    pip install diskbackup

(An alternative installation method is to just copy the single file `diskbackup.py` where you want to use it.)

This is how to use it:

    from diskbackup import backup
    backup(src=r'd:\docs', dest=r'i:\docs')                  
    backup(src=r'd:\docs', dest=r'i:\docs', fake=True)   # fake run, no change on destination
    backup(src=r'd:\docs', dest=r'i:\docs', exclude=[r'excluded_dir\', '.mp4'])

## Author

Joseph Ernest

## License

MIT