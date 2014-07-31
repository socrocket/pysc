import argparse

parser = argparse.ArgumentParser()

def create(*k, **kw):
    parser = argparse.ArgumentParser(*k, **kw)
    return parser
