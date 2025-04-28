function renderSites(sites) {
    const container = document.getElementById("site-container");
    container.innerHTML = "";

    const header = document.createElement("h2");
    header.textContent = "🌐 Сайты";
    container.appendChild(header);

    sites.forEach((site) => {
        const id = site.id;
        const siteBlock = document.createElement("div");
        siteBlock.className = "site-block";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = `site-${id}`;
        checkbox.checked = site.is_active || false;

        checkbox.addEventListener("change", () => {
            site.is_active = checkbox.checked;
            
            window.pywebview.api.updateSiteStatus(site.id, site.is_active);
        });

        const label = document.createElement("label");
        label.setAttribute("for", `site-${id}`);
        label.textContent = site.url;

        const siteRemoveBtn = document.createElement("button");
        siteRemoveBtn.textContent = "Удалить";
        siteRemoveBtn.className = "remove-btn";
        siteRemoveBtn.addEventListener("click", () => {
            removeSite(sites, id);
        });

        siteBlock.appendChild(checkbox);
        siteBlock.appendChild(label);
        siteBlock.appendChild(siteRemoveBtn);

        container.appendChild(siteBlock);
    });
}

function addSite(sites) {
    const input = document.getElementById("newSiteInput");
    const newUrl = input.value.trim();

    window.pywebview.api.addNewSite(newUrl)
        .then(siteFromDb => {
            sites.push(siteFromDb);
            input.value = "";
            renderSites(sites);
        })
        .catch(err => {
            console.error("Ошибка при добавлении сайта:", err);
        });
}

function removeSite(sites, id) {
    const index = sites.findIndex(s => s.id === id);
    const removedUrl = sites[index].url;

    window.pywebview.api.deleteSite(id, removedUrl)
        .then(response => {
            sites.splice(index, 1);
            renderSites(sites);
        })
        .catch(err => {
            console.error("Ошибка при удалении сайта:", err);
        });
}

export { renderSites, addSite, removeSite };