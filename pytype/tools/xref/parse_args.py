"""Parse command line arguments for xref."""

import argparse

from pytype import config as pytype_config
from pytype.tools import arg_parser
from pytype.tools.xref import kythe


def make_parser():
  """Make parser for command line args.

  Returns:
    A Parser object.
  """

  def add_kythe_field(parser, field):
    parser.add_argument(
        "--" + field, dest=field, type=str, action="store", default="",
        help="Part of kythe's file-level vname proto.")

  parser = argparse.ArgumentParser(usage="%(prog)s [options] input")
  add_kythe_field(parser, "kythe_corpus")
  add_kythe_field(parser, "kythe_root")
  parser.add_argument("inputs", metavar="input", nargs=1,
                      help="A .py file to index")
  parser.add_argument("--debug", action="store_true",
                      dest="debug", default=None,
                      help="Display debug output.")
  # Add options from pytype-single.
  wrapper = arg_parser.ParserWrapper(parser)
  pytype_config.add_basic_options(wrapper)
  pytype_config.add_infrastructure_options(wrapper)
  return arg_parser.Parser(parser, wrapper.actions)


def parse_args(argv):
  """Parse command line args.

  Arguments:
    argv: Raw command line args, typically sys.argv[1:]

  Returns:
    A tuple of (
      parsed_args: argparse.Namespace,
      kythe_args: kythe.Args,
      pytype_options: pytype.config.Options)
  """

  parser = make_parser()
  args = parser.parse_args(argv)
  pytype_options = pytype_config.Options(args.inputs)
  pytype_options.tweak(**parser.get_pytype_kwargs(args))
  kythe_args = kythe.Args(corpus=args.kythe_corpus, root=args.kythe_root)
  return (args, kythe_args, pytype_options)
