"""
Validate information files

"""
# Standard library modules
import json
# import pprint
import os.path
import sys
import pkg_resources

# Non-standard modules
import jsonschema
import jsonref
import yaml

lazy_errors = True   # Can report multiple errors, but less stable
VALID_FORMATS = ['JSON', 'YAML']


def validate(filename, format=None, verbose=True, quiet=False):
    """
    Validates a YAML or JSON file against schema
    format: "JSON" or "YAML"

    if format is not provided, tries to figure it out from the
    filename suffix
    """

    if quiet:
        verbose = False

    SCHEMA_FILE = pkg_resources.resource_filename(
        'seaplan', f'data/seaplan.schema.json')

    if verbose:
        print(f'  Validating {filename} against '
              f'{os.path.basename(SCHEMA_FILE)}')

    instance = read_json_yaml(filename, format=format)

    base_path = os.path.dirname(SCHEMA_FILE)
    base_uri = f'file://{base_path}/'

    # LOAD SCHEMA FILE
    with open(SCHEMA_FILE, 'r') as f:
        try:
            schema = jsonref.loads(f.read(), base_uri=base_uri,
                                   jsonschema=True)
        except json.decoder.JSONDecodeError as e:
            print(f'JSONDecodeError: Error loading JSON schema file: '
                  f'{SCHEMA_FILE}')
            print(str(e))
            return
        except:
            print(f"Error loading JSON schema file: {SCHEMA_FILE}")
            print(sys.exc_info()[1])
            return
    # VALIDATE SCHEMA FILE
    try:
        if verbose:
            print('\tTesting schema ...', end='')

        v = jsonschema.Draft4Validator(schema)

        if verbose:
            print('OK, instance ...', end='')
    except jsonschema.ValidationError as e:
        if quiet:
            # IF HAVE TO PRINT ERROR MESSAGE, PRINT INTRO TOO
            print(f'instance = {filename}')
        else:
            print('')
        print('\t' + e.message)
    except:
        print("schema failed and I don't know why")
    # VALIDATE PARAMETER FILE
    try:
        if not v.is_valid(instance):
            if quiet:
                # IF HAVE TO PRINT ERROR MESSAGE, PRINT INTRO TOO
                print(f'instance = {filename}')
            else:
                print('')
            if lazy_errors:
                # Lazily report all errors in the instance
                # ASSUMES SCHEMA IS DRAFT-04 (I couldn't get it to work
                # otherwise)
                try:
                    for error in v.iter_errors(instance):
                        print('\t\t', end='')
                        try:
                            for elem in error.path:
                                print(f"['{elem}']", end='')
                        except:
                            print("Error in error.path")
                        print(f': {error.message}')
                except:
                    print('Error in v.iter_errors(instance)')
            else:
                # Just report first error and bail
                error = next(v.iter_errors(instance))
                print('\t\t', end='')
                for elem in error.path:
                    print(f"['{elem}']", end='')
                print(f': {error.message}')
            print('\tFAILED')
        else:
            if not quiet:
                print('OK')
    except jsonschema.ValidationError as e:
        if quiet:
            # IF HAVE TO PRINT ERROR MESSAGE, PRINT INTRO TOO
            print(f'instance = {filename}')
        else:
            print('')
        print('\t' + e.message)
    except jsonschema.exceptions.UnknownType as e:
        print(e)
    return


def read_json_yaml(filename, format=None, debug=False):
    """ Reads a JSON or YAML file """
    if not format:
        format = get_information_file_format(filename)

    with open(filename, 'r') as f:
        if format == 'YAML':
            try:
                element = yaml.safe_load(f)
            except:
                print(f"Error loading YAML file: {filename}")
                print(sys.exc_info()[1])
                return
        else:
            try:
                element = json.load(filename)
            except JSONDecodeError as e:
                print(f"JSONDecodeError: Error loading JSON file: {filename}")
                print(str(e))
                return
            except:
                print(f"Error loading JSON file: {filename}")
                print(sys.exc_info()[1])
                return

    return element


def get_information_file_format(filename):
    """
    Determines if the information file is in JSON or YAML format

    Assumes that the filename is "*.{FORMAT}
    """

    format = filename.split('.')[-1].upper()
    if format in VALID_FORMATS:
        return format
    print('Unknown format: {format}')
    sys.exit(1)


def _console_script(argv=None):
    """
    Validate a seaplan information file

    Validates a file named *.seaplan.json or *.seaplan.yaml against
    schema.seaplan.json.
    """
    from argparse import ArgumentParser

    parser = ArgumentParser(prog='seaplan-validate', description=__doc__)
    parser.add_argument('info_file', help='Information file')
    parser.add_argument('-f', '--format', choices=VALID_FORMATS,
                        default=None,
                        help='Forces information file to be interpreted as '
                             '"JSON" or "YAML"(overrides interpreting from '
                             'filename)')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='increase output verbosiy')
    args = parser.parse_args()

    validate(args.info_file, format=args.format, verbose=args.verbose)
