import { 
    renderTasks, addTask, 
    removeTask 
} from './tasksScript.js';

import { 
    renderSites, addSite, 
    removeSite
} from './sitesAppsScript.js';

import { 
    saveTasksToLocal, loadTasksFromLocal , 
    saveSitesToLocal, loadSitesFromLocal
} from './storage.js';

import { 
    killHandlers 
} from './handlers.js';

let tasks = [];
let sites = [];

function initApp() {
    window.pywebview.api.getTasks().then(fetchedTasks => {
        tasks = fetchedTasks;

        saveTasksToLocal(tasks);
        console.info(tasks);
        renderTasks(tasks);
    })

    window.pywebview.api.getSites().then(fetchedSites => {
        sites = fetchedSites;

        saveSitesToLocal(sites);
        console.info(sites);
        renderSites(sites);
    })

    const taskInput = document.getElementById("newTaskInput");
    const siteInput = document.getElementById("newSiteInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const addSiteBtn = document.getElementById("addSiteBtn");
    const resetBlockedSitesBtn = document.getElementById("resetBlockedSitesBtn")
    const blockSitesBtn = document.getElementById("blockSitesBtn");
    const siteErrMsg = document.getElementById("siteErrMsg");

    addTaskBtn.addEventListener("click", () => {
        if (taskInput.value.trim() !== "") {
            addTask(tasks);
        }
    });

    addSiteBtn.addEventListener("click", () => {
        if (siteInput.value.trim() !== "") {
            addSite(sites);
        }
    });

    resetBlockedSitesBtn.addEventListener("click", () => {
        const changed = [];
        
        sites.forEach(site => {
            if (site.is_active === true) {
                changed.push(site);
            }
            
            site.is_active = false;
        });

        window.pywebview.api.resetSiteStatus(changed)
            .then(() => {
                
            })
            .catch(err => {
                console.error("Ошибка при сбросе сайтов:", err);
        });
    })

    blockSitesBtn.addEventListener("click", () => {
        const activeSites = sites.filter(site => site.is_active);
        
        if (activeSites.length === 0) {
            siteErrMsg.style.display = "block";
            setTimeout(() => {
                siteErrMsg.style.display = "none";
            }, 2000);
        
            return;
        }
        
        window.pywebview.api.blockSites(sites)
            .then(() => {
                killHandlers(); 
            })
            .catch(err => {
                console.error("Ошибка при блокировке сайтов:", err);
            });
    }); 
}

window.addEventListener('pywebviewready', initApp);