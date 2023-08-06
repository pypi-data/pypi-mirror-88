# -*- coding: utf-8 -*-

# Copyright © 2017, François Laurent

# Copyright © 2017, Institut Pasteur
#   Contributor: François Laurent
#   Contribution: Metadata, parse_metadata

# Copyright © 2018, Institut Pasteur
#   Contributor: François Laurent
#   Contribution: LockInfo.__nonzero__

# This file is part of the Escale software available at
# "https://github.com/francoislaurent/escale" and is distributed under
# the terms of the CeCILL-C license as circulated at the following URL
# "http://www.cecill.info/licenses.en.html".

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C license and that you accept its terms.


from escale.base.essential import asstr, basestring
import os.path
# former format
import time
import calendar


class LockInfo(object):

    __slots__ = ['version', 'owner', 'target', 'mode']

    def __init__(self, version=None, owner=None, target=None, mode=None):
        self.owner = None
        if owner:
            self.owner = asstr(owner)
        self.target = target
        self.mode = None
        if mode:
            self.mode = asstr(mode)
        self.version = None
        if version:
            self.version = asstr(version)
        elif self.owner or self.mode:
            self.version = '1.0'

    def __bool__(self):
        return not (self.owner is None and self.target is None and self.mode is None)

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        if self.version:
            info = ['%'.join(('lock', self.version))]
            if self.owner:
                info.append(': '.join(('owner', self.owner)))
            if self.mode:
                info.append(': '.join(('mode', self.mode)))
            return '\n'.join(info)
        elif self.owner:
            return self.owner # former format, before LockInfo introduction
        else:
            return ''


def parse_lock_file(file, target=None):
    if target is None:
        target = file
    version = None
    owner = None
    mode = None
    with open(file, 'r') as f:
        line = f.readline()
        if line.startswith('lock%'):
            version = line[5:].rstrip() # 1.0
            for line in f.readlines():
                if line.startswith('owner:'):
                    owner = line[6:].strip()
                elif line.startswith('mode:'):
                    mode = line[5:].strip()
        else: # first format
            if line:
                owner = line
    return LockInfo(version, owner, target, mode)


former_timestamp_format = '%y%m%d_%H%M%S'


class Metadata(object):

    __slots__ = ['header', 'version', 'target', 'pusher',
            'timestamp', 'timestamp_format', 'checksum',
            'parts', 'pullers',
            'ignored']

    def __init__(self, version=None, target=None, pusher=None, timestamp=None, timestamp_format=None,
            checksum=None, parts=None, pullers=[], **ignored):
        self.header = 'placeholder'
        if pusher:
            pusher = asstr(pusher)
        self.pusher = pusher
        self.target = target
        if timestamp:
            if isinstance(timestamp, basestring):
                if not timestamp_format or timestamp_format is True:
                    timestamp_format = former_timestamp_format
                timestamp = time.strptime(timestamp, timestamp_format)
            if isinstance(timestamp, time.struct_time):
                timestamp = calendar.timegm(timestamp)
            timestamp = int(timestamp)
        self.timestamp = timestamp
        self.timestamp_format = timestamp_format
        self.checksum = checksum
        if version:
            version = asstr(version)
        elif pusher or checksum:
            version = '1.0'
        self.version = version
        self.pullers = pullers
        self.ignored = ignored
        if parts:
            parts = int(parts)
        self.parts = parts

    def __repr__(self):
        if self.version:
            if not (self.timestamp or self.checksum):
                raise ValueError("neither 'timestamp' nor 'checksum' are defined")
            info = ['%'.join((self.header, self.version))]
            if self.pusher:
                info.append(': '.join(('pusher', self.pusher)))
            if self.timestamp:
                info.append(': '.join(('timestamp', str(self.timestamp))))
            if self.checksum:
                info.append(': '.join(('checksum', asstr(self.checksum))))
            if self.parts:
                info.append(': '.join(('parts', str(self.parts))))
            for k in self.ignored:
                info.append(': '.join((k, self.ignored[k])))
            info.append('---pullers---')
            if self.pullers:
                info += self.pullers
            return '\n'.join(info)
        elif self.timestamp:
            # former format, before :class:`Metadata` introduction
            if not self.timestamp_format or self.timestamp_format is True:
                self.timestamp_format = former_timestamp_format
            timestamp = time.strftime(self.timestamp_format, time.gmtime(self.timestamp))
            if self.pullers:
                return '\n'.join([timestamp]+self.pullers)
            else:
                return timestamp
        else:
            return ''

    @property
    def reader_count(self):
        if not self.pullers:
            return 0
        elif isinstance(self.pullers, (int, float)):
            return self.pullers
        elif isinstance(self.pullers, (list, tuple)):
            return len(self.pullers)

    @property
    def part_count(self):
        return self.parts

    def fileModified(self, local_file=None, last_modified=None, checksum=None, hash_function=None, remote=False, debug=None):
        """
        Tell whether a file has been modified.

        Arguments:

            local_file (str): local file path; file must have a valid last
                modification time.

            last_modified (int): last modification time (local).

            checksum (str-like): checksum of file content (local).

            hash_function (callable): hash function that can be applied to the
                content of the `local_file` file if `checksum` is not defined.

            remote (bool): if `True`, `fileModified` tells whether or not
                the remote copy of the file is a modified version of the 
                local file;
                if `False`, `fileModified` tells whether or not the local
                file is a modified version of the remote copy of the file;
                if `None`, `fileModified` tells whether there is any
                difference.

        Returns:

            bool: `True` if file has been modified.

        """
        if last_modified and self.timestamp and last_modified == self.timestamp:
            return False
        file_available = local_file and os.path.isfile(local_file)
        identical = None
        if self.checksum:
            if not checksum and file_available and hash_function is not None:
                with open(local_file, 'rb') as f:
                    content = f.read()
                    checksum = hash_function(content)
            if checksum:
                identical = checksum == self.checksum
                #if debug and not identical:
                #    debug((local_file, checksum, self.checksum))
                if identical:
                    # if files are identical
                    return False
        if file_available:
            local_mtime = last_modified if last_modified else int(os.path.getmtime(local_file))
            if self.timestamp:
                remote_mtime = self.timestamp
                if identical is False and local_mtime == remote_mtime:
                    # likely cause: encryption introduces "salt" in the message
                    # checksum should be calculated from plain data
                    msg = "the last modification times match but the checksums do not: file {}".format(self.target if self.target else local_file)
                    if debug:
                        debug(msg)
                        if file_available:
                            with open(local_file, 'rb') as f:
                                content = f.read()
                        try:
                            import struct
                            cs = sum(struct.unpack('<'+'B'*len(content), content))
                            debug((local_file, cs, checksum, self.checksum))
                        except (KeyboardInterrupt, SystemExit):
                            raise
                        except:
                            debug((local_file, checksum, self.checksum))
                        return True
                    else:
                        raise RuntimeError(msg)
                elif identical is True and local_mtime != remote_mtime:
                    if debug:
                        msg = "reverting external change in last modification time: file {}".format(self.target if self.target else local_file)
                        debug(msg)
                    os.utime(local_file, (time.time(), remote_mtime))
                    return False
                #if debug and local_mtime != remote_mtime:
                #    debug((local_file, local_mtime, remote_mtime))
                if remote is False:
                    return remote_mtime < local_mtime
                elif remote is True:
                    return local_mtime  < remote_mtime
                elif remote is None:
                    return local_mtime != remote_mtime
                else:
                    raise ValueError("wrong value for 'remote': '{}'".format(remote))
        else:
            return True
        return None


