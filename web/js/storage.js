function saveTasksToLocal(tasks) {
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

function loadTasksFromLocal() {
    const stored = localStorage.getItem("tasks");
    return stored ? JSON.parse(stored) : [];
}

function saveSitesToLocal(sites) {
    localStorage.setItem("sites", JSON.stringify(sites));
}

function loadSitesFromLocal() {
    const stored = localStorage.getItem("sites");
    return stored ? JSON.parse(stored) : [];
}

function saveAppsToLocal(apps) {
    localStorage.setItem("apps", JSON.stringify(apps));
}

function loadAppsFromLocal() {
    const stored = localStorage.getItem("apps");
    return stored ? JSON.parse(stored) : [];
}

export {
    saveTasksToLocal,
    loadTasksFromLocal,
    saveSitesToLocal,
    loadSitesFromLocal,
    saveAppsToLocal,
    loadAppsFromLocal
}