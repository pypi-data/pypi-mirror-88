"""Common verification functions for class-of-service"""

# Python
import re
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_chassis_fpc_slot_state(device, expected_state, 
                                  expected_slot=None, 
                                  all_slots=False, 
                                  environment=False,
                                  max_time=60, 
                                  check_interval=10):
    """ Verifies slot state via 
            - show chassis fpc
            - show chassis environment fpc

    Args:
        device (obj): Device object
        expected_state (list): Expected state of that slot. For example: ["Offline", "Online"].
        expected_slot (str, optional): Expected slot to check. For example: "0".
        all_slots(bool, optional): Flag that indicate all slots need to be verified. Defaults to False.
        environment(bool, optional): Flag that indicate different show commands. Defaults to False. 
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            if environment:
                out = device.parse("show chassis environment fpc")
            else:
                out = device.parse('show chassis fpc')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # Sample outputs:
        # 
        # show chassis fpc:
        # 'fpc-information': {
        #       'fpc': [{'slot': '0', 
        #       'state': 'Offline'}]

        # show chassis environment fpc:
        # {'environment-component-information': {
        #     'environment-component-item': [
        #         {
        #             'name': 'FPC 0',
        #             'state': 'Online', <-----------------
        #             ...

        
        fpc_list = out.q.contains('slot|state', regex=True).get_values('fpc')
        
        # Verify all slot have the same expected_state
        if all_slots:
            states_set = set(out.q.get_values('state'))
            if states_set.issubset(set(expected_state)):
                return True
            
        # Verify given slot has the expected_state
        else:
            # show chassis environment fpc
            if environment:
                items = out.q.get_values("environment-component-item", None)

                for i in items:
                    slot_pattern = re.compile(r'FPC +(?P<slot>\d+)')
                    slot_match = slot_pattern.match(i['name'])

                    if slot_match:
                        if slot_match.groupdict()['slot'] == expected_slot and i['state'] in expected_state:
                            return True
                    
            
            # show chassis fpc
            else:
                for fpc in fpc_list:
                    slot = fpc.get('slot')
                    state = fpc.get('state')

                    if slot == expected_slot and state in expected_state:
                        return True

        timeout.sleep()
        
    return False

def verify_chassis_re_state(device,
                       expected_re_state,
                       max_time=60,
                       check_interval=10,):
    """ Verify output of show chassis routing-engine ends as expected state

        Args:
            device (`obj`): Device object
            expected_re_state (`str`): Expected end of output state
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis routing-engine')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # "route-engine-information": {
        #             "route-engine": [{
        #                   "mastership-state": "Master",
        #                    ...
        #              },
        #              {
        #                   "mastership-state": "Backup",
        #              }]
        #              "re-state": {master}

        re_state = output.q.get_values('re-state')
        if expected_re_state in re_state:
            return True

        timeout.sleep()
    return False