def parse_metadata(lines, target=None, timestamp_format=None, log=None):
    if isinstance(lines, Metadata):
        return lines
    # read file if not already done
    if not isinstance(lines, (tuple, list)):
        if os.path.isfile(lines):
            with open(lines, 'r') as f:
                lines = f.readlines()
        else:
            lines = lines.splitlines()
    # define a few helpers
    def invalid(line):
        return ValueError("invalid meta attribute: '{}'".format(line))
    convert = {'timestamp': int, 'parts': int}
    # 'parts' can be converted in `Metadata` constructor; 'timestamp' cannot
    # parse
    meta = {}
    if target:
        meta['target'] = target
    pullers = []
    version = None
    if lines:
        line = lines[0].rstrip()
        if line:
            try:
                header, version = line.rsplit('%', 1)
            except ValueError:
                # former format
                meta['timestamp'] = line
                list_pullers = True
            else:
                list_pullers = False
            for line in lines[1:]:
                line = line.rstrip()
                if not line:
                    continue
                if list_pullers:
                    pullers.append(line)
                elif line[0] in '-=+#%':
                    section = line.strip(line[0]).lower()
                    if section.startswith('puller') or section.startswith('reader'):
                        list_pullers = True
                    else:
                        # TODO: debug and remove the broken_metadata.txt file creation below
                        with open('broken_metadata.txt', 'w') as f:
                            for _line in lines:
                                f.write(_line+'\n')
                        raise invalid(line)
                else:
                    try:
                        key, value = line.split(':', 2)
                    except ValueError:
                        raise invalid(line)
                    value = value.lstrip()
                    try:
                        value = convert[key](value)
                    except KeyError:
                        pass
                    meta[key] = value
    # make metadata object
    metadata = Metadata(version=version, pullers=pullers,
            timestamp_format=timestamp_format, **meta)
    # report and purge ignored metadata
    if metadata.ignored:
        if log:
            msg_body = 'unsupported meta attribute'
            if metadata.target:
                for k in metadata.ignored:
                    log("{} for resource '{}': '{}'".format(msg_body, metadata.target, k))
            else:
                for k in metadata.ignored:
                    log("{}: '{}'".format(msg_body, k))
        metadata.ignored = {}
    return metadata

