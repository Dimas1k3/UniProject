import webview
import os

from db import (
    init_db,
   
    get_items_from_db, add_item_to_db,
    delete_item_from_db, update_item_status,

    reset_status
)

from handlers import (
    block_sites, kill_browsers, filter_items, block_apps
)

class API:
    def getItems(self, type):
        return get_items_from_db(type)

    def addItem(self, type, value):
        return add_item_to_db(type, value)

    def deleteItem(self, type, id, label):
        delete_item_from_db(type, id)

        return f"{type.capitalize()} удалён: {label}"

    def updateStatus(self, type, id, status):
        update_item_status(type, id, status)
        
        return f"Статус {type} обновлён: {status}"
    
    def blockSites(self, sites):
        blocked_sites = filter_items(sites, 'url')
        block_sites(blocked_sites)

        return f"Сайты заблокированы"
    
    def killBrowser(self):
        kill_browsers()

        return f"Браузеры закрыты"
    
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
        "Антипрокрастинатор",
        url,
        js_api=api,
        width=1200,
        height=800,
        resizable=False
    )

    webview.start(debug=True, http_server=False) 