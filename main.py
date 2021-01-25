"""
Helpful links:
 - for starting the timer video:
 - - https://obsproject.com/docs/reference-sources.html?highlight=media#c.obs_source_info.media_play_pause
 - - 
"""
import obspython as obs
print("\n----------------------------------\n")

def start_match(ignore1, ingore2):
    global timer_source_name, timer_source_info
    # print(timer_source_name)
    timer_source = obs.obs_get_source_by_name(timer_source_name)
    print(timer_source)
    timer_source_data = obs.calldata_source(timer_source, "scene")
    print(timer_source_data)
    timer_source.media_play_pause()

    obs.obs_source_release(timer_source)
    timer_source = None


def script_properties():
    global props
    props = obs.obs_properties_create()
    video_list_prop = obs.obs_properties_add_list(props, "TimerSource", "Select Timer Video Source", 
        obs.OBS_COMBO_TYPE_LIST, 
        obs.OBS_COMBO_FORMAT_STRING)
    source_enum = obs.obs_enum_sources()
    for source in source_enum:
        obs.obs_property_list_add_string(video_list_prop, obs.obs_source_get_name(source), obs.obs_source_get_name(source))
    source_list_release(source_enum)
    source_enum = None
    obs.obs_properties_add_button(props, "StartBtn", "Start Match", start_match)

    return props

def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global timer_source_name, timer_source_info
    timer_source_name = obs.obs_data_get_string(settings, "TimerSource")
    print(timer_source_name)
    # timer_source_info = obs_source_info.create(settings, obs_get_source_by_name(timer_source_name))