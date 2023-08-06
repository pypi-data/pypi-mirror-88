import re
import uuid
import asyncio
import logging
import aiofiles
import concurrent
import collections
from functools import partial
from async_lru import alru_cache
try:
    # get ADVERTISED_URL for xpresso result service
    from taas.results.settings import ADVERTISED_URL
except Exception:
    ADVERTISED_URL = ''

logger = logging.getLogger(__name__)


class BaseResultsParser(object):
    # TODO: store_results
    def __init__(self, archive, result_id='', store_results=False,
                 related_id='N/A', component='N/A', branch='N/A',
                 created_by='', meta_info={}):
        self.archive = archive
        self.results = {}  # Memory storage for parsed results
        self._sequence_number = 0

        self.result_id = result_id
        # self.archive_location = archive_location
        self.related_id = related_id
        self.component = component
        self.branch = branch

        # If true, then save to DB; else save in mem in results dict
        self.store_results = store_results
        self.created_by = created_by
        self.meta_info = meta_info
        self.BLANK = ''

    def parse(self):
        # Need to implement parsing part in subclasses
        # short cut
        self.meta = self.results.get('meta')
        self.scripts = self.results.get('scripts')
        self.summary = self.results.get('summary')
        self.prepare_sections()
        return self

    def prepare_sections(self):
        # store {uuid: section/step object}
        self.sections_dict = {}
        for task in [*self.scripts]:
            for section in task.get('sections', []):
                self.sections_dict[section['id']] = LogSection(
                    self.archive, section, self.meta.get('exec_host'),
                    self.result_id)

    def get_section(self, section_uuid):
        ''' section_uuid: section/step uuid
            return: LogSection object
        '''
        if not hasattr(self, "sections_dict"):
            self.parse()
        return self.sections_dict.get(section_uuid)

    def get_task_names(self):
        task_list = []
        for item_no, item in enumerate(self.scripts):
            task_list.append(
                {
                    'task_id': item['meta']['task_id'],
                    'sequence_number': item_no
                }
            )
        return task_list

    def get_overview(self):
        overview = {}
        overview.update(self.meta)
        overview["summary"] = self.summary
        return overview


class Pattern(object):
    # +++ csr1000v-1: configure command 'config-register 0x2102' +++
    pattern_command = re.compile(r'^\+\+\+ (?P<device>\S+)\: '
                    '(?P<execute_type>(executing|execute|configure)) command '
                    '\'(?P<title>[\s\S]+)\' \+\+\+$')

    # +++ PE1: config +++
    pattern_config_ping = re.compile(r'^\+\+\+ (?P<device>\S+)\: '
                                     '(?P<execute_type>(config|ping)) \+\+\+$')

    pattern_ping_ip = re.compile(r'^Target IP address: (?P<ip>[\d\.]+)$')


