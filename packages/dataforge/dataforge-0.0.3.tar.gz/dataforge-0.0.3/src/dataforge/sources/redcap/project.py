"""Utilities for manipulating data from a REDCap project"""

from dataforge.sources.redcap.schema import schema
import pandas as pd
import glob
import os
import re

class REDCapProject:
    
    def __init__(self, project_name='', path='tmp/redcap'):
        
        last_export = self._last_export(project_name, path)
        if not last_export:
            raise Exception('No REDCap exports found')
        if project_name:
            project_name = project_name + '_'
        base = os.path.join(path, project_name)
        
        try:
            datafile = f'{base}DATA_LABELS_{last_export}.csv'
            # We use the Python engine here because it handles embedded newlines
            data = pd.read_csv(datafile, engine='python', dtype='object',
                               keep_default_na=False)
        except FileNotFoundError:
            print(f'Error reading REDCap data file: {datafile}')
            raise
        
        try:
            metafile = f'{base}{last_export}.REDCap.xml'
            with open(metafile) as f:
                metadata = schema.parse(f.read()).studies[0]
        except FileNotFoundError:
            print(f'Error reading REDCap metadata file: {metafile}')
            raise
        
        self.global_vars = metadata.global_variableses[0]
        self.metadata = metadata.meta_data_versions[0]
        self.record_id = self.metadata.redcap_record_id_field
        self.data = data.set_index(self.record_id)
        self.events = self._get_events()
        self.forms = self._get_forms()
    
    def _last_export(self, project_name, path):
        """Return datetime of last REDCap export"""
        
        if project_name:
            project_name = project_name + '_'
        files = sorted(glob.glob(f'{os.path.join(path, project_name)}*'))
        if files:
            s = re.search(r'([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{4})\.csv$', files[-1])
            if s:
                return s.group(1)
    
    def _get_items(self):
        """Return dicionary of items indexed by OID"""
        
        items = {}
        for item_def in self.metadata.item_defs:
            items[item_def.oid] = REDCapItem(item_def)
        return items
    
    def _get_item_groups(self):
        """Return dicionary of item groups indexed by OID"""
        
        items = self._get_items()
        item_groups = {}
        for item_group_def in self.metadata.item_group_defs:
            item_groups[item_group_def.oid] = []
            for item_ref in item_group_def.item_refs:
                item_groups[item_group_def.oid].append(items[item_ref.item_oid])
        return item_groups
    
    def _get_events(self):
        """Return dictionary of events indexed by REDCap unique event name
        
        Will be empty for non-longitudinal studies.
        """
        
        events = {}
        for study_event_def in self.metadata.study_event_defs:
            event = REDCapEvent(study_event_def, self.global_vars \
                                .redcap_repeating_instruments_and_eventses[0])
            events[study_event_def.redcap_unique_event_name] = event
        return events
    
    def _get_forms(self):
        """Return dictionary of all forms indexed by form name"""
        
        forms = {}
        item_groups = self._get_item_groups()
        
        try:
            repeating_instruments = self.global_vars.redcap_repeating_instruments_and_eventses[0] \
                                        .redcap_repeating_instrumentses
        except (AttributeError, IndexError):
            repeating_instruments = []
        
        data = self.data.reindex()
        
        for form_def in self.metadata.form_defs:
            repeat_events = {}
            for instruments in repeating_instruments:
                for instrument in instruments.redcap_repeating_instruments:
                    label = instrument.redcap_custom_label[1:-1]
                    if instrument.redcap_repeat_instrument==form_def.redcap_form_name:
                        repeat_events[instrument.redcap_unique_event_name] = label
            
            forms[form_def.name] = REDCapForm(form_def, item_groups, self.events,
                                              repeat_events, self.data)
        return forms

class REDCapEvent:
    
    def __init__(self, study_event_def, repeating_instruments_and_events):
        
        self.name = study_event_def.name
        self.unique_name = study_event_def.redcap_unique_event_name
        self.forms = set()
        for form_ref in study_event_def.form_refs:
            self.forms.add(form_ref.form_oid)
        
        self.repeat = False
        for event in repeating_instruments_and_events.redcap_repeating_events:
            if event.redcap_unique_event_name==self.unique_name:
                self.repeat = True
                break

class REDCapForm:
    """A REDCap form
    
    Note that we intentionally collapse over item groups when creating the
    list of items, since the metadata lost (i.e., sections and matrices) is
    not typically necessary for creating data products and the result is
    considerably simpler.
    
    Repeat events is a dictionary indexed by the events within which the form
    repeats, with the entries containing the variable used to index individual
    instances of the form.
    """
    
    def __init__(self, form_def, item_groups, events, repeat_events, data):
        self.name = form_def.name
        self.items = []
        for item_group_ref in form_def.item_group_refs:
            self.items.extend(item_groups[item_group_ref.item_group_oid])
        self.events = set()
        for event in events:
            if form_def.oid in events[event].forms:
                self.events.add(events[event].name)
        self.repeat = repeat_events
        self.data = self._get_form_data(data)
    
    def _get_form_data(self, data):
        """Return data frame containing form data"""
        
        if 'redcap_event_name' in data.columns:
            form_data = data.loc[data['redcap_event_name'].isin(self.events)]
            # TODO Handle case where events have been given custom labels
            form_data.set_index('redcap_event_name', append=True, inplace=True)
        else:
            form_data = data
        
        # TODO Handle repeating forms and verify resulting index is unique
        
        # N.B. Make sure to handle case where repeating instruments have been
        # given custom labels
        
        # Are there situations in which the data may not contain all of the vars?
        form_data = form_data[[item.oid for item in self.items
                               if item.varname in form_data.columns]]
        # form_data = form_data[[item.oid for item in self.items
        #                        if item.varname not in form_data.index.names]]
        return form_data.sort_index()

class REDCapItem:
    
    def __init__(self, item_def):
        
        self.oid = item_def.oid
        self.name = item_def.name
        self.data_type = item_def.data_type
        self.length = item_def.length
        self.varname = item_def.redcap_variable
        self.field_type = item_def.redcap_field_type
