import { isLoggedIn, toggleContentOnLogState } from "./Utils.js";
import { injectUserData } from "./User.js";
import { injectModule } from "./Modules.js";

class Page {
	constructor(name, urlPath, filePath, sidebar) {
		this.name = name;
		this.urlPath = urlPath;
		this.filePath = filePath;
		this.sidebar = sidebar;
	}
	async fetchHtml() {
		return await fetch(this.filePath).then((x) => x.text());
	}
}

const routes = [
	new Page("Dashboard", "/", "html/Dashboard.html", true),
	new Page("Dashboard", "/dash", "html/Dashboard.html", true),

	new Page("Sidebar", "", "html/Sidebar.html", false),

	new Page("About", "/about", "html/About.html", true),
	new Page("Game", "/game", "html/Game.html", true),
];

const mainPageDiv = "#content-container";
const sidebarDiv = "#sidebar-container";
let previousPage = null;

function setInnerHtml(elm, html) {
	elm.innerHTML = html;
	Array.from(elm.querySelectorAll("script")).forEach((oldScript) => {
		const newScript = document.createElement("script");
		Array.from(oldScript.attributes).forEach((attr) =>
			newScript.setAttribute(attr.name, attr.value)
		);
		newScript.appendChild(document.createTextNode(oldScript.innerHTML));
		oldScript.parentNode.replaceChild(newScript, oldScript);
	});
}

function navigateTo(url) {
	if (url !== location.pathname) {
		history.pushState({}, null, url);
		router(routes, mainPageDiv);
	}
	toggleContentOnLogState();
	injectUserData();
	toggleActiveTab(url);
}

const router = async (routes) => {
	const potentialMatches = routes.map((route) => {
		return {
			route: route,
			isMatch: location.pathname === route.urlPath,
		};
	});
	let match = potentialMatches.find((potentialMatch) => potentialMatch.isMatch);
	if (!match) {
		match = {
			route: routes[0],
			isMatch: true,
		};
		history.pushState({}, "", "/");
	}
	const page = match.route;
	const html = await page.fetchHtml();
	setInnerHtml(document.querySelector(mainPageDiv), html);
	if (
		page.sidebar == true &&
		(previousPage == null || previousPage.sidebar == false)
	) {
		setInnerHtml(document.querySelector(sidebarDiv), "");
		let sidebarHtml = await routes
			.find((elm) => elm.name === "Sidebar")
			.fetchHtml();
		setInnerHtml(document.querySelector(sidebarDiv), sidebarHtml);
	}
	if (page.sidebar == false)
		setInnerHtml(document.querySelector(sidebarDiv), "");
	previousPage = page;
	injectModule();
	toggleContentOnLogState();
	injectUserData();
	toggleActiveTab(location.pathname);
};

window.addEventListener("popstate", (event) => router(routes));

document.addEventListener("DOMContentLoaded", () => {
	document.body.addEventListener("click", (e) => {
		let target = e.target;
		while (
			target &&
			target.parentNode !== document.body &&
			!target.getAttribute("href")
		) {
			target = target.parentNode;
		}
		if (target && target.matches("[navlink]")) {
			e.preventDefault();
			navigateTo(target.getAttribute("href"));
		}
	});
	router(routes);
});

const logIn = new Event("logIn");
document.addEventListener("logIn", () => {
})

function toggleActiveTab(target) {
	var currentActive = document.querySelector(".active");
	if (currentActive != null)
		currentActive.classList.remove("active");
	if (target == "/")
		target = "/dash";
	if (target == "/dash" || target == "/game" || (target == "/about" && !isLoggedIn()))
		document.querySelector("a[href='" + target + "']").classList.add("active");
}

export { navigateTo, logIn, setInnerHtml };
