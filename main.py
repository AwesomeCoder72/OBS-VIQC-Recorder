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

def rename_and_compress():
    global compress_output#, recording_path
    print(obs_frontend_get_recording_output())


def time_keeper(timer_source):
    global stop_timer
    print("bruh")
    obs_frontend_recording_start()
    for i in range(135):
        if stop_timer:
            return
        else:
            sleep(0.5)
    obs_frontend_recording_stop()
    obs_source_media_stop(timer_source)
    print("bruh moment 2.0")
    return

def start_match(ignore1, ingore2):
    global timer_source_name, time_thread, stop_timer
    stop_timer = False
    timer_source = obs_get_source_by_name(timer_source_name)
    time_thread = threading.Thread(target = time_keeper, args=(timer_source,))
    time_thread.start()
    obs_source_media_restart(timer_source)
    print(obs_source_media_get_state(timer_source))
    obs_source_release(timer_source)
    timer_source = None

def end_match(ignore1, ignore2):
    global timer_source_name, time_thread, compress_output, stop_timer
    obs_frontend_recording_stop()
    stop_timer = True
    timer_source = obs_get_source_by_name(timer_source_name)
    obs_source_media_set_time(timer_source, 63000)
    obs_source_media_stop(timer_source)
    print(obs_source_media_get_state(timer_source))
    obs_source_release(timer_source)
    timer_source = None
    if compress_output:
        rename_and_compress()

def script_description():
    return """<div style='text-align: center;'><span><img height=30 src='file:"""+ str(script_path())+"iqlogo.png'>"+"""</span><h2>Match Timer and Recorder</h2></div>"""
	# return "<span valign=middle sy><img height=18 src='file:"+ str(script_path())+"iqlogo.png"+"'/></span>"

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
    obs_properties_add_bool(props, "CompressBtn", "Compress Recordings on Completion?")

    return props

def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global timer_source_name, compress_output
    timer_source_name = obs_data_get_string(settings, "TimerSource")
    
    compress_output = obs_data_get_bool(settings, "CompressBtn")
