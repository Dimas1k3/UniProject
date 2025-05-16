import { 
    renderItems, addItem, removeItem 
} from './tasksSitesAppsScript.js';

import { 
    saveTasksToLocal, loadTasksFromLocal , 
    saveSitesToLocal, loadSitesFromLocal,
    saveAppsToLocal, loadAppsFromLocal
} from './storage.js';

import { 
    killHandlers, blockItems,
    resetItems,
    switchSiteAppContainer
} from './handlers.js';

let tasks = [];
let sites = [];
let apps = [];
let isAppsMode = false;

const taskInput = document.getElementById("newTaskInput");
const siteInput = document.getElementById("newSiteInput");
const appInput = document.getElementById("newAppInput");
const addTaskBtn = document.getElementById("addTaskBtn");
const addSiteBtn = document.getElementById("addSiteBtn");
const addAppBtn = document.getElementById("addAppBtn");
const resetBlockedSitesBtn = document.getElementById("resetBlockedSitesBtn");
const blockSitesBtn = document.getElementById("blockSitesBtn");
const resetBlockedAppsBtn = document.getElementById("resetBlockedAppsBtn");
const blockAppsBtn = document.getElementById("blockAppsBtn");
const siteErrMsg = document.getElementById("siteErrMsg");
const appErrMsg = document.getElementById("appErrMsg");

const switchButton = document.getElementById("switch-button");
const siteContainer = document.getElementById("site-container");
const appContainer = document.getElementById("app-container");
const controlSiteContainer = document.getElementById("control-site-container");
const controlAppContainer = document.getElementById("control-app-container");

function initApp() {
    window.pywebview.api.getItems("task").then(fetchedTasks => {
        tasks = fetchedTasks;

        saveTasksToLocal(tasks);
        console.info(tasks);
        renderItems("task", tasks, "task-container");
    });

    window.pywebview.api.getItems("site").then(fetchedSites => {
        sites = fetchedSites;

        saveSitesToLocal(sites);
        console.info(sites);
        renderItems("site", sites, "site-container");
    });

    window.pywebview.api.getItems("app").then(fetchedApps => {
        apps = fetchedApps;

        saveAppsToLocal(apps);
        console.info(apps);
        renderItems("app", apps, "app-container");
    });

    addTaskBtn.addEventListener("click", () => {
        if (taskInput.value.trim() !== "") {
            addItem("task", tasks, "task-container");
        }
    });

    addSiteBtn.addEventListener("click", () => {
        if (siteInput.value.trim() !== "") {
            addItem("site", sites, "site-container");
        }
    });

    addAppBtn.addEventListener("click", () => {
        if (appInput.value.trim() !== "") {
            addItem("app", apps, "app-container");
        }
    });

    resetBlockedSitesBtn.addEventListener("click", () => {
        resetItems(sites, "sites");
    });

    blockSitesBtn.addEventListener("click", () => {
        blockItems(sites, siteErrMsg);
    });

    resetBlockedAppsBtn.addEventListener("click", () => {
        resetItems(apps, "apps");
    });
 
    blockAppsBtn.addEventListener("click", () => {
        blockItems(apps, appErrMsg);
    });

    switchButton.addEventListener("click", () => {
        let newIsAppsMode = switchSiteAppContainer(
            isAppsMode, switchButton, 
            siteContainer, appContainer, 
            controlSiteContainer, controlAppContainer
        );

        isAppsMode = newIsAppsMode;
    });


}

window.addEventListener('pywebviewready', initApp);