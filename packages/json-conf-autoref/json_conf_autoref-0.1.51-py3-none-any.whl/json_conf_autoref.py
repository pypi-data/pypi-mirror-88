# coding: utf-8
"""json_conf_autoref

    Version
    -------
    0.1.5

    Description
    -----------

    This module is a config parser that works with JSON format. Content can come
    from a JSON file or string. The module accepts variable definition inside the
    JSON data just adding '$' character to refere to any key that exists inside
    the JSON content.

    Examples
    --------

    # conf/default.json
    {
        "hdfs-user":"some_cool_guy"
        ,"hdfs-base":"hdfs://yourcompany.com/user/$hdfs-user/fantastic-project"

    }

    # code snipet - from JSON file
    import json_conf_autoref as jca

    conf = jca.process(file="conf/default.json")
    jca.show(conf)

    Shows

    {
        "hdfs-base": "hdfs://yourcompany.com/user/some_cool_guy/fantastic-project",
        "hdfs-user": "some_cool_guy"
    }

    # From a JSON string

    my_json = '{"hdfs-user":"some_cool_guy","hdfs-base":"hdfs://yourcompany.com/user/${hdfs-user}/fantastic-project"}

    conf = jca.process(json_string = my_json)

    jca.show(conf)

    Shows

    {
        "hdfs-base": "hdfs://yourcompany.com/user/some_cool_guy/fantastic-project",
        "hdfs-user": "some_cool_guy"
    }

    # Vars
    {
        "project-name":"fantastic-project"
        "hdfs-base": "hdfs://yourcompany.com/user/some_cool_guy/${project-name}",
        "hdfs-user": "some_cool_guy"
    }

    # Vars inside lists(EXPERIMENTAL)

    my_json = '{"hdfs-user":"joe", "system-users":["${hdfs-user}","mary","lucca"] }'

    conf = jca.process(json_string = my_json)

    jca.show(conf)


    Shows

    '{"hdfs-user":"joe", "system-users":["joe","mary","lucca"] }'


    Limitations
    -----------

    Vars on list is experimental and could crash in "not-mapped" situations.


"""
import json
import sys
import os
import re
from exceptions import *

__version__ = '0.1.5'


__author__ = "André Carneiro"


def __traverse_json(json_input,path):
    """A internal recursive function that goes through JSON hierarchical structure
    looking for variables inside values using regular expression and yields
    a list of variables that it's found.

        Parameters
        ----------

        json_input: list or dict, requited
        Python data structure(list or dict) with JSON data

        path: str,required
        The start point in the JSON structure

        Yields
        -------

            First scenario - Not-list structure
            -----------------------------------
            A new recursive call to function passing the current path if value in some
            point of structure not satisfies the requirements to replace variables to
            values

            or

            A key-value pair dictionary with

            Second scenario - list structure
            --------------------------------
            Iterates the list and do the same thing in first scenario for each
            element of the list

    """
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            # Divides the structure keys with '/'. Familiar, huh?
            if isinstance(v,str) and re.search(r'^.*?(\$(ENV|){.+?}).*?$',v):
                yield { '/'.join([path , k]) : v }
            else:
                # yields a new recursive call for __traverse passing
                # the current value and current path level
                yield from __traverse_json(v, '/'.join([path , k]))
    elif isinstance(json_input, list):
        yield { path:json_input }


def __check_result(data):
    """Returns False if exists some variable under processing results structure.
        Otherwise returns True

        Parameters
        ----------
        data : dict
            Processing result dictionary

        Returns
        -------
        False
            If there is variables not replaced by their respective values.

        True
            Otherwise


    """
    lookups = []
    for _ in __traverse_json(data,''):
        lookups.append(_);

    if len(lookups) == 0:
        return True
    ok = True
    for l in lookups:
        for k,v in l.items():
            if isinstance(v,list):
                for i in v:
                    if re.search(r'\${.+?}*',str(i)):
                        return False
            elif re.search(r'\${.+?}*',str(v)):
                return False
            else:
                return True
    return ok


def __get_from_path(data,path):
    """Recovers a value that is referenced by a var under 'dot-path'("Ex: "$hdfs-paths.incoming").

        Parameters
        ----------
        data : dict
            Full JSON data under dictionary

        path : str
            A 'dot-path' var string


        Returns
        -------
        A single value of a var.


    """
    levels = re.split(r'\.',path)
    if len(levels) == 0:
        levels = [path]

    value = None
    key = re.sub(r'^\${','',levels[0])
    key = re.sub(r'}','',key)
    value = data[key]
    if isinstance(value,list) or isinstance(value,dict):
        levels.pop(0)
        new_path = '.'.join(levels)
        new_data = value
        return __get_from_path(new_data,new_path)
    else:
        return value


