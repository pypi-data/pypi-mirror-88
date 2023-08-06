# Standard Library
import argparse
import base64
from datetime import datetime
import os
import textwrap

# external
from six import binary_type, iteritems, text_type
from stix2validator import validate_string
from stix2validator.validator import FileValidationResults

# internal
from stix2elevator.options import info, warn


def id_property(path):
    name = path[0][-1]
    if name.find('[') != -1:
        name = path[0][-2]
    return name == "id" or name.endswith("ref") or name.endswith("refs")


def identifying_info(stix1x_obj):
    if stix1x_obj:
        if hasattr(stix1x_obj, "id_") and stix1x_obj.id_:
            return text_type(stix1x_obj.id_)
        elif hasattr(stix1x_obj, "idref") and stix1x_obj.idref:
            return "with idref " + text_type(stix1x_obj.idref)
        elif hasattr(stix1x_obj, "title") and stix1x_obj.title:
            return "'" + text_type(stix1x_obj.title) + "'"
        elif hasattr(stix1x_obj, "name") and stix1x_obj.name:
            return "'" + text_type(stix1x_obj.name) + "'"
        elif hasattr(stix1x_obj, "item") and stix1x_obj.item:
            # Useful in Related Types.
            return "parent of object " + identifying_info(stix1x_obj.item)
        else:
            return stix1x_obj.__class__.__name__
    return "- no identifying information available"


def canonicalize_label(t):
    t = text_type(t)
    t = t.lower()

    t = t.replace(" ", "-")

    return t


def map_vocabs_to_label(t, vocab_map):
    if vocab_map.get(t, ""):
        return vocab_map[t]
    else:
        return canonicalize_label(t)


def convert_controlled_vocabs_to_open_vocabs(new_obj, new_property_name, old_vocabs, vocab_mapping, only_one, required=True):
    if not old_vocabs and required:
        if only_one:
            new_obj[new_property_name] = "unknown"
        else:
            new_obj[new_property_name] = ["unknown"]
        warn("No STIX 1.x vocab value given for %s, using 'unknown'", 509, new_property_name)
    else:
        new_obj[new_property_name] = []
        for t in old_vocabs:
            if new_obj[new_property_name] is None or not only_one:
                if isinstance(t, (text_type, binary_type)):
                    new_obj[new_property_name].append(map_vocabs_to_label(t, vocab_mapping))
                else:
                    new_obj[new_property_name].append(map_vocabs_to_label(text_type(t.value), vocab_mapping))
            else:
                warn("Only one %s allowed in STIX 2.0 - used first one", 510, new_property_name)


def strftime_with_appropriate_fractional_seconds(timestamp, milliseconds_only):
    if isinstance(timestamp, (text_type, binary_type)):
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    if milliseconds_only:
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def convert_timestamp_to_string(timestamp, entity=None, parent_timestamp=None, milliseconds_only=False):
    if timestamp is not None:
        return strftime_with_appropriate_fractional_seconds(timestamp, milliseconds_only)
    elif parent_timestamp is not None:
        info("Using parent object timestamp on %s", 902, identifying_info(entity))
        return strftime_with_appropriate_fractional_seconds(parent_timestamp, milliseconds_only)
    else:
        warn("Timestamp not available for %s, using current time", 905, identifying_info(entity))
        return strftime_with_appropriate_fractional_seconds(datetime.now(), milliseconds_only)


def convert_timestamp_of_stix_object(entity, parent_timestamp=None, milliseconds_only=False):
    if entity and hasattr(entity, "timestamp"):
        if entity.timestamp is not None:
            return strftime_with_appropriate_fractional_seconds(entity.timestamp, milliseconds_only)
    if parent_timestamp is not None:
        info("Using parent object timestamp on %s", 902, identifying_info(entity))
        # parent_timestamp might have already been converted to a string in a previous call
        if isinstance(parent_timestamp, text_type):
            return parent_timestamp
        else:
            return strftime_with_appropriate_fractional_seconds(parent_timestamp, milliseconds_only)
    warn("Timestamp not available for %s, using current time", 905, identifying_info(entity))
    return strftime_with_appropriate_fractional_seconds(datetime.now(), milliseconds_only)


_TYPE_MAP_FROM_1_x_TO_2_x = {"observable": "observed-data",
                             "toolinformation": "tool"}


def map_1x_type_to_20(stix1x_type):
    if stix1x_type in _TYPE_MAP_FROM_1_x_TO_2_x:
        return _TYPE_MAP_FROM_1_x_TO_2_x[stix1x_type]
    return stix1x_type


_MARKING_MAP_FROM_1_x_TO_2_x = {}


def check_map_1x_markings_to_2x(stix1x_marking):
    return (stix1x_marking in _MARKING_MAP_FROM_1_x_TO_2_x or
            stix1x_marking.id_ in _MARKING_MAP_FROM_1_x_TO_2_x or
            stix1x_marking.idref in _MARKING_MAP_FROM_1_x_TO_2_x)


