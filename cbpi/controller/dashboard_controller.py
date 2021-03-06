import logging
import json
from cbpi.controller.crud_controller import CRUDController
from cbpi.database.model import DashboardModel, DashboardContentModel
import os

class DashboardController(CRUDController):

    model = DashboardModel
    name = "Dashboard"

    def __init__(self, cbpi):
        self.caching = False
        super(DashboardController, self).__init__(cbpi)
        self.cbpi = cbpi
        self.logger = logging.getLogger(__name__)
        self.cbpi.register(self)

    def get_state(self):
        return dict(items=self.cache)

    async def get_content(self, dashboard_id):
        try:
            with open('./config/dashboard/cbpi_dashboard_%s.json' % dashboard_id) as json_file:
                data = json.load(json_file)
                return data
        except:
            return {}
        

    async def add_content(self, dashboard_id, data):
        with open('./config/dashboard/cbpi_dashboard_%s.json' % dashboard_id, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        
        return {"status": "OK"}

    async def delete_content(self, dashboard_id):
        if os.path.exists('./config/dashboard/cbpi_dashboard_%s.json' % dashboard_id):
            os.remove('./config/dashboard/cbpi_dashboard_%s.json' % dashboard_id)


    async def delete_dashboard(self, dashboard_id):
        await DashboardContentModel.delete_by_dashboard_id(dashboard_id)
        await self.model.delete(dashboard_id)