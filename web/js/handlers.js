import { renderItems } from "./tasksSitesAppsScript.js";

function killBrowsers() {
    const blockedSitesMsg = document.getElementById("blockedSitesMsg");
    const confirmKillBtn = document.getElementById("confirmKill");
    const cancelKillBtn = document.getElementById("cancelKill");

    blockedSitesMsg.style.display = "block";

    confirmKillBtn.removeEventListener("click", confirmKillHandler);
    cancelKillBtn.removeEventListener("click", cancelKillHandler);

    confirmKillBtn.addEventListener("click", confirmKillHandler);
    cancelKillBtn.addEventListener("click", cancelKillHandler);
}

function confirmKillBrowsers() {
    window.pywebview.api.killBrowser()
        .then(() => {
            document.getElementById("blockedSitesMsg").style.display = "none";
        })
        .catch(err => {
            console.error("❌ Error while closing browsers");
        });
}

function cancelKillBrowsers() {
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
        // show error
        return;
    }

    window.pywebview.api.resetStatus(changed, table)
        .then((item) => {
            renderItems(`${item}`, items, `${item}-container`);
        })
        .catch(err => {
            console.error("Error while resetting:", err);
    });
}

function blockItems(items, ErrMsg, type) {
    const activeItems = items.filter(item => item.is_active);
            
    if (activeItems.length === 0) {
        ErrMsg.style.display = "block";
        setTimeout(() => {
            ErrMsg.style.display = "none";
        }, 2000);
            
        return;
    }

    if (type === 'sites') {     
        window.pywebview.api.blockSites(items)
            .then((response) => {
                console.info(response);
                console.log(typeof response);
                if (response === 'Websites blocked') {
                    const confirmKill = document.getElementById("confirmKill")
                    const cancelKill = document.getElementById("cancelKill")
                    document.getElementById("blockedSitesMsg").style.display = "block";
                    
                    confirmKill.addEventListener("click", () => {
                        confirmKillBrowsers(); 
                    });

                    cancelKill.addEventListener("click", () => {
                        document.getElementById("blockedSitesMsg").style.display = "none";
                        return;
                    });
                }
            })
            .catch(err => {
                console.error("Error while blocking", err);
        });
        return;
    }

    if (type === 'apps') {
        window.pywebview.api.blockApps(items)
            .then((response) => { 
            })
            .catch(err => {
                console.error("Error while blocking", err);
        });
        return;
    }
}

function switchSiteAppContainer(isAppsMode, switchButton, siteContainer, 
    appContainer, controlSiteContainer, controlAppContainer) {
    isAppsMode = !isAppsMode;

    switchButton.classList.toggle("active");
    switchButton.textContent = isAppsMode ? "Applications (Apps) ⇄ Sites" : "Sites ⇄ Applications (Apps)";

    siteContainer.style.display = isAppsMode ? "none" : "block";
    appContainer.style.display = isAppsMode ? "block" : "none";

    controlSiteContainer.style.display = isAppsMode ? "none" : "flex";
    controlAppContainer.style.display = isAppsMode ? "flex" : "none";

    return isAppsMode;
}

export { killBrowsers, resetItems, blockItems, switchSiteAppContainer };