def verify_chassis_slots_present(device,
                                 expected_slots,
                                 invert=False,
                                 max_time=60,
                                 check_interval=10,):
    """ Verify slots present in 'show chassis routing-engine'

        Args:
            device (`obj`): Device object
            expected_slots (`list`): Given slots
            invert ('bool', 'optional'): Inverts to check if it doesn't exist
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis routing-engine')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        # "route-engine-information": {
        #     "route-engine": [{
        #         ...
        #         "model": "RE-VMX",
        #         "slot": "0", <------------------
        #         "start-time": {
        #             "#text": "2019-08-29 09:02:22 UTC"
        #         },

        slots = output.q.get_values('slot')
        
        if not invert:
            # check if 'slots' has all elements in 'expected'
            if all(i in slots for i in expected_slots):
                    return True

            timeout.sleep()
        else:
            for slot in slots:
                if str(slot) == expected_slots:
                    timeout.sleep()
                    continue
            return True

    return False


def verify_chassis_slot_state(device,
                              expected_slots_states_pairs,
                              max_time=60,
                              check_interval=10,):
    """ Verify slot's state in 'show chassis routing-engine'

        Args:
            device (`obj`): Device object
            expected_slots_states_pairs (`dict`): Expected states with given slots. E.g.,{'slot1':'state1', 'slot2':'state2'}
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show chassis routing-engine')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        # "route-engine-information": {
        #     "route-engine": [{
        #         ...
        #         "model": "RE-VMX",
        #         "mastership-state": "Master",   <------------------    
        #         "slot": "0", <-----------------
        #         "start-time": {
        #             "#text": "2019-08-29 09:02:22 UTC"
        #         },

        rout=Dq(out).contains('slot|mastership-state',regex=True).reconstruct()
        # rout example:
        # {'route-engine-information': {'route-engine': 
        #                                   [{'mastership-state': 'Master',
        #                                         'slot': '0'},
        #                                    {'mastership-state': 'Backup',
        #                                         'slot': '1'}]}}

        route_engines = Dq(rout).get_values('route-engine')
        # 'route_engines' example:
        # [{'mastership-state': 'Master', 'slot': '0'}, 
        # {'mastership-state': 'Backup', 'slot': '1'}]

        # 'expected_slots_states_pairs' example:
        # {'0':'master', '1':'backup'} 
        for i in route_engines:
            if i['slot'] in expected_slots_states_pairs and \
                i['mastership-state'].lower() == expected_slots_states_pairs[i['slot']].lower():
                return True

        timeout.sleep()
    return False

def verify_chassis_fan_tray_present(device,
                                    fan_tray_list,
                                    max_time=60,
                                    check_interval=10,):
    """ Verify fan_tray_list is present in 'show chassis hardware'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        #         "chassis-inventory": {
        #             "chassis": {
        #                 "@junos:style": "inventory",
        #                 "chassis-module": [
        #                     {
        #                         "name": "Midplane" <--------------------
        #                     },
        #                     {
        #                         "description": "RE-VMX",
        #                         "name": "Routing Engine 0"

        modules = output.q.get_values('chassis-module', None)
        if modules:
            names = [i['name'] for i in modules]

        # check if all items in fan_tray_list appears in names
        # >>> l1=[1,2]
        # >>> l2=[1,2,3,4]
        # >>> all(i in l2 for i in l1)
        # True
        # >>> all(i in l1 for i in l2)
        # False       
         
        if all(i in names for i in fan_tray_list):
            return True
        else:
            timeout.sleep()
            continue
        
    return False    

def verify_chassis_environment_present(device,
                                       fan_tray_list,
                                       expected_status,
                                       max_time=60,
                                       check_interval=10,):
    """ Verify all item in fan_tray_list have expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            expected_status (`str`): Expected status
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            return None

        # fan_tray_list:
        #     - Fan Tray 0
        #     - Fan Tray 1
        #     - Fan Tray 2
        #     - Fan Tray 3        

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-item', None)

        if environment_items_list:
            for item in environment_items_list:
                
                # >>> name
                # 'Fan Tray 0 Fan 2'
                # >>> m=re.search('(.+?) +Fan +\d+',name).group(1)
                # >>> m
                # 'Fan Tray 0'   
                head_of_string = re.search('(.+?) +Fan +\d+',item['name']).group(1)  

                if head_of_string in fan_tray_list:
                    if item['status'] != expected_status:
                        return False

        timeout.sleep()
    return True      

def verify_chassis_no_alarms(device, 
                             max_time=60, 
                             check_interval=10):
    """ Verify there are no alarms via 'show chassis alarms'

        Args:
            device (`obj`): Device object
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        try:
            output = device.execute('show chassis alarms')
            if 'No alarms currently active' in output:
                return True
        except Exception:
            timeout.sleep()
            continue
        timeout.sleep()
    return False


def verify_chassis_routing_engine(device,
                                  expected_item,
                                  invert=False,
                                  max_time=60,
                                  check_interval=10,):
    """ Verify fan_tray_list is present in 'show chassis hardware'

        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            invert ('bool'): Invert function
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            return None

        # Sample output
        # {
        #         "chassis-inventory": {
        #             "chassis": {
        #                 "@junos:style": "inventory",
        #                 "chassis-module": [
        #                     {
        #                         "name": "Midplane" <--------------------
        #                     },
        #                     {
        #                         "description": "RE-VMX",
        #                         "name": "Routing Engine 0"

        modules = output.q.get_values('chassis-module', None)
        if modules:
            names = [i['name'] for i in modules]

        if not invert:
            for name in names:
                if name == expected_item:
                    return True
        else:
            for name in names:
                if name == expected_item:
                    timeout.sleep()
                    continue
            return True
        timeout.sleep()
    return False