def __replace_vars_list(data,path,element_path,position):
    """Replace vars under single values(strings and numbers for example).

        Parameters
        ----------
        data : dict
            JSON structure(full of it) transcripted to a dictionary

        path : list
            All path to an target element

        element_path : str
            The full path element string of JSON structure

        position : int
            The position in the list that is beeing analyzed


        Returns
        -------
        A dictionary with the processing result
    """

    # Separating variables from the rest of the path
    vars_to_replace = re.findall(r'(\${.+?})',str(element_path))
    new_list = []

    # Transforming paths into a valid dictionary path
    transformed_path = ""
    for part in path:
        transformed_path += "['{}']".format(part)
    # temp_flag = False

    # Just place the same value on the array(list) position
    if len(vars_to_replace) == 0:
        exec("data{}[{}] = element_path".format(str(transformed_path),str(position)))

    else:

        # Getting values for replacing
        for v in vars_to_replace:
            # Removing stupid chars(and content after it) that could mess
            # the reference names.
            # Don't know if this regex is enough yet. For now, this is it!
            v = re.sub(r'[\:\,\ \@\#\*\&\%\/].*?$','',str(v))
            #v = re.sub(r'.*?(\$.+?)$','',v)

            value = __get_from_path(data,v)
            what = re.sub(r'\$',"\\$",v)
            to = value
            where = element_path
            regex_result = re.sub(r"" + what + r"", str(to), str(where))
            cmd = ''
            if not re.search(r'[\(\{\:]+', regex_result) or re.search(r'\$', regex_result):
                cmd = f"data{transformed_path}[{position}] = '{regex_result}'"
            else:
                cmd = f"data{transformed_path}[{position}] = {regex_result}"

            exec(cmd)
    return data


def __replace_vars_single(data,path,element_path):
    """Replace vars under single values(strings and numbers for example).

        Parameters
        ----------
        data : dict
            JSON structure(full of it) transcripted to a dictionary

        path : list
            All path to an target element

        element_path : str
            The full path element string of JSON structure


        Returns
        -------
        A dictionary with the processing result

    """
    # Separating variables from the rest of the path
    vars_to_replace = re.findall(r'(\$\{.+?\})',str(element_path))

    # Transforming paths into a valid dictionary path
    transformed_path = ""
    for part in path:
        transformed_path += f"['{part}']"

    # Getting values for replacing
    for v in vars_to_replace:
        if v == '':
            continue
        # Removing stupid chars(and content after it) that could mess
        # the reference names.
        # Don't know if this regex is enough yet. For now, this is it!
        v = re.sub(r'[\:\,\ \@\#\*\&\%\/].*?$','',str(v))
        # For variables that represents paths. Like "$pathLv1.pathLv2.pathLvN"
        key = value = ''
        if re.search(r'\.',v):
            value_path = re.split(r'\.',v)
            var_path = ""

            for part in value_path:
                # Preparing var
                prepared_part = re.sub(r'^\${','',part)
                prepared_part = re.sub(r'}$','',prepared_part)
                var_path += f"['{prepared_part}']"

            # Getting value for 'doted' variables
            value = eval(f"data{var_path}")

        # For variables that is defined on root of config content
        else:
            # So, var is in the root path
            key = re.sub(r'\${','',v)
            key = re.sub(r'}','',key)
            value = data[key]

        # Preparing 'v' for regex
        v = re.sub(r'\$', '\\$',v)
        # Storing regex replacement result
        #replacement = eval("re.sub(r''+ v, value, element_path)")
        replacement = re.sub(r''+ v, value, element_path)
        # updating element_path with regex replacement result
        element_path = replacement
        # Finally replacing values in data
        exec(f"data{transformed_path} = replacement")

    # EXPERIMENTAL
    # Replacing environment var. if it exists. If not, raise error?
    envs = re.findall(r'(\$ENV\{(.+?)})', element_path)
    for env in envs:
        # The target string that will be submited to regex
        target = env[0]
        # Name of the environment variable
        env_name = env[1]
        # Value(If exists) of the environment variable
        replacement = os.environ[env_name]
        # Preparing target to regex
        target = re.sub(r'\$','\\$', target)
        # Applying regex
        regex_result = re.sub( r'' + target + r'', replacement, element_path )
        # Updating element_path
        element_path = regex_result
        # Placing the result back to the data
        exec(f"data{transformed_path} = regex_result")

    return data


def __replace_vars_factory(data,path,element_path,type):
    """A factory function when the goes is decide what kind
        of processing data must be submited. The possibilities
         of 'type' are determinated by a string that must contain only one
        of two values:

        * single: a single value(string or numbers)

        * list: single values inside lists(arrays)

        Parameters
        ----------
        data : dict
            JSON structure(full of it) transcripted to a dictionary

        path : list
            All path to an target element

        element_path : str
            The full path element string of JSON structure

        type : str
            The type of vars replacing. Must be 'single' or 'list'


        Returns
        -------
        A dictionary with the processing result


        Exceptions
        ----------
        InvalidParam
            When type was passed as something different than 'single' nor 'list'


    """
    if type == 'list':
        position = 0
        for e in element_path:
            data = __replace_vars_list(data,path,e,position)
            position += 1
    elif type == 'single':
        data = __replace_vars_single(data,path,element_path)
    else:
        raise InvalidParam("type must be 'list' or 'single'!")

    return data


