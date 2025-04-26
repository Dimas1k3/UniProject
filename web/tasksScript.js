function renderTasks(tasks) {
    console.info(tasks);
    const container = document.getElementById("task-container");
    container.innerHTML = "";

    const header = document.createElement("h2");
    header.textContent = "📝 Задачи";
    container.appendChild(header);

    tasks.forEach((task) => {
        const id = task.id
        const taskBlock = document.createElement("div");
        taskBlock.className = "task-block";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = `task-${id}`;
        checkbox.checked = task.done || false;
        checkbox.addEventListener("change", () => {
            task.done = checkbox.checked;
            
            window.pywebview.api.updateTaskStatus(task.id, task.done);
        });

        const label = document.createElement("label");
        label.setAttribute("for", `task-${id}`);
        label.textContent = task.title;

        const taskRemoveBtn = document.createElement("button");
        taskRemoveBtn.textContent = "Удалить";
        taskRemoveBtn.className = "remove-btn";
        taskRemoveBtn.addEventListener("click", () => {
            removeTask(tasks, id); 
        });

        taskBlock.appendChild(checkbox);
        taskBlock.appendChild(label);
        taskBlock.appendChild(taskRemoveBtn);

        container.appendChild(taskBlock);
    });
}

function addTask(tasks) {
    const input = document.getElementById("newTaskInput");
    const newTask = input.value.trim();

    window.pywebview.api.addNewTask(newTask)
        .then(newTask => {
            // console.info(newTask); 

            tasks.push(newTask);
            input.value = "";
            renderTasks(tasks);
        })
        .catch(err => {
            console.error("Ошибка при добавлении задачи:", err);
        });
}

function removeTask(tasks, id) {
    const index = tasks.findIndex(t => t.id === id);
    const removedTaskTitle = tasks[index].title;

    window.pywebview.api.deleteTask(id, removedTaskTitle)
        .then(response => {
            // console.info(response); 

            tasks.splice(index, 1);
            renderTasks(tasks);
        })
        .catch(err => {
            console.error("Ошибка при удалении задачи:", err);
        });
}

export { renderTasks, addTask, removeTask };