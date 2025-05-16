import { renderItems } from "./tasksSitesAppsScript.js";

function killHandlers() {
    const blockedSitesMsg = document.getElementById("blockedSitesMsg");
    const confirmKillBtn = document.getElementById("confirmKill");
    const cancelKillBtn = document.getElementById("cancelKill");

    blockedSitesMsg.style.display = "block";

    confirmKillBtn.removeEventListener("click", confirmKillHandler);
    cancelKillBtn.removeEventListener("click", cancelKillHandler);

    confirmKillBtn.addEventListener("click", confirmKillHandler);
    cancelKillBtn.addEventListener("click", cancelKillHandler);
}

function confirmKillHandler() {
    window.pywebview.api.killBrowser()
        .then(() => {
            document.getElementById("blockedSitesMsg").style.display = "none";
        })
        .catch(err => {
            console.error("❌ Ошибка при закрытии браузеров");
        });
}

function cancelKillHandler() {
    document.getElementById("blockedSitesMsg").style.display = "none";
}

function resetItems(items, table) {
    const changed = [];
        
    items.forEach(item => {
        if (item.is_active === true) {
            changed.push(item);
        }
        
        item.is_active = false;
    });

    if (changed.length === 0) {
        // show err
        return;
    }

    window.pywebview.api.resetStatus(changed, table)
        .then(() => {
            renderItems("site", items, "site-container");
        })
        .catch(err => {
            console.error("Ошибка при сбросе сайтов:", err);
    });
}

function blockItems(sites, siteErrMsg) {
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
}

function switchSiteAppContainer(isAppsMode, switchButton, siteContainer, 
    appContainer, controlSiteContainer, controlAppContainer) {
    isAppsMode = !isAppsMode;

    switchButton.classList.toggle("active");
    switchButton.textContent = isAppsMode ? "Сайты ⇄ Приложения (Apps)" : "Приложения ⇄ Сайты (Sites)";
    
    siteContainer.style.display = isAppsMode ? "none" : "block";
    appContainer.style.display = isAppsMode ? "block" : "none";

    controlSiteContainer.style.display = isAppsMode ? "none" : "flex";
    controlAppContainer.style.display = isAppsMode ? "flex" : "none";

    return isAppsMode;
}

export { killHandlers, resetItems, blockItems, switchSiteAppContainer};