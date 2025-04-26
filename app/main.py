import webview
import os

from db import (
    init_db,
   
    get_tasks_from_db, add_task_to_db,
    delete_task_from_db, update_task_status,

    get_sites_from_db, add_site_to_db,
    delete_site_from_db, update_site_status
)

from handlers import (
    block_sites, killBrowsers
)

class API:
    def getTasks(self):
        tasks = get_tasks_from_db()
        
        return tasks
    
    def addNewTask(self, task):
        print(task)
        
        new_task = add_task_to_db(task)
        print(new_task)
        
        return new_task
    
    def deleteTask(self, id, title):
        print(id)
        delete_task_from_db(id)

        return f"Удалена задача: {title}"
    
    def updateTaskStatus(self, task_id, task_status):
        print(task_id)
        print(task_status)

        update_task_status(task_id, task_status)
        
        return f"Обновлен статус задачи: {task_status}"
    
    # ------------------------------------------------------

    def getSites(self):
        sites = get_sites_from_db()
        
        return sites

    def addNewSite(self, url):
        print(url)
        
        new_site = add_site_to_db(url)
        print(new_site)
        
        return new_site

    def deleteSite(self, id, url):
        print(id)
        delete_site_from_db(id)
        
        return f"Удалён сайт: {url}"

    def updateSiteStatus(self, site_id, is_active):
        print(site_id)
        print(is_active)

        update_site_status(site_id, is_active)
        
        return f"Обновлен статус сайта: {is_active}"
    
    def blockSites(self, sites):
        blocked_sites = []
        print(sites)

        for site in sites:
            if site['is_active'] == True:
                blocked_sites.append(site['url'])

        block_sites(blocked_sites)

        return f"Сайты заблокированы"
    
    def killBrowser(self):
        killBrowsers()

        return f"Браузеры закрыты"

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