from dsmpy.event import Event
from dsmpy.station import Station
from dsmpy.window import Window
from dsmpy.component import Component
import pickle
from obspy.taup import TauPyModel
import numpy as np

class WindowMaker:
    """Utility class to compute list of Window.

    """

    @staticmethod
    def windows_from_obspy_traces(
            trace, model_name, phase_names,
            t_before=10., t_after=40.):
        event = Event(
            trace.stats.sac.kevnm,
            trace.stats.sac.evla,
            trace.stats.sac.evlo,
            trace.stats.sac.evdp,
            None, None, None)
        station = Station(
            trace.stats.station,
            trace.stats.network,
            trace.stats.sac.stla,
            trace.stats.sac.stlo)
        component = Component.parse_component(trace.stats.sac.kcmpnm)

        windows = WindowMaker.compute(
            event, [station], model_name, phase_names,
            [component], t_before, t_after)
        return windows

    @staticmethod
    def windows_from_dataset(
            dataset, model_name, phase_names,
            components, t_before=10., t_after=40.):
        '''Compute list of Window from a Dataset.

        Args:
            dataset (Dataset): dataset
            model_name (str): name of the 1-D reference model
            phase_names (list of str): name of seismic phases
            components (list of Component): seismic components
            t_before (float): time before arrival (default: 10)
            t_after (float): time after arrival (default: 40)

        Returns:
            windows (list of Window): time windows

        '''
        windows = []
        for i, event in enumerate(dataset.events):
            start, end = dataset.get_bounds_from_event_index(i)
            stations = dataset.stations[start:end]
            tmp_windows = WindowMaker.compute(
                event, stations, model_name, phase_names,
                components, t_before, t_after)
            windows += tmp_windows
        return windows

    @staticmethod
    def compute(
            event, stations, model_name, phase_names,
            components, t_before=10., t_after=40.):
        '''Compute time windows using TauP.

        Args:
            event (Event): seismic event
            stations (list of Station): seismic stations
            model_name (str): name of reference 1-D model
            phase_names (list of str): list of TauP phase names
            components (list of Component): seismic components
            t_before (float): time before arrival (default is 10)
            t_after (float): time after arrival (default is 40)

        Returns:
            windows (list of Window): time windows

        '''
        taup_model = TauPyModel(model_name)
        windows = []
        for station in stations:
            distance = event.get_epicentral_distance(station)
            arrivals = taup_model.get_travel_times(
                event.depth, distance, phase_list=phase_names)
            # at the moment consider only first arrival
            processed_phases = set()
            if len(arrivals) > 0:
                for arrival in arrivals:
                    if arrival.name not in processed_phases:
                        for component in components:
                            windows.append(
                                Window(
                                    arrival.time, event, station, arrival.name,
                                    component, t_before, t_after))
                    processed_phases.add(arrival.name)
            # else:
            #     for component in components:
            #         windows.append(Window(
            #             np.NaN, event, station, None,
            #             component, np.NaN, np.NaN))
        return windows

    @staticmethod
    def set_limit(windows, t_before, t_after):
        '''Set t_before and t_after for all window in windows.
        
        Args:
            windows (list of Windows): time windows
            t_before (float): time before arrival (in seconds)
            t_after (float): time after arrival (in seconds)
        '''
        for i in range(len(windows)):
            windows[i].t_before = t_before
            windows[i].t_after = t_after

    @staticmethod
    def save(path, windows):
        '''Save windows using pickle.dump().

        Args:
            path (str): name of the output file.
            windows (list of Window): time windows.

        '''
        with open(path, 'wb') as f:
            pickle.dump(windows, f)

    @staticmethod
    def load(path):
        '''Read path into list of Window using pickle.load().

        Args:
            path (str): path to the file that contains time windows

        Returns:
            windows (list of Window)): time windows

        '''
        with open(path, 'rb') as f:
            output = pickle.load(f)
        return output
        
if __name__ == '__main__':
    from dsmpy.utils.cmtcatalog import read_catalog
    catalog = read_catalog()
    event = Event.event_from_catalog(
    catalog, '200707211534A')
    stations = [
    Station(
        name='FCC', network='CN',
        latitude=58.7592, longitude=-94.0884), ]
    model = 'prem'
    phases = ['S', 'ScS']
    components = [Component.T]
    windows = WindowMaker.compute(event, stations, model, phases, components)
    print(windows)