def map_1x_markings_to_2x(stix1x_marking):
    if check_map_1x_markings_to_2x(stix1x_marking):
        if stix1x_marking in _MARKING_MAP_FROM_1_x_TO_2_x:
            return _MARKING_MAP_FROM_1_x_TO_2_x[stix1x_marking]
        if stix1x_marking.id_ in _MARKING_MAP_FROM_1_x_TO_2_x:
            return _MARKING_MAP_FROM_1_x_TO_2_x[stix1x_marking.id_]
        if stix1x_marking.idref in _MARKING_MAP_FROM_1_x_TO_2_x:
            return _MARKING_MAP_FROM_1_x_TO_2_x[stix1x_marking.idref]
    return stix1x_marking


def add_marking_map_entry(stix1x_marking, stix2x_marking_id):
    if stix1x_marking not in _MARKING_MAP_FROM_1_x_TO_2_x:
        _MARKING_MAP_FROM_1_x_TO_2_x[stix1x_marking] = stix2x_marking_id
        if stix1x_marking.id_:
            _MARKING_MAP_FROM_1_x_TO_2_x[stix1x_marking.id_] = stix2x_marking_id
        return
    return map_1x_markings_to_2x(stix1x_marking)


def clear_1x_markings_map():
    global _MARKING_MAP_FROM_1_x_TO_2_x
    _MARKING_MAP_FROM_1_x_TO_2_x = {}


def iterpath(obj, path=None):
    """
    Generator which walks the input ``obj`` model. Each iteration yields a
    tuple containing a list of ancestors and the property value.

    Args:
        obj: A TLO object.
        path: None, used recursively to store ancestors.

    Example:
        >>> for item in iterpath(tlo):
        >>>     print(item)
        (['type'], 'campaign')
        ...
        (['cybox', 'objects', '[0]', 'hashes', 'sha1'], 'cac35ec206d868b7d7cb0b55f31d9425b075082b')

    Returns:
        tuple: Containing two items: a list of ancestors and the property value.

    """
    if path is None:
        path = []

    for varname, varobj in iter(sorted(iteritems(obj))):
        path.append(varname)
        yield (path, varobj)

        if isinstance(varobj, dict):

            for item in iterpath(varobj, path):
                yield item

        elif isinstance(varobj, list):

            for idx, item in enumerate(varobj):
                index = "[{0}]".format(idx)
                path.append(index)

                yield (path, item)

                if isinstance(item, dict):
                    for descendant in iterpath(item, path):
                        yield descendant

                path.pop()

        path.pop()


def operation_on_path(obj, path, value, op=1):
    """operations: (1 = set_value, 2 = delete_entry)"""
    current = path[0]
    path = path[1:]

    if isinstance(current, int):
        current_obj = obj[current]
    elif "[" in current and "]" in current:
        current = int(current.strip("[]"))
        current_obj = obj[current]
    else:
        current_obj = obj[current]

    if not path:
        if op == 1:
            obj[current] = value
        elif op == 2:
            del obj[current]

        return

    operation_on_path(current_obj, path, value, op)


def find_dir(path, directory):
    """
    Args:
        path: str containing path of the script calling this method.
        directory: str containing directory to find.

    Returns:
        str: A string containing the absolute path to the directory.
        None otherwise.

    Note:
        It only finds directories under the cti-stix-elevator package.

    Raises:
        RuntimeError: If trying to access other directories outside of the
        cti-stix-elevator package.
    """
    working_dir = path.split("cti-stix-elevator")

    if len(working_dir) <= 1 or not all(x for x in working_dir):
        msg = "Verify working directory. Only works under cti-stix-elevator"
        raise RuntimeError(msg)

    working_dir = os.path.join(working_dir[0], "cti-stix-elevator")

    for root, dirs, files in os.walk(working_dir, topdown=True):
        if directory in dirs:
            found_dir = os.path.join(root, directory)
            return os.path.abspath(found_dir)


class NewlinesHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom help formatter to insert newlines between argument help texts.
    """
    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        txt = textwrap.wrap(text, width)
        txt[-1] += '\n'
        return txt


def validate_stix2_string(json_string, validator_options, file_path=None):
    # Ensure the json_string is a Unicode text string. json.dumps() sometimes
    # returns a byte-"str" on Python 2.
    if isinstance(json_string, binary_type):
        json_string = json_string.decode("utf-8")
    results = validate_string(json_string, validator_options)
    fvr = FileValidationResults(results.is_valid, file_path, results)
    return fvr


def encode_in_base64(s):
    return base64.b64encode(text_type(s).encode('utf-8')).decode('utf-8')


class Environment():
    def __init__(self, created_by_ref=None, timestamp=None, bundle_instance=None):
        self.created_by_ref = created_by_ref
        self.timestamp = timestamp
        self.bundle_instance = bundle_instance

    def newEnv(self, created_by_ref=None, timestamp=None):
        return Environment(created_by_ref if created_by_ref else self.created_by_ref,
                           timestamp if timestamp else self.timestamp,
                           self.bundle_instance)

    def add_to_env(self, created_by_ref=None, timestamp=None):
        if created_by_ref:
            self.created_by_ref = created_by_ref
        if timestamp:
            self.timestamp = timestamp