def verify_chassis_hardware_item_present(device,
                            expected_item,
                            max_time=60,
                            check_interval=10):
    """ Verify fan_tray_list is present in 'show chassis hardware'

        Args:
            device (`obj`): Device object
            expected_item (`list`): Item name
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis hardware')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        # {
        #         "chassis-inventory": {
        #             "chassis": {
        #                 "@junos:style": "inventory",
        #                 "chassis-module": [
        #                     {
        #                         "name": "Midplane" <--------------------
        #                     },
        #                     {
        #                         "description": "RE-VMX",
        #                         "name": "Routing Engine 0"

        item_list = output.q.contains(expected_item).get_values('name')
        if expected_item in item_list:
            return True
        timeout.sleep()
    return False


def verify_chassis_environment_component_present(device,
                                        name,
                                       component_list,
                                       expected_status,
                                       max_time=60,
                                       check_interval=10,):
    """ Verify all item in fan_tray_list have expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            expected_status (`str`): Expected status
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        try:
            output = device.parse('show chassis environment {name}'.format(
                name=name
            ))
        except SchemaEmptyParserError:
            result = False

        # fan_tray_list:
        #     - Fan Tray 0
        #     - Fan Tray 1
        #     - Fan Tray 2
        #     - Fan Tray 3        

        # Sample output:
        # {'environment-information': {'environment-component-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-component-item', None)
        
        if environment_items_list:
            for item in environment_items_list:
                
                name_ = item.get('name', None)
                state_ = item.get('state', None)

                if name_ in component_list and state_ != expected_status:
                    result = False
                    break
        if result:
            return True
        timeout.sleep()
    return False

def verify_chassis_power_item_present(device,
                                       component_list,
                                       expected_status,
                                       max_time=60,
                                       check_interval=10):
    """ Verify all item in fan_tray_list have expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            fan_tray_list (`list`): Given fan tray list
            expected_status (`str`): Expected status
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        try:
            output = device.parse('show chassis power')
        except SchemaEmptyParserError:
            result = False

        power_usage_item_list = output.contains('{}|name'.format(
            expected_status, 
        ), regex=True).get_values('power-usage-item')
        
        if power_usage_item_list:
            for item in power_usage_item_list:
                
                name_ = item.get('name', None)
                state_ = item.get('state', None)

                if name_ in component_list and state_ != expected_status:
                    result = False
                    break
        if result:
            return True
        timeout.sleep()
    return False


def verify_chassis_environment_status(device,
                                      expected_item,
                                      expected_status,
                                      max_time=60,
                                      check_interval=10,):
    """ Verify specific item in fan_tray_list has expected_status in 'show chassis environment'

        Args:
            device (`obj`): Device object
            expected_item (`str`): Hardware inventory item expected
            expected_status (`str`): Expected status
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:

            output = device.parse('show chassis environment')
        except SchemaEmptyParserError:
            return None      

        # Sample output:
        # {'environment-information': {'environment-item': [
        #                                          {'class': 'Fans',
        #                                            'comment': '2760 RPM',
        #                                            'name': 'Fan Tray 0 Fan 1', <---------------
        #                                            'status': 'OK'}, <--------------------------
        #                                           {'class': 'Fans',
        #                                            'comment': '2520 RPM',
        #                                            'name': 'Fan Tray 0 Fan 2',
        #                                            'status': 'OK'},]}}
        environment_items_list = output.q.get_values('environment-item', None)

        if environment_items_list:
            for item in environment_items_list:
                if item['name'] == expected_item and item['status'] == expected_status:
                    return True

        timeout.sleep()
    return True      


