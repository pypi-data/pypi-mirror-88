"""REDCap extensions to CDISC ODM schema"""

from dataforge.schema.cdisc_odm import schema

@schema.define
class GlobalVariables:
    def __init__(self,
                 study_names = [],
                 redcap_repeating_instruments_and_eventses = []):
        self.study_names = study_names
        self.redcap_repeating_instruments_and_eventses = redcap_repeating_instruments_and_eventses

@schema.define
class redcap_RepeatingInstrumentsAndEvents:
    def __init__(self,
                 redcap_repeating_events = [],
                 redcap_repeating_instrumentses = []):
        self.redcap_repeating_events = redcap_repeating_events
        self.redcap_repeating_instrumentses = redcap_repeating_instrumentses

@schema.define
class redcap_RepeatingEvent:
    def __init__(self,
                 redcap_unique_event_name):
        self.redcap_unique_event_name = redcap_unique_event_name

@schema.define
class redcap_RepeatingInstruments:
    def __init__(self,
                 redcap_repeating_instruments = []):
        self.redcap_repeating_instruments = redcap_repeating_instruments

@schema.define
class redcap_RepeatingInstrument:
    def __init__(self,
                 redcap_unique_event_name,
                 redcap_repeat_instrument,
                 redcap_custom_label):
        self.redcap_unique_event_name = redcap_unique_event_name
        self.redcap_repeat_instrument = redcap_repeat_instrument
        self.redcap_custom_label = redcap_custom_label

@schema.define
class MetaDataVersion:
    def __init__(self,
                 redcap_record_id_field,
                 protocols = [],
                 study_event_defs = [],
                 form_defs = [],
                 item_group_defs = [],
                 item_defs = []):
        self.redcap_record_id_field = redcap_record_id_field
        self.protocols = protocols
        self.study_event_defs = study_event_defs
        self.form_defs = form_defs
        self.item_group_defs = item_group_defs
        self.item_defs = item_defs

@schema.define
class StudyEventDef:
    def __init__(self,
                 name,
                 redcap_unique_event_name,
                 form_refs = []):
        self.name = name
        self.redcap_unique_event_name = redcap_unique_event_name
        self.form_refs = form_refs

@schema.define
class FormRef:
    def __init__(self,
                 form_oid,
                 redcap_form_name):
        self.form_oid = form_oid
        self.redcap_form_name = redcap_form_name

@schema.define
class FormDef:
    def __init__(self,
                 oid,
                 name,
                 redcap_form_name,
                 item_group_refs = []):
        self.oid = oid
        self.name = name
        self.redcap_form_name = redcap_form_name
        self.item_group_refs = item_group_refs

@schema.define
class ItemDef:
    def __init__(self,
                 oid,
                 name,
                 data_type,
                 length,
                 redcap_variable,
                 redcap_field_type):
        self.oid = oid
        self.name = name
        self.data_type = data_type
        self.length = length
        self.redcap_variable = redcap_variable
        self.redcap_field_type = redcap_field_type
