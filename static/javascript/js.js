const list = [];
const list_scheme = [];
var header = document.getElementById("top_2btn");
var btns = header.getElementsByClassName("btnsel");
for (var i = 0; i < btns.length; i++) {
	btns[i].addEventListener("click", function () {
		let current = document.getElementsByClassName("active");
		if (current.length > 0) {
			current[0].classList.remove("active");
		}
		this.classList.add("active");
		if (this.textContent != "Formularz") {
			let form = document.getElementById("form")
			form.style = "display: none;"
			let scheme = document.getElementById("scheme")
			scheme.style = "display: unset;"
		}
		else {
			let scheme = document.getElementById("scheme")
			scheme.style = "display: none;"
			let form = document.getElementById("form")
			form.style = "display: unset;"
		}

	});
}

var form_ol = document.getElementById("add_field");
var form_buttons = form_ol.getElementsByClassName("btn");
for (var i = 0; i < form_buttons.length; i++) {
	form_buttons[i].addEventListener("click", function () {
		if (document.getElementsByClassName("active")[0].textContent == "Formularz") {
			var form = document.getElementById("form");
			var li = document.createElement('li');
			li.style = "padding: 10px 10px; display: flex; align-items: center; gap: 10px;";
			li.className = "li";

			var button_up = document.createElement("button");
			button_up.textContent = "↑";
			button_up.style = "flex-shrink: 0;";
			button_up.className = "btn-sm";

			var button_down = document.createElement("button");
			button_down.textContent = "↓";
			button_down.style = "flex-shrink: 0;";
			button_down.className = "btn-sm";

			var button_delete = document.createElement("button");
			button_delete.textContent = "x";
			button_delete.style = "flex-shrink: 0; background: #f66; color: white; border: none; border-radius: 3px; padding: 2px 8px; cursor: pointer;";
			button_delete.className = "btn-sm";

			var text = document.createElement("h6");
			text.textContent = handleX(list, this.textContent);
			text.id = "element_text";
			list.push(handleX(list, this.textContent));
			//list.push[this.textContent];
			text.style = "flex-grow: 1; margin: 0;";

			uuh(li, button_up, button_down, button_delete, form);
			li.appendChild(button_up);
			li.appendChild(button_down);
			li.appendChild(text);
			li.appendChild(button_delete);
			form.appendChild(li);
		}
		else {
			let textarea = document.getElementById("scheme_text");
			textarea.value += " {" + handleX(list_scheme, this.textContent) + "} ";
			list_scheme.push(handleX(list_scheme, this.textContent));
		}
	});
}

function uuh(li, button_up, button_down, button_delete, form) {
	button_up.addEventListener("click", function () {
		const prev = li.previousElementSibling;
		if (prev) form.insertBefore(li, prev);
	});

	button_down.addEventListener("click", function () {
		const next = li.nextElementSibling;
		if (next) form.insertBefore(next, li);
	});

	button_delete.addEventListener("click", function () {
		let textElement = li.querySelector("#element_text");
		let index = list.indexOf(textElement.textContent);
		li.remove();
		list.splice(index, 1); // worx
	});
}

function handleX(list, element) {
	let count = 1;

	for (let item of list) {
		if (item.includes(element)) {
			count++;
		}
	}

	if (count === 1) {
		return (element);
	} else {
		return (element + count);
	}
}

var save_button = document.getElementById("save_button");
save_button.addEventListener("click", function () {
	if (document.getElementsByClassName("active")[0].textContent == "Formularz") {
		saveForm(list);
	}
	else {
		saveSchema(list);
	}
});

/*function getCSRFToken() {
	return document.querySelector('[name=csrfmiddlewaretoken]').value;
}*/

function saveForm(list) {
	fetch('/save_form/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			//'X-CSRFToken': getCSRFToken()
		},
		body: JSON.stringify(list)
	})
		.then(res => res.text())
		.then(msg => showSaveBanner(msg))
		.catch(err => console.error(err));
}

function saveSchema() {
	let textarea = document.getElementById("scheme_text");
	fetch('/save_schema/', {
		method: 'POST',
		headers: {
			'Content-Type': 'text/plain',
			//'X-CSRFToken': getCSRFToken()
		},
		body: textarea.value
	})
		.then(res => res.text())
		.then(msg => showSaveBanner(msg))
		.catch(err => console.error(err));
}

function showSaveBanner(message = "Save successful") {
	const banner = document.getElementById("saveBanner");
	banner.textContent = message;
	banner.style.display = "block";

	setTimeout(() => {
		banner.style.display = "none";
	}, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
	const savedList = document.getElementById("item_list");

	savedList.addEventListener("click", function (e) {
		const target = e.target.closest(".saved-item");
		if (!target) return;

		const filename = target.dataset.filename;
		const type = target.dataset.type;

		fetch('/' + filename)
			.then(res => res.text())
			.then(data => {
				if (type === ".json") {
					const form = document.getElementById("form");
					form.innerHTML = '';
					const list = JSON.parse(data);

					list.forEach(item => {
						const li = document.createElement('li');
						li.style = "padding: 10px 10px; display: flex; align-items: center; gap: 10px;";
						li.className = "li";

						const button_up = document.createElement("button");
						button_up.textContent = "↑";
						button_up.className = "btn-sm";
						button_up.style = "flex-shrink: 0;";

						const button_down = document.createElement("button");
						button_down.textContent = "↓";
						button_down.className = "btn-sm";
						button_down.style = "flex-shrink: 0;";

						const button_delete = document.createElement("button");
						button_delete.textContent = "x";
						button_delete.className = "btn-sm";
						button_delete.style = "flex-shrink: 0; background: #f66; color: white; border: none; border-radius: 3px; padding: 2px 8px; cursor: pointer;";

						const text = document.createElement("h6");
						text.textContent = item;
						text.id = "element_text";
						text.style = "flex-grow: 1; margin: 0;";
						list.push(item);

						uuh(li, button_up, button_down, button_delete, form);
						li.appendChild(button_up);
						li.appendChild(button_down);
						li.appendChild(text);
						li.appendChild(button_delete);
						form.appendChild(li);
					});

					document.getElementById("form_button").click();
				} else {
					document.getElementById("scheme_text").value = data;
					document.getElementById("scheme_button").click();
				}
			})
			.catch(err => {
				console.error("Failed to load file", err);
				alert("Could not load file: " + filename);
			});
	});
});
