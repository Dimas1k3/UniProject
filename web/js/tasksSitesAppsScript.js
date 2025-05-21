function renderItems(type, items, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    const header = document.createElement("h2");
    header.textContent = {
        site: "🌐 Websites",
        app: "💻 Applications",
        task: "📝 Tasks"
    }[type];

    container.appendChild(header);
    console.info(type, items, containerId);
    items.forEach((item) => {
        const id = item.id;
        const block = document.createElement("div");
        block.className = `${type}-block`;

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = `${type}-${id}`;
        const isChecked = type === "task" ? item.is_done : item.is_active || false;
        checkbox.checked = isChecked;

        checkbox.addEventListener("change", () => {
            const status = checkbox.checked;
            if (type === "task") item.done = status;
            else item.is_active = status;

            window.pywebview.api.updateStatus(type, id, status);
        });

        const label = document.createElement("label");
        label.setAttribute("for", `${type}-${id}`);
        if (type === "task") {
            label.textContent = item.title;
        } else if (type === "site") {
            label.textContent = item.url;
        } else {
            label.textContent = item.name;
        }

        const removeBtn = document.createElement("button");
        removeBtn.textContent = "Delete";
        removeBtn.className = "remove-btn";
        removeBtn.addEventListener("click", () => {
            removeItem(type, items, id, containerId);
        });

        block.appendChild(checkbox);
        block.appendChild(label);
        block.appendChild(removeBtn);
        container.appendChild(block);
    });
}

function addItem(type, items, containerId) {
    const inputId = {
        site: "newSiteInput",
        app: "newAppInput",
        task: "newTaskInput"
    }[type];

    const input = document.getElementById(inputId);
    const value = input.value.trim();
    
    if (!value) return;

    window.pywebview.api.addItem(type, value)
        .then(newItem => {
            items.push(newItem);
            input.value = "";
            console.info(items);
            renderItems(type, items, containerId);
        })
        .catch(err => {
            console.error(`Error while adding ${type}:`, err);
        });
}

function removeItem(type, items, id, containerId) {
    const index = items.findIndex(i => i.id === id);
    const label = type === "task" ? items[index].title : items[index].url;

    window.pywebview.api.deleteItem(type, id, label)
        .then(() => {
            items.splice(index, 1);
            renderItems(type, items, containerId);
        })
        .catch(err => {
            console.error(`Error while deleting ${type}:`, err);
        });
}

export { renderItems, addItem, removeItem };