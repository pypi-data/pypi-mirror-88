from os import path
from .utils import parse_params_values
from .cli_configs import BootstrapConfig
from ...io.config import generate_nabu_configfile
from ..validators import convert_to_bool

def parse_sections(sections):
    sections = sections.lower()
    if sections == "all":
        return None
    sections = sections.replace(" ", "").split(",")
    return sections



def bootstrap():
    args = parse_params_values(
        BootstrapConfig,
        parser_description="Initialize a nabu configuration file"
    )

    do_bootstrap = bool(args["bootstrap"])
    do_convert = (args["convert"] != "")
    no_comments = bool(args["nocomments"])

    if do_convert: # do_convert
        print("The --convert option is deprecated. It will be removed in a future version")
        exit(1)
    if do_bootstrap:
        print("The --bootstrap option is now the default behavior of the nabu-config command. This option is therefore not needed anymore.")

    if path.isfile(args["output"]):
        rep = input("File %s already exists. Overwrite ? [y/N]" % args["output"])
        if rep.lower() != "y":
            print("Stopping")
            exit(0)

    prefilled_values = {}
    if args["dataset"] != "":
        prefilled_values["dataset"] = {}
        prefilled_values["dataset"]["location"] = args["dataset"]
    generate_nabu_configfile(
        args["output"],
        comments=not(no_comments),
        options_level=args["level"],
        prefilled_values=prefilled_values,
    )