def __analyze(data):
    """Applies the 'traverse' on JSON structure(here is a dictionary) and submit
        data to __replace_vars_factory to replace values under this structure
        depending the kind of it(single or list) and return the results as a
        dictionary.

        Parameters
        ----------
        data : dictionary
        JSON structure transcripted to a dictionary


        Returns
        -------
        A dictionary with the processing results

    """
    lookups = []
    for _ in __traverse_json(data,''):
        lookups.append(_);
    for l in lookups:
        for rawPath,lookup in l.items():
            Items = re.split(r'/',rawPath)
            if Items[0] == '':
                Items.pop(0)

            # What's it values?
            element_path = None
            path = []
            for i in Items:
                if(element_path == None):
                    element_path = data[i]
                else:
                    element_path = element_path[i]
                path.append(i)

            if isinstance(element_path,list):
                data = __replace_vars_factory(data,path,element_path,'list')
            else:
                data = __replace_vars_factory(data,path,element_path,'single')

    return data


def show(data):
    """Shows the results of JSON processing from a config data
    passing the 'process' resultant dictionary on the screen

        Parameters
        ----------
        data : dictionary
                The dictionary generated after 'process'
                function call

        Returns
        -------
        Nothing


    """
    print(str(json.dumps(data,indent=4,sort_keys=True)))


def __remove_comments_single(line):
    """Removes the comments from a single line string.

    """
    # If a '#' character is between a valid JSON string, it will be ignored. Otherwise,
    # all characters after '#' character will be removed from the string
    if (re.search(r'^.*?#.+?$', line) and \
    not re.search(r'("|\').*?#.*?("|\')', line)) or \
    re.search(r'^[^\'"]*#', line):
        line = re.sub(r'^(.*?)#.+?$', r'\1', line)

    return line

def __remove_comments_multilines(lines):
    """Break the multiline string into a single line string and applies their
    __remove_comments function.

    """
    more_lines = re.split(r'(\r\n|\n\r|\n|\r)', lines)
    removed = []
    for line in more_lines:
        line = __remove_comments_single(line)
        removed.append(line)
    result = lines

    if len(removed) > 0:
        result = "".join(removed)
    return result


def __remove_comments(lines):
    """Removes the comment using '#' character as reference, considering the possibility
    to have the '#' inside an valid string on JSON structure. Returns a string
    without comments.

        Parameters
        ----------

        lines (str): line string to remove comments.


        Returns
        -------

        A string without comments

    """
    if re.search(r'(\n|\r|\r\n|\n\r)', lines):
        line = __remove_comments_multilines(lines)

    else:
        line = __remove_comments_single(lines)

    return line

def process(json_string=None,file=None):
    """Reads the JSON from file or string. Then, iterates the processing
        using __analyze and __check_results internal functions to evaluate if
        there is some variable in deep structure needs to be replaced and/or
        if the times to try is over or not.

        Returns a dictionary with all data processed.


        Parameters
        ----------
        json_string : str or None

        file : str or None


        Returns
        -------
        A dictionary with processed config data


        Exceptions
        ----------

        ValueError
            When JSON reading fails.

        LimitException
            When iterations exceeds the iterations times limits(max 5x)

        InvalidParam
            When 'json_string' and 'file' params are not set

    """
    data = None

    # Checking parameters
    if not json_string and not file:
        raise InvalidParam("No input data! You must define 'json_string' or 'file' parameter")

    # The file parameter has precedence over json_string parameter
    if file is not None:
        data = {}
        tmp_file = f"{file}.tmp"
        # Removing comments from file
        with open(file) as f, open(tmp_file, 'w') as f2:
            for line in f:
                line = __remove_comments(line)
                f2.write(line)
        f2.close()

        #Loading JSON from new file
        with open(tmp_file) as f:
            data = json.load(f)

    else:
        try:
            # Removing comments
            json_string = __remove_comments(json_string)

            # Loading JSON
            data = json.loads(json_string)
        except ValueError as e:
            print("JSON error! {}".format(str(e)))
            raise

    # Because of random key acess, some variables could not be processed. So,
    # must run again until this happens. But a limit of 5 iterations was defined
    # to avoid infinit recursion.
    data = __analyze(data)
    if not __check_result(data):
        limit = 5
        curr_time = 0
        while not __check_result(data):
            data = __analyze(data)
            if curr_time >= limit:
                raise LimitException("Fatal! Can't process this data! Please, report this issue sending the config data!")
            curr_time += 1

    return data


if __name__ == '__main__':
    pass


class LimitException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
