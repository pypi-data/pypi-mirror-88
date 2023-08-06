import yaml
import asyncio
import concurrent
from functools import partial
from .base_parser import BaseResultsParser

# from yaml import Loader
# from collections import OrderedDict
# _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


# def dict_constructor(loader, node):
#     return OrderedDict(loader.construct_pairs(node))

# Loader.add_constructor(_mapping_tag, dict_constructor)

class KleenexParser(BaseResultsParser):

    def get_yaml_data(self):
        with open(str(self.archive.dir / 'CleanResultsDetails.yaml'), 'r') as f:
            if hasattr(yaml, 'CLoader'):
                return yaml.load(f, yaml.CLoader)
            else:
                return yaml.safe_load(f)

    async def parse(self):
        """ 
        Parse output.xml file in the given archive

        The parsed result contains 3 main sections:
        'meta': Info about the job/suite itself
        'scripts': Info about each script (and it's sections)
        'summary': Summary of the results for that job

        The parsed results is stored in self.results
        """
        # Parse CleanResultsDetails.yaml
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            dataMap = await loop.run_in_executor(pool, 
                                                 partial(self.get_yaml_data))

        # Parse the meta section (suite info)
        self._parse_job_info(dataMap, 'kleenex')
        # Parse all internal sections of the suite (tests and their keywords)
        self._parse_job(dataMap)
        # Parse the suite summary
        self._parse_job_summary(dataMap)

        return super().parse()

    def _parse_job_summary(self, element):
        """
        Parse job summary.

        Parameters
        ----------
        element: yaml content
        Return
        ------
        None
        """
        summary = self._parse_summary(element['summary'])
        self.results['summary'] = summary

    def _parse_summary(self, summary_element):
        """
        """
        summary = {'abort': 0,
                   'applicable_tasks': 0,
                   'block': 0,
                   'error': 0,
                   'fail': 0,
                   'never_ran': 0,
                   'pass': 0,
                   'passx': 0,
                   'skip': 0,
                   'total_tasks': 0,
                   'unknown': 0}

        summary['pass'] = summary_element['pass']
        summary['fail'] = summary_element['fail']
        summary['total_tasks'] = summary_element['total']
        summary['applicable_tasks'] = summary['total_tasks']
        return summary

    def _parse_job_info(self, dataMap, _format):
        """
        Parse the job information. This includes:

        suite_name 
        result_id 
        submitter 
        testbed 
        run_time 
        start_time 
        stop_time 
        ats_tree 
        archive_location 
        exec_host

        Store the parsed info (in dict form) in self.results['meta']

        Parameters
        ----------
        dataMap:
            The dataMap element for starting the parsing
        _format:
            Parser type: kleenex
        Return
        ------
        None
        """

        job_info = dict()

        job_info['suite_name'] = ''
        job_info['result_id'] = self.result_id if self.result_id else \
            dataMap['initinfo']['resultid']
        job_info['result_format'] = _format
        job_info['submitter'] = dataMap['initinfo']['submitter'] if \
            dataMap['initinfo']['submitter'] else ""
        job_info['cli'] = dataMap['initinfo']['cli']
        job_info['start_time'] = dataMap['starttime']
        job_info['stop_time'] = dataMap['stoptime']
        job_info['run_time'] = dataMap['runtime']
        job_info['testbed'] = dataMap['initinfo']['testbed_name'] if \
            'testbed_name' in dataMap['initinfo'] else ""
        job_info['ats_tree'] = ''
        job_info['exec_host'] = dataMap['initinfo']['host']
        job_info['archive_location'] = str(self.archive.file)

        job_info['related_id'] = self.related_id
        job_info['component'] = self.component
        job_info['branch'] = self.branch
        job_info['created_by'] = self.created_by
        job_info['job'] = job_info['suite_name']
        job_info['meta_info'] = self.meta_info

        self.results['meta'] = job_info

    def _parse_job(self, dataMap):
        """
        Parse the job contents. This means every script/task in that job.
        For every script/task, parse its info, its sections and its summary.
        Store these 3 pieces (of each script) as a dictionary:
        {'meta': <dict>,
         'scripts': <list of dicts>,
         'summary': <dict>
        }

        Make a list of those scripts/tasks

        Parameters
        ----------
        dataMap:
            The dataMap element for starting the parsing

        Return
        ------
        None
        """
        job_scope = True
        # Find all scripts/tasks 
        # (could be 0 or multiple depends on job scope or task scope)
        try:
            scripts = dataMap['tasks']
            # task scope
            job_scope = False
        except:
            try:
                testbed_name = dataMap['initinfo']['testbed_name']
                if not testbed_name:
                    # you should be never reaching here
                    testbed_name = "__dummy_testbed"
            except:
                # you should never reach here!
                testbed_name = "__dummy_testbed"
            scripts = {testbed_name: dataMap}

        # Initialize an empty list of scripts in results
        self.results['scripts'] = []

        # Parse each script: parse its info, its sections, and its summary
        for script in scripts:
            meta = self._parse_script_info(script)

            if not job_scope:
                sections = self._parse_script(script,
                                              dataMap['tasks'][script])
                summary = self._parse_script_summary(dataMap['tasks'][script])
            else:
                sections = self._parse_script(script,
                                              dataMap)
                summary = self._parse_script_summary(dataMap)

            self.results['scripts'].append({'meta': meta,
                                            'sections': sections,
                                            'summary': summary})

    def _parse_script_info(self, script):
        """
        """
        return {
            'task_id': script,
            'name':  script,
            'path':  "",
        }

    def _parse_script(self, task_id, task):
        """
        Each parsed record is added as a dictionary to a list containing
        all the script/task sections.

        Parameters
        ----------
        task: script/task element

        Return
        ------
        script_sections: list
            A list of script sections / devices. Each section/device is a 
            dictionary containing section_id, section_name, start_time, etc
        """

        script_sections = []

        # this is for entire script
        script_section = {}

        # Parse script itself as a section
        script_section['start_time'] = task['starttime']
        script_section['stop_time'] = task['stoptime']
        script_section['run_time'] = task['runtime']
        script_section['section_name'] = task_id
        script_section['section_id'] = task_id
        script_section['section_type'] = 'testscript'  # task
        script_section['log_file'] = task['logfile']['name']
        script_section['log_start'] = task['logfile']['begin']
        script_section['log_size'] = task['logfile']['size']
        script_section['log_start_line'] = task['logfile']['begin_lines']
        script_section['log_size_line'] = task['logfile']['size_lines']
        script_section['result'] = task['result']

        script_section['description'] = ""
        script_section['parent_id'] = None
        # script_section['parents'] = ['suite', ]
        script_section['parents'] = []
        script_section['source_file'] = ""
        script_section['source_line'] = 0
        self._sequence_number += 1
        script_section['sequence_number'] = self._sequence_number
        script_section['id'] = str(self._sequence_number)
        script_sections.append(script_section)

        # Parse test cases/devices
        for device in task['devices']:
            script_sections += self._parse_testcase(
                device,
                task['devices'][device],
                parent=script_section['id'],
                parents=script_section['parents'] +
                [script_section['sequence_number'], ]
            )
        return script_sections

    def _parse_testcase(self, device_id, device, parent='script', parents=None):
        """
        Parse all sections inside a testcase/device as follows:
        - Parse the testcase/device itself as a section
            - Parse each steps in the testcase

        Sequence_number is incremented accordingly.

        Each parsed record is added as a dictionary to a list containing
        all the testcase sections.

        Parameters
        ----------
        device: device element
        parent: str
            section_id of the direct parent of this testcase. By default
            it is 'script'
        parents: list
            An ordered list of the parents of this testcase. The list
            contains the section_id of each parent (as string)

        Return
        ------
        testcase_sections: list
            A list of testcase sections. Each section is a dictionary
            containing section_id, section_name, start_time, etc
        """

        testcase_sections = []

        # Parse the testcase itself as a section (in here is the device itself)
        testcase_section = self._parse_section(
            device_id,
            device,
            with_initinfo=True,
            parent=parent,
            section_type='testcase',
            parents=parents
        )
        testcase_sections.extend(testcase_section)

        return testcase_sections

    def _parse_section(self,
                       device_id,
                       element,
                       with_initinfo=False,
                       parent=None,
                       section_type='testsection',
                       parents=None):
        """
        This method operates at the lowest level of parsing. It is where the
        actual values of the fields are parsed. 
        Parameters
        ----------
        element: The element whose info is to be parsed
        with_initinfo: bool
            If True, certain fields need to be parsed from the initinfo
            section within the given element (instead of parsing directly
            under the element itself)
        parent: str
            section_id of the direct parent of the given element
        section_type: str
            The type of the section; could be: script, testcase, etc
        parents: list (of strings)
            An ordered list of the parents of the given element

        Return
        ------
        ret: dict
            A dictionary containing the parsed fields
        """
        ret = []
        sec = {}

        sec['parent_id'] = parent
        sec['start_time'] = element['starttime']
        sec['stop_time'] = element['stoptime']
        sec['run_time'] = element['runtime']
        sec['result'] = element['result']

        sec['parents'] = parents

        self._sequence_number += 1
        sec['sequence_number'] = self._sequence_number
        sec['id'] = str(self._sequence_number)
        sec.update(self._parse_init_info(
            device_id, element, section_type=section_type))

        ret.append(sec)

        try:
            for step in element.get('steps',{}):
                current_step = self._parse_step_info(step, 
                                                     element['steps'][step], 
                                                     sec)
                if current_step:
                    ret.append(current_step)
        except:
            pass
        return ret

    def _parse_step_info(self, step_id, element, parent_dict):
        """ Parse step
        """
        ret = {}
        try:
            step_name = element['name']
            ret['start_time'] = element['starttime']
            ret['stop_time'] = element['stoptime']
            ret['run_time'] = element['runtime']
            ret['result'] = element['result']
            self._sequence_number += 1
            ret['sequence_number'] = self._sequence_number
            ret['id'] = str(self._sequence_number)
            ret['section_name'] = step_name
            ret['section_id'] = step_name
            ret['parent_id'] = parent_dict.get('id')
            ret['parents'] = parent_dict['parents'] + [
                        parent_dict['sequence_number']]
            ret['log_file'] = element['logfile']['name']
            ret['log_start'] = element['logfile']['begin']
            ret['log_size'] = element['logfile']['size']
            ret['log_line_start'] = element['logfile']['begin_lines']
            ret['log_line_size'] = element['logfile']['size_lines']
