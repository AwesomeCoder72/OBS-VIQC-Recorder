"""
Helpful links:
 - for starting the timer video:
 - - https://obsproject.com/docs/reference-sources.html?highlight=media#c.obs_source_info.media_play_pause
 - - 
"""
from obspython import *
from time import sleep
import threading
print("\n----------------------------------\n")

def time_keeper(timer_source):
    print("bruh")
    obs_frontend_recording_start()
    sleep(65)
    obs_frontend_recording_stop()
    obs_source_media_stop(timer_source)
    print("bruh moment 2.0")
    return

def start_match(ignore1, ingore2):
    global timer_source_name, time_thread
    timer_source = obs_get_source_by_name(timer_source_name)
    time_thread = threading.Thread(target = time_keeper, args=(timer_source,))
    time_thread.start()
    obs_source_media_restart(timer_source)
    print(obs_source_media_get_state(timer_source))
    obs_source_release(timer_source)
    timer_source = None

def end_match(ignore1, ignore2):
    global timer_source_name, time_thread
    obs_frontend_recording_stop()
    time_thread.stop()
    timer_source = obs_get_source_by_name(timer_source_name)
    obs_source_media_set_time(timer_source, 63000)
    obs_source_media_stop(timer_source)
    print(obs_source_media_get_state(timer_source))
    obs_source_release(timer_source)
    timer_source = None

def script_properties():
    global props
    props = obs_properties_create()
    video_list_prop = obs_properties_add_list(props, "TimerSource", "Select Timer Video Source", 
        OBS_COMBO_TYPE_LIST, 
        OBS_COMBO_FORMAT_STRING)
    source_enum = obs_enum_sources()
    for source in source_enum:
        obs_property_list_add_string(video_list_prop, obs_source_get_name(source), obs_source_get_name(source))
    source_list_release(source_enum)
    source_enum = None
    obs_properties_add_button(props, "StartBtn", "Start Match", start_match)
    obs_properties_add_button(props, "EndBtn", "End Match", end_match)

    return props

def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global timer_source_name
    timer_source_name = obs_data_get_string(settings, "TimerSource")
    print(timer_source_name)
    # timer_source_info = obs_source_info.create(settings, obs_get_source_by_name(timer_source_name))