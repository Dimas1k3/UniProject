import webview
import os

from db import (
    init_db,

    get_items_from_db, add_item_to_db,
    delete_item_from_db, update_item_status,

    reset_status
)

from handlers import (
    block_sites, kill_browsers, filter_items, 
    block_apps, reset_sites
)

class API:
    def getItems(self, item_type):
        return get_items_from_db(item_type)

    def addItem(self, item_type, value):
        return add_item_to_db(item_type, value)

    def deleteItem(self, item_type, item_id, label):
        delete_item_from_db(item_type, item_id)
        
        return f"{item_type.capitalize()} deleted: {label}"

    def updateStatus(self, item_type, item_id, status):
        update_item_status(item_type, item_id, status)
        
        return f"{item_type.capitalize()} status updated: {status}"
    
    def blockSites(self, sites):
        blocked_sites = filter_items(sites, 'url')
        block_sites(blocked_sites)
        
        return "Websites blocked"
    
    def killBrowser(self):
        kill_browsers()
        
        return "Browsers closed"
    
    def blockApps(self, apps):
        blocked_apps = filter_items(apps, 'name')
        block_apps(blocked_apps)
    
    def resetStatus(self, items, table):
        reset_status(items, table)

        return f"{table[:-1]}"

if __name__ == '__main__':
    init_db()
    api = API()

    html_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web', 'index.html'))
    url = 'file:///' + html_file.replace('\\', '/')

    window = webview.create_window(
        "Antiprocrastinator",
        url,
        js_api=api,
        width=1200,
        height=700,
        resizable=False
    )

    webview.start(debug=True, http_server=False)