#            ret['xref_file'] = element['xref']['file']
#            ret['xref_line'] = element['xref']['line']
            ret['source_file'] = ""
            ret['source_line'] = ""
            ret['section_type'] = 'step'

        finally:
            return ret

    def _parse_init_info(self, device_id, element, section_type='testsection'):
        """ Parse initinfo fields for each testsection
        """
        ret = {}
        ret['section_id'] = device_id
        ret['section_name'] = device_id
        ret['section_type'] = section_type
        ret['description'] = ""
        ret['log_file'] = element['logfile']['name']
        ret['log_start'] = element['logfile']['begin']
        ret['log_size'] = element['logfile']['size']
        ret['log_start_line'] = element['logfile']['begin_lines']
        ret['log_size_line'] = element['logfile']['size_lines']
        ret['source_file'] = ""
        ret['source_line'] = 0
        return ret

    def _parse_script_summary(self, element):
        """
        """
        summary = {'abort': 0,
                   'applicable_tasks': 0,
                   'block': 0,
                   'error': 0,
                   'fail': 0,
                   'never_ran': 0,
                   'pass': 0,
                   'passx': 0,
                   'skip': 0,
                   'total_tasks': 0,
                   'unknown': 0}

        summary['pass'] = element['summary']['pass']
        summary['fail'] = element['summary']['fail']
        summary['total_tasks'] = summary['pass'] + summary['fail']
        summary['applicable_tasks'] = summary['total_tasks']

        return summary
