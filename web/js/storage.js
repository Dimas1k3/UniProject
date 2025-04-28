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

export {
    saveTasksToLocal,
    loadTasksFromLocal,
    saveSitesToLocal,
    loadSitesFromLocal
};