def verify_chassis_alarm_output(device,
                                message_topic,
                                invert=False,
                                max_time=60, 
                                check_interval=10):
    """ Verify message_topic is mentioned via 'show chassis alarms'

        Args:
            device (`obj`): Device object
            message_topic ('str'): Message information that should be in output
            invert ('bool'): Invert function
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            if invert:
                return True
            timeout.sleep()
            continue

        #"alarm-detail": {
        #        "alarm-class": "Major",
        #        "alarm-description": "PSM 15 Not OK",
        #        "alarm-short-description": "PSM 15 Not OK",
        #        "alarm-time": {
        #            "#text": "2020-07-16 13:38:21 EST",
        #        },
        #        "alarm-type": "Chassis"
        #    },
        #    "alarm-summary": {
        #        "active-alarm-count": "1"
        #    }
        
        alarm_description = output.q.get_values('alarm-description', {})

        if not invert:
            if message_topic in alarm_description:
                return True
            timeout.sleep()
        else:
            if message_topic not in alarm_description:
                return True
            timeout.sleep()

    return False

def verify_chassis_usb_flag_exists(device, 
                                   flag,
                                   usb,
                                   invert=False,
                                   max_time=60, 
                                   check_interval=10):
    """ Verify there is/isn't usb flag in given usb in the routing engine via show chassis hardware detail

        Args:
            device (`obj`): Device object
            flag (`str`): USB flag description in output,
            usb (`str`): USB name in output,,
            invert (`bool`, optional): Used to indicate a reverse verification. default: False
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:            
            out = device.parse('show chassis hardware detail')
        except SchemaEmptyParserError:
            return None

        # usb: USB
        # usb_insert_flag: umass
        # 
        # {
        #     "chassis-inventory": {
        #         "chassis": {
        #             "chassis-module": [
        #                 {
        #                     'chassis-re-usb-module': [{'description': 'umass0', <-----------usb_insert_flag
        #                                                 'name': 'usb0 ' <------------- usb
        #                                                         '(addr '
        #                                                         '1)',
        #                                                 'product': 'EHCI '
        #                                                             'root '
        #                                                             'hub',
        #                                                 'product-number': '0',
        #                                                 'vendor': 'Intel'}]}
        
        chassis_module_list = out.q.get_values("chassis-module", 0)


        for module in chassis_module_list:
            if 'chassis-re-usb-module' in module:
                usb_module_list = module['chassis-re-usb-module']

                for usb_module in usb_module_list:
                    # check if current usb_module has name starts with 'usb'
                    # usb_name: 'usb0 (addr 1)'
                    # usb: 'USB'
                    usb_name = usb_module['name']

                    if usb.lower() in usb_name:
                        # check if current usb_module has the usb_insert_flag
                        usb_description = usb_module['description']
                    
                        if flag in usb_description:
                            if invert:
                                return False
                            else:
                                return True
                        
                        timeout.sleep()
                        continue
            timeout.sleep()
        if invert:
            return True
        else:
            return False            


def verify_chassis_alarms_no_error(device, 
                                   target_fpc,
                                   max_time=60, 
                                   check_interval=10):
    """ Verify there are no error about target FPC via 'show chassis alarms'

        Args:
            device (`obj`): Device object
            target_fpc (`str`): Target fpc. 
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show chassis alarms')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        errored_pattern = re.compile(r'FPC (?P<slot>\d+) offline due to unreachable destinations')

        # Sample output
        #     {
        #     "alarm-information": {
        #         "alarm-detail": {
        #             "alarm-class": "Major",
        #             "alarm-description": "FPC 15 Not OK", <--------------------------
        #             "alarm-short-description": "FPC 15 Not OK",
        #             "alarm-time": {
        #                 "#text": "2020-07-16 13:38:21 EST",
        #             },
        #             "alarm-type": "Chassis"
        #         },
        #         "alarm-summary": {
        #             "active-alarm-count": "1"
        #         }
        #     },
        # }

        description = output.q.get_values('alarm-description', None)

        if errored_pattern.match(description):
            return True

        timeout.sleep()
    return False