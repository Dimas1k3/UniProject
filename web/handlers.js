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
    console.log("🔥 confirmKill CLICKED");

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

export { killHandlers };