#!/usr/bin/env python
# coding: utf-8

# # Juno
# A file watching daemon for Jupyter Notebooks.

# In[1]:


import os
import re
import sys
import argparse
import logging
import signal
import asyncio
import subprocess as sp


# In[ ]:


_root = None


# In[ ]:


def kill_process( process ):
    process.send_signal( signal.SIGINT )
    process.send_signal( signal.SIGINT )

    # tasks = [ 
    #   task 
    #   for task in asyncio.all_tasks() 
    #   if task is not asyncio.current_task() 
    # ]

    # for task in tasks:
    #   task.cancel()

    sys.exit( 0 )


# In[ ]:


def compile( file ):
    sp.run( [ 'jupyter', 'nbconvert', '--to', 'script', file ] )
    print( f'Compiled {file}' )
    


# In[ ]:


def listen( read, write, handler = None):
    pattern = re.compile( 'Saving file at (.+\.ipynb)' )
    for line in read:
        line = line.decode( 'utf-8' )
        print( line, file = write, flush = True )
        match = pattern.search( line )
        if match is not None:
            file = match.group( 1 )[ 1: ] # strip leading slash
            compile( file )


# In[ ]:


def start_jupyter( path = '.' ):
    process = sp.Popen( [ 'jupyter', 'notebook' ], stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE )
    return process


# In[ ]:


def main( path = '.' ):
    global _root
    _root = path

    process = start_jupyter( path )
    signal.signal( signal.SIGINT, lambda sig, frame: kill_process( process ) )

    stdout = process.stdout
    stderr = process.stderr

    listen( stderr, sys.stderr )


# In[ ]:


def parse_args():
    parser = argparse.ArgumentParser(
        description = 'A Jupyter Notbook watcher.'
    )

    parser.add_argument(
        '-r', '--root',
        help = 'Path to server root',
        type = str,
        default = '.'
    )

    args = parser.parse_args()
    return args


# In[ ]:


if __name__ == '__main__':
    args = parse_args()
    root = args.root
    path = (
        root
        if os.path.isabs( root ) else
        os.path.normpath( os.path.join( os.getcwd(), root ) )
    )
    
    main( path )

