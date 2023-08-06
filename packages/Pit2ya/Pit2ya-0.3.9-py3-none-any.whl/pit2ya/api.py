import asyncio
from datetime import datetime
from pit2ya.db import get_data, set_data
from pit2ya.toggl_wrap import begin_timer_raw

#local = datetime.timezone(#TODO

def user_start():
    from iterfzf import iterfzf
    desc_list = get_data()
    query, desc = iterfzf(desc_list, print_query=True, extended=True)
    if desc:
        begin_timer_raw(desc, desc_list.timers[desc]['pid'])
        print(f"'{desc}'ing since {datetime.now().strftime('%H:%M:%S')}")
    else:
        return    # TODO: collect project information, allow creating new time entries
    set_data(desc_list, desc)

def user_modify():
    from iterfzf import iterfzf
    desc_list = get_data()
    query, desc = iterfzf(desc_list, print_query=True, extended=True)
    from toggl.api import TimeEntry
    cur = TimeEntry.objects.current()
    print(cur.start)
    if cur is None:
        print(f'No current running timer! starting {desc}..')
        begin_timer_raw(desc, desc_list.timers[desc]['pid'])
    elif desc:
        print(f"'{desc}'ing since {cur.start.strftime('%H:%M:%S')}")
        setattr(cur, 'description', desc)
        setattr(cur, 'project', desc_list.timers[desc]['pid'])
        cur.save()
    elif query:       # create a whole new timer
        print('Creating new timer', query, 'with current details...')
        desc_list.timers[query] = { 'pid': int(cur.pid or -1) }
        desc = query
        setattr(cur, 'description', desc)
        cur.save()
    else:
        print('No input! Abort.')
        return
    set_data(desc_list, desc)

