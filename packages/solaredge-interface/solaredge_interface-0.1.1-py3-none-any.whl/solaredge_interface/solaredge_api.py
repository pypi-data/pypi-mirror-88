
import functools
from .util.misc import url_join, http_request


BASEURL = "https://monitoringapi.solaredge.com"


class SolarEdgeAPI:
    """
    This class implements Python3 interfaces to the documented SolarEdge API end-points.  Refer to
    [se_monitoring_api.pdf](https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf) for more details
    on the SolarEdge API.
    """

    api_key = None

    def __init__(self, api_key):
        """
        To call the SolarEdge API you need a valid `api_key` which can be obtained from your SolarEdge account.

        _parameters_
        * _api_key_ (str) required - a valid api_key from https://monitoring.solaredge.com
        """
        self.api_key = api_key

    @functools.lru_cache(maxsize=128, typed=False)
    def get_accounts(self, size=100, start_index=0, search_text="", sort_property="", sort_order="ASC"):
        """
        Returns the sub-accounts accessible by the `api_key` with an ability to search and filter.

        _parameters_
        * _size_ (int) default: `100` - The maximum number of accounts returned by this call.  The maximum number of
        accounts that can be returned by this call is 100. If you have more than 100 accounts, just request another
        100 accounts with startIndex=100 which will fetch accounts 100-199.
        * _start_index_ (int) default: `0` - The first account index to be returned in the results.
        * _search_text_ (str) default: - The search text for accounts.  Searchable accounts properties: Name, Notes,
        Email, Country, State, City, Zip, Full address
        * _sort_property_ (str) default: - A sorting option for this account list, based on one of its properties.
        Available sort properties: Name, country, city, Address, zip, fax, phone, notes
        * _sort_order_ (str) default: `ASC` - Sort order for the sort property. Allowed values are ASC (ascending) and
        DESC (descending)

        Uses Least-Recently-Used caching strategy to reduce calls to API backend and speed re-occurring function calls.
        """

        url = url_join(BASEURL, "accounts", "list")
        params = {
            'api_key': self.api_key,
            'size': size,
            'startIndex': start_index,
            'sortOrder': sort_order,
        }
        if search_text:
            params['searchText'] = search_text
        if sort_property:
            params['sortProperty'] = sort_property

        return http_request(url, params)

    @functools.lru_cache(maxsize=128, typed=False)
    def get_sites(self, size=100, start_index=0, search_text="", sort_property="", sort_order="ASC", status="Active,Pending"):
        """
        Returns the sites accessible by the `api_key` with an ability to search and filter.

        _parameters_
        * _size_ (int) default: `100` - The maximum number of sites returned by this call.  The maximum number of sites
        that can be returned by this call is 100. If you have more than 100 sites, just request another 100 sites with
        startIndex=100 which will fetch sites 100-199.
        * _start_index_ (int) default: `0` - The first site index to be returned in the results.
        * _search_text_ (str) default: - The search text for sites.  Searchable site properties: Name, Notes,
        Address, City, Zip code, Full address, Country
        * _sort_property_ (str) default: - A sorting option for this site list, based on one of its properties.
        Available sort properties: Name, Country, State, City, Address, Zip, Status, PeakPower, InstallationDate,
         Amount, MaxSeverity, CreationTime
        * _sort_order_ (str) default: `ASC` - Sort order for the sort property. Allowed values are ASC (ascending) and
        DESC (descending)
        * _status_ (str) default: `Active,Pending` - Select the sites to be included in the list by their status:
        Active, Pending, Disabled, All.

        Uses Least-Recently-Used caching strategy to reduce calls to API backend and speed re-occurring function calls.
        """

        url = url_join(BASEURL, "sites", "list")
        params = {
            'api_key': self.api_key,
            'size': size,
            'startIndex': start_index,
            'sortOrder': sort_order,
            'status': status
        }
        if search_text:
            params['searchText'] = search_text
        if sort_property:
            params['sortProperty'] = sort_property

        return http_request(url, params)

    @functools.lru_cache(maxsize=128, typed=False)
    def get_site_details(self, site_id):
        """
        Returns site details for `site_id` such as name, location, status, etc.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.

        Uses Least-Recently-Used caching strategy to reduce calls to API backend and speed re-occurring function calls.
        """

        url = url_join(BASEURL, "site", site_id, "details")
        params = {
            'api_key': self.api_key
        }

        return http_request(url, params)

    @functools.lru_cache(maxsize=128, typed=False)
    def get_site_data_period(self, site_id):
        """
        Returns the start-date and end-date of energy production at the site(s).

        _parameters_
        * _site_id_ (int or list) required - The site identifier(s) to retrieve data for, may be provided as a single
        int value or a list of int values to retrieve data in "bulk-mode"

        Uses Least-Recently-Used caching strategy to reduce calls to API backend and speed re-occurring function calls.
        """

        if type(site_id) is list:
            url = url_join(BASEURL, "sites", ",".join(site_id), "dataPeriod")
        else:
            url = url_join(BASEURL, "site", site_id, "dataPeriod")
        params = {
            'api_key': self.api_key
        }

        return http_request(url, params)

    def get_site_energy(self, site_id, start_date, end_date, time_unit="DAY"):
        """
        Returns the site(s) energy measurements.

        NB: the time input parameters required are date values in the format YYYY-MM-DD not full timestamp values.

        _parameters_
        * _site_id_ (int or list) required - The site identifier(s) to retrieve data for, may be provided as a single
        int value or a list of int values to retrieve data in "bulk-mode"
        * _start_date_ (str) required - must be in format YYYY-MM-DD
        * _end_date_ (str) required - must be in format YYYY-MM-DD
        * _time_unit_ (str) default: `DAY` - Permitted values are: QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR
        """

        if type(site_id) is list:
            url = url_join(BASEURL, "sites", ",".join(site_id), "energy")
        else:
            url = url_join(BASEURL, "site", site_id, "energy")
        params = {
            'api_key': self.api_key,
            'startDate': start_date,
            'endDate': end_date,
            'timeUnit': time_unit
        }

        return http_request(url, params)

    def get_site_time_frame_energy(self, site_id, start_date, end_date, time_unit="DAY"):
        """
        Return the site(s) total energy produced for a given date period.

        NB: the time input parameters required are date values in the format YYYY-MM-DD not full timestamp values.

        _parameters_
        * _site_id_ (int or list) required - The site identifier(s) to retrieve data for, may be provided as a single
        int value or a list of int values to retrieve data in "bulk-mode"
        * _start_date_ (str) required - must be in format YYYY-MM-DD
        * _end_date_ (str) required - must be in format YYYY-MM-DD
        * _time_unit_ (str) default: `DAY` - Permitted values are: QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR
        """

        if type(site_id) is list:
            url = url_join(BASEURL, "sites", ",".join(site_id), "timeFrameEnergy")
        else:
            url = url_join(BASEURL, "site", site_id, "timeFrameEnergy")
        params = {
            'api_key': self.api_key,
            'startDate': start_date,
            'endDate': end_date,
            'timeUnit': time_unit
        }

        return http_request(url, params)

    def get_site_overview(self, site_id):
        """
        Return the site(s) overview data.

        _parameters_
        * _site_id_ (int or list) required - The site identifier(s) to retrieve data for, may be provided as a single
        int value or a list of int values to retrieve data in "bulk-mode"
        """

        if type(site_id) is list:
            url = url_join(BASEURL, "sites", ",".join(site_id), "overview")
        else:
            url = url_join(BASEURL, "site", site_id, "overview")
        params = {
            'api_key': self.api_key
        }

        return http_request(url, params)

    def get_site_power(self, site_id, start_time, end_time):
        """
        Return the site(s) power measurements in 15 minute resolution.

        _parameters_
        * _site_id_ (int or list) required - The site identifier(s) to retrieve data for, may be provided as a single
        int value or a list of int values to retrieve data in "bulk-mode"
        * _start_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _end_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        """

        if type(site_id) is list:
            url = url_join(BASEURL, "sites", ",".join(site_id), "power")
        else:
            url = url_join(BASEURL, "site", site_id, "power")
        params = {
            'api_key': self.api_key,
            'startTime': start_time,
            'endTime': end_time
        }

        return http_request(url, params)

    def get_site_power_details(self, site_id, start_time, end_time, meters=None):
        """
        Detailed site power measurements from meters such as consumption, export (feed-in), import (purchase), etc.
        Calculated meter readings (also referred to as "virtual meters"), such as self-consumption, are calculated
        using the data measured by the meter and the inverters.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _start_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _end_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _meters_ (str) default: - If this value is omitted all meter readings are returned. The following values are
        permitted separated by comma: Production, Consumption, SelfConsumption, FeedIn, Purchased
        """

        url = url_join(BASEURL, "site", site_id, "powerDetails")
        params = {
            'api_key': self.api_key,
            'startTime': start_time,
            'endTime': end_time
        }
        if meters:
            params['meters'] = meters

        return http_request(url, params)

    def get_site_energy_details(self, site_id, start_time, end_time, meters=None, time_unit="DAY"):
        """
        Detailed site energy measurements from meters such as consumption, export (feed-in), import (purchase), etc.
        Calculated meter readings (also referred to as "virtual meters"), such as self-consumption, are calculated
        using the data measured by the meter and the inverters.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _start_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _end_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _meters_ (str) default: None - If this value is omitted all meter readings are returned. The following values
        are permitted separated by comma: Production, Consumption, SelfConsumption, FeedIn, Purchased
        * _time_unit_ (str) default: `DAY` - Permitted values are: QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR
        """

        url = url_join(BASEURL, "site", site_id, "energyDetails")
        params = {
            'api_key': self.api_key,
            'startTime': start_time,
            'endTime': end_time,
            'timeUnit': time_unit
        }
        if meters:
            params['meters'] = meters

        return http_request(url, params)

    def get_site_current_power_flow(self, site_id):
        """
        Provides the current power flow between all elements of the site including PV array, storage (battery), loads
        (consumption) and grid.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        """

        url = url_join(BASEURL, "site", site_id, "currentPowerFlow")
        params = {
            'api_key': self.api_key
        }

        return http_request(url, params)

    def get_site_storage_data(self, site_id, start_time, end_time, serials=None):
        """
        Get detailed storage information from batteries:the state of energy, power and lifetime energy.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _start_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _end_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _serials_ (list) default: None - Return data only for specific battery serial numbers; If omitted, the
        response includes all the batteries at the site.
        """

        url = url_join(BASEURL, "site", site_id, "storageData")
        params = {
            'api_key': self.api_key,
            'startTime': start_time,
            'endTime': end_time
        }
        if serials:
            params['serials'] = serials

        return http_request(url, params)

    # def get_site_image(self, site_id, name=None, max_width=None, max_height=None, hash=None):
    #     pass

    # def get_site_installer_logo(self, site_id, name=None):
    #     pass

    def get_site_environmental_benefits(self, site_id, system_units=None):
        """
        Get all environmental benefits based on site energy production:CO2 emissions saved, equivalent trees planted,
        and light bulbs powered for a day.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _system_units_ (str) default: None - The system units used when returning gas emission savings.  Valid
        values: `Metrics`, `Imperial` note these values are case sensitive. If system_units is not specified, the user
        system units are used.
        """

        url = url_join(BASEURL, "site", site_id, "envBenefits")
        params = {
            'api_key': self.api_key,
        }
        if system_units:
            params['systemUnits'] = system_units

        return http_request(url, params)

    # def get_site_equipment_list(self, site_id):
    #     pass

    @functools.lru_cache(maxsize=128, typed=False)
    def get_site_inventory(self, site_id):
        """
        Get the inventory of SolarEdge equipment at the site, including inverters/SMIs, batteries, meters,  gateways
        and sensors.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.

        Uses Least-Recently-Used caching strategy to reduce calls to API backend and speed re-occurring function calls.
        """

        url = url_join(BASEURL, "site", site_id, "inventory")
        params = {
            'api_key': self.api_key
        }

        return http_request(url, params)

    def get_site_equipment_data(self, site_id, start_time, end_time, serial_number):
        """
        Get specific inverter data for a given timeframe.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _start_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _end_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _serial_number_ (str) required - The inverter short serial number, eg 12345678-90
        """

        url = url_join(BASEURL, "equipment", site_id, serial_number, "data")
        params = {
            'api_key': self.api_key,
            'startTime': start_time,
            'endTime': end_time
        }

        return http_request(url, params)

    def get_site_equipment_change_log(self, site_id, serial_number):
        """
        Returns a list of equipment component replacements ordered by date. This method is applicable to inverters,
        optimizers, batteries and gateways.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _serial_number_ (str) required - Inverter, battery, optimizer or gateway short serial number.
        """

        url = url_join(BASEURL, "equipment", site_id, serial_number, "changeLog")
        params = {
            'api_key': self.api_key,
        }

        return http_request(url, params)

    def get_site_meters(self, site_id, start_time, end_time, meters=None):
        """
        Returns for each meter on site its lifetime energy reading, metadata and the device to which it is connected.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        * _start_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _end_time_ (str) required - must be in format YYYY-MM-DD hh:mm:ss
        * _meters_ (str ot list) default: None - Select specific meters only. If this value is omitted, all meter
        readings are returned.  Valid values: Production, Consumption,
         FeedIn, Purchased.
        """

        url = url_join(BASEURL, "site", site_id, "meters")
        params = {
            'api_key': self.api_key,
            'startTime': start_time,
            'endTime': end_time
        }
        if meters:
            params['meters'] = meters

        return http_request(url, params)

    def get_site_equipment_sensors(self, site_id):
        """
        Returns a list of all the sensors in the site, and the device to which they are connected.

        _parameters_
        * _site_id_ (int) required - The site identifier to retrieve data for.
        """

        url = url_join(BASEURL, "equipment", site_id, "sensors")
        params = {
            'api_key': self.api_key,
        }

        return http_request(url, params)

    def get_version(self):
        """
        Returns a list of all the sensors in the site, and the device to which they are connected.
        """

        url = url_join(BASEURL, "version", "current")

        return http_request(url)
