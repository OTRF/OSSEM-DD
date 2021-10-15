import pandas as pd, requests, yaml
pd.set_option('display.max_colwidth', None)
# Sysmon Linux events
sysmon_events = [1,3,4,5,9,11,16,23]
# Defining difference list to store data
difference_list = []
for event in sysmon_events:
    # Getting OSSEM dictionaries data
    url_sysmon_linux = 'https://raw.githubusercontent.com/OTRF/OSSEM-DD/main/linux/sysmon/events/event-' + str(event) + '.yml'
    url_sysmon_windows = 'https://raw.githubusercontent.com/OTRF/OSSEM-DD/main/windows/sysmon/events/event-' + str(event) + '.yml'    
    dict_linux = yaml.safe_load(requests.get(url_sysmon_linux).text)
    dict_windows = yaml.safe_load(requests.get(url_sysmon_windows).text)
    event_fields_linux = dict_linux.get('event_fields')
    event_fields_windows = dict_windows.get('event_fields')
    # Getting Windows event fields names
    event_fields_names_windows = []
    for event_field_windows in event_fields_windows:
        event_fields_names_windows.append(event_field_windows.get('name'))
    # Getting metadata of Linux event fields that are not in Windows
    for event_field_linux in event_fields_linux:
        if event_field_linux.get('name') not in event_fields_names_windows:
            difference_data = {}
            difference_data.update({'event_code':dict_linux.get('event_code')})
            difference_data.update({'event_name':dict_linux.get('title').split(':')[1]})
            difference_data.update({'field_name':event_field_linux.get('name')})
            difference_data.update({'field_description':event_field_linux.get('description')})
            difference_data.update({'field_sample':event_field_linux.get('sample_value')})
            # Adding dictionary with metadata to list
            difference_list.append(difference_data)
# Creating a dataframe
difference_dataframe = pd.DataFrame(difference_list)
print(difference_dataframe)