class LogSection(collections.UserDict):

    def __init__(self, archive, section, host, result_id=''):
        self.data = section
        self.archive = archive
        self.log_start = int(self.get('log_start', 0))
        self.log_size = int(self.get('log_size', -1))
        if self.get('log_file'):
            self.logfile = str(self.archive.dir / self.get('log_file'))
        else:
            self.logfile = ''
        self.host = host
        if ADVERTISED_URL and result_id:
            self.data['light_logviewer_url'] = \
                "{}light-logviewer/results/{}/section/{}".format(
                    ADVERTISED_URL, result_id, self.data.get('id','')
                )

    def _has_line_prefix(self, line):
        if self.host in line and len(line.split(': ')) > 4:
            return True
        else:
            return False

    def _get_time(self, line):
        try:
            return line.split(': ')[2].split('T')[1]
        except:
            return None

    async def get_robot_log_content(self, offset, limit):
        section = self.data
        log_file = str(self.archive.dir / "output.xml")
        loop = asyncio.get_event_loop()
        try:
            from lxml import etree
        except:
            logger.error("Optional package 'lxml' is not found. \n"
                         "To view robot result, please run 'pip install lxml'.")
            raise

        with concurrent.futures.ThreadPoolExecutor() as pool:
            root = await loop.run_in_executor(pool, 
                                              partial(etree.parse, 
                                              log_file))
        content = []
        if section["section_type"] == 'testscript':
            messages = root.xpath('suite/test/kw/msg')
            for msg in messages:
                    message = msg.text
                    time = msg.attrib['timestamp']
                    level = msg.attrib['level']
                    content.append((time, level, message))
        
        if section["section_type"] == 'testcase':
            messages = root.xpath('suite/test/kw/msg')
            for msg in messages:
                if msg.getparent().getparent().attrib['id'] == \
                                                        section["section_id"]:
                    message = msg.text
                    time = msg.attrib['timestamp']
                    level = msg.attrib['level']
                    content.append((time, level, message))

        if section["section_type"] == 'testsection':
            messages = root.xpath('suite/test/kw/msg')
            for msg in messages:
                if msg.getparent().getparent().attrib['id'] == \
                    section["parent_id"] and \
                    msg.getparent().attrib['name'] == section["section_name"]:
                        message = msg.text
                        time = msg.attrib['timestamp']
                        level = msg.attrib['level']
                        content.append((time, level, message))
        if limit == -1:
            result = content[offset:]
        elif offset+limit >= len(content):
            result = content[offset:len(content)]
        else:
            result = content[offset:offset+limit]
        return {"count": len(content), "file_content": result}

    @property
    @alru_cache()
    async def child_execute(self):
        '''
        finds all api calls from this log file
        this api call is cached for performance
        '''
        child_execute = {}

        cur_log_obj = None
        await self.archive.extract_archive()
        meta = self.archive.results.results.get('meta',{})
        if meta.get("result_format") == 'robot':
            file_content_list = await self.get_robot_log_content(0, -1)
            logs = []
            for item in file_content_list['file_content']:
                logs.extend(item[-1].split('\n'))
        else:
            async with aiofiles.open(self.logfile, 'r', newline='\n') as f:
                # seek the beginning of the section
                await f.seek(self.log_start)
                logs = await f.readlines(self.log_size)
        for line_no, line in enumerate(logs):
            line = line.strip()

            # End of LogExecute
            if isinstance(cur_log_obj, LogExecute) and \
                    self._has_line_prefix(line):
                cur_log_obj.end_line = line_no
                cur_log_obj.stop_time = self._get_time(line)
                if not hasattr(cur_log_obj, 'title'):
                    if cur_log_obj.end_line - cur_log_obj.start_line <= 10:
                        cur_log_obj.logs = ''.join(logs[
                            cur_log_obj.start_line:
                            cur_log_obj.end_line]).rstrip()
                    else:
                        cur_log_obj.logs = ''.join(
                            logs[cur_log_obj.start_line:
                                    cur_log_obj.start_line + 10]) \
                            + '(truncate)'
                child_execute[cur_log_obj.execute_id] = cur_log_obj
                cur_log_obj = None

            if isinstance(cur_log_obj, LogExecute) \
                    and cur_log_obj.execute_type == 'ping' \
                    and not hasattr(cur_log_obj, 'title'):
                m = Pattern.pattern_ping_ip.match(line)
                if m:
                    cur_log_obj.title = m.groupdict()['ip']
                continue

            # Start of LogExecute
            if '+++' in line and self._has_line_prefix(line):
                line_mini = line[line.find(']: ')+3:]

                # Start of '+++ device: config +++'
                # Start of '+++ device: ping +++'
                m = Pattern.pattern_config_ping.match(line_mini)
                if not m:
                    # Start of '+++ device: executing command 'xxx' ...'
                    m = Pattern.pattern_command.match(line_mini)
                if m:
                    start_time = self._get_time(line)
                    group = m.groupdict()
                    cur_log_obj = LogExecute(
                        archive=self.archive,
                        start_line=line_no,
                        start_time=start_time,
                        logfile=self.logfile,
                        parent_id=self.get('section_id'),
                        execute_id=str(uuid.uuid3(
                            uuid.NAMESPACE_X500, self.logfile+str(line_no))),
                        section_log_start=self.log_start,
                        section_log_size=self.log_size,
                        **group)

        return child_execute

    async def all_executions(self):
        executions = await self.child_execute
        return [i.to_json() for i in executions.values()]

    async def get_execution(self, execution_uuid):
        execution = await self.child_execute
        return execution.get(execution_uuid)

    async def read_logs(self, offset=0, limit=0):
        meta = self.archive.results.results.get('meta',{})
        if meta.get("result_format") == 'robot':
            return await self.get_robot_log_content(offset=offset, limit=limit)
        if not self.logfile:
            raise Exception(
                "Section {} doesn't have a logfile.".format(self['id']))
        return await self.archive.read_bytes(self.logfile,
                                             self.log_start, self.log_size,
                                             offset=offset, limit=limit)

    async def read_log_lines(self, offset=None, limit=None):
        if not self.logfile:
            raise Exception(
                "Section {} doesn't have a logfile.".format(self['id']))
        return await self.archive.read_lines(self.logfile,
                                             log_start=self.log_start,
                                             limit=limit,
                                             offset=offset,
                                             log_size=self.log_size)

    def __hash__(self):
        '''required for functools to hash the self argument for lru caching'''
        return id(self)


class LogExecute(object):
    def __init__(self, archive, **kwargs):
        self.archive = archive
        for key_args in kwargs:
            setattr(self, key_args, kwargs[key_args])
        self._format_type()

    def _format_type(self):
        type_formatter = {
            'executing': 'execute',
            'configure': 'config'
        }
        if hasattr(self, 'execute_type') and \
           self.execute_type in type_formatter:
            self.execute_type = type_formatter[self.execute_type]

    def to_json(self):
        serialize_key = ['execute_id', 'title', 'execute_type',
                         'device', 'start_time', 'logs']
        ret = {attr_name: getattr(self, attr_name)
               for attr_name in serialize_key if hasattr(self, attr_name)}
        return ret
    
    async def read_logs(self):
        return await self.archive.read_lines(self.logfile,
                                      offset=self.start_line, 
                                      limit=self.end_line-self.start_line,
                                      log_start=self.section_log_start,
                                      log_size=self.section_log_size)
