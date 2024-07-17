import { resize, isFullScreen } from "../pong/resize.js";
import { checkCollision } from "../pong/collision.js";
import { displayMainMenu, createSelectMenu, createOnlineMenu, createLocalMenu } from '../pong/menu.js';
import { handleKeyPress, handleMenuKeyPress } from '../pong/handleKeyPress.js';
import { displayCharacter, updateMixers } from '../pong/displayCharacter.js';
import { initGame } from "../pong/initGame.js";
import { createEndScreen, returnToMenu } from "../pong/createEndScreen.js"
import { actualizeScore } from "../pong/score.js";
import { createField } from "../pong/createField.js";
import { createOnlineSelectMenu } from "../pong/online.js";
import { ClearAllEnv, getSize } from "../pong/createEnvironment.js";
import { loadAllModel } from "../pong/loadModels.js"
import { loadScene } from "../pong/loadModels.js";
import { getUserData } from "../User.js";
import { sendTournamentForm, createFormTournament } from "../pong/createTournament.js";
import { createJoinTournamentMenu } from "../pong/joinTournament.js";
import { checkIfUserIsInTournament, connectToTournament } from "../pong/tournament.js";
import { showAlert } from "../Utils.js";
import { injectGameTranslations } from "../modules/translationsModule/translationsModule.js";
import { trainModel, storeData, createModel, moveAI } from "../pong/AI/AI.js"
import * as THREE from 'three';
import { getState } from "../pong/AI/envForAI.js";

export var lobby;
export var clock;
export var characters;
export var soloMode;
export var environment;
export var states = [];
export var actions = [];
export var currentActions = [];

export async function init(queryParams) {
	if (queryParams && queryParams.get("message"))
		showAlert(queryParams.get("message"), queryParams.get("success"));

	var target = document.querySelector('#game');
	var config = { attributes: true, childList: true, characterData: true };
	var observer = new MutationObserver(function (mutations) {
		mutations.forEach(injectGameTranslations);
	});
	observer.observe(target, config);

	lobby = await loadScene('lobbyTest');
	clock = new THREE.Clock();
	characters = new Map();
	let start = false;
	let divMenu = document.getElementById("menu");
	let player1;
	let player2;
	let keyPress = false;
	let keysPressed = {};
	let isOnline = false;
	let localLoop = false;
	let userData;
	let form;
	let model;

	const gameDiv = document.getElementById('game');
	const field = await createField();
	soloMode = false;

	loadAllModel();

	getUserData().then((data) => {
		userData = data;
		if (userData) {
			checkIfUserIsInTournament(userData).then((response) => {
				if (response && response['joined'])
					connectToTournament(response['tournament']);
			});
		}
	})
	async function goToLocalSelectMenu() {
		divMenu = document.getElementById("localMenu");
		divMenu.remove();
		environment = createSelectMenu(field, characters);
		player1 = await displayCharacter(player1, environment, "chupacabra", "player1");
		player2 = await displayCharacter(player2, environment, "elvis", "player2");
	}

	async function createAISelectMenu(field) {
		document.getElementById("localMenu").remove();
		environment = createSelectMenu(field, characters);
		document.getElementById("cursorP2").remove();
		document.getElementsByClassName("inputP2")[0].remove();
		environment.renderer.render(environment.scene, environment.camera);
		player1 = await displayCharacter(player1, environment, "chupacabra", "player1");
		player2 = await displayCharacter(player2, environment, "elvis", "player2");
		}

	gameDiv.addEventListener("keydown", function (event) {
		keysPressed[event.key] = true;
		if (keysPressed['A'])
			keysPressed['a'] = true;
		if (keysPressed['D'])
			keysPressed['d'] = true;
		if (keysPressed['W'])
			keysPressed['w'] = true;
		if (keysPressed['S'])
			keysPressed['s'] = true;
		keyPress = true;
		event.stopPropagation();
	});

	gameDiv.addEventListener("keyup", function (event) {
		delete keysPressed[event.key];
	});

	gameDiv.addEventListener('click', function (event) {
		document.body.style.overflow = 'hidden';
		gameDiv.focus();
		if (!gameDiv.contains(event.target)) {
			document.body.style.overflow = 'auto';
		}
	});

	gameDiv.addEventListener("click", function (event) {
		getUserData().then((data) => {
			userData = data;
		})

		if (userData) {
			checkIfUserIsInTournament(userData).then((response) => {
				if (response && response['joined'])
					connectToTournament(response['tournament']);
			});
		}

		if (event.target.id == 'restart' && !isOnline) {
			document.getElementById("endscreen").remove();
			actualizeScore(player1, player2, environment, environment.font);
			start = true;
		}
		if (event.target.id == 'backMenu' || event.target.id == 'backIcon') {
			localLoop = false;
			isOnline = false;
			ClearAllEnv(environment);
			returnToMenu();
		}
		if (event.target.id == 'localGame') {
			localLoop = true;
			createLocalMenu(field);
		}
		if (event.target.id == '1v1') {
			soloMode = false;
			localGameLoop();
			goToLocalSelectMenu();
		}
		if (event.target.id == 'easy') {
			soloMode = true;
			localGameLoop();
			createAISelectMenu(field);
		}
		if (event.target.id == 'onlineGame' && userData) {
			isOnline = true;
			createOnlineMenu(field);
		}
		if (event.target.id == 'quick') {
			createOnlineSelectMenu(field);
		}
		if (event.target.id == 'create') {
			createFormTournament();
			form = document.getElementById("tournamentForm");
			form.addEventListener('submit', function (event) {
				event.preventDefault();
				sendTournamentForm(form);
			});
		}
		if (event.target.id == 'join') {
			createJoinTournamentMenu();
		}
		if (event.target.id == 'fullScreen') {
			if (!isFullScreen())
				gameDiv.requestFullscreen();
			else
				document.exitFullscreen();
		}
		if (event.target.id == 'toggleButton') {
			const div = document.getElementById('toggleDiv');
			if (div.classList.contains('hidden'))
				div.classList.remove('hidden');
			else
				div.classList.add('hidden');
		}
	});

	gameDiv.addEventListener('fullscreenchange', function () {
		if (isFullScreen())
			resize(environment);
	});

	async function setIfGameIsEnd() {
		if (player1.score < 5 && player2.score < 5)
			return;
		
		if (localLoop) {
			console.log("States : ", states.length, " | Actions : ", actions.length);
			await trainModel(model, 500);
		}
		let winner = player1.name;
		if (player2.score > player1.score)
			winner = player2.name;
		createEndScreen(winner);
		start = false;
		player1.score = 0;
		player2.score = 0;
	}


	async function localGameLoop() {
		if (keyPress && !start) {
			await handleMenuKeyPress(keysPressed, player1, player2, environment);
			keyPress = false;
		}
		if (keysPressed[" "] && document.getElementById("selectMenu") && player1 && player2 && !start) {
			start = true;
			ClearAllEnv(environment);
			if (!soloMode)
				divMenu.remove();   
			model = await tf.loadLayersModel('https://127.0.0.1:8000/js/pong/AI/model/model.json');
			model.compile({
				optimizer: tf.train.adam(0.001),
				loss: 'meanSquaredError'
			});
		environment = await initGame(player1, player2);
		}
		if (start) {
			let action = 0;
			let actualState = getState(environment, player2);
			if (keyPress)
				action = handleKeyPress(keysPressed, player1, player2, environment);
			if (soloMode)
				action = moveAI(player2, environment, model)
			storeData(actualState, action);
			checkCollision(environment.ball, player1, player2, environment);
			await setIfGameIsEnd();
		}
		if (player1 && player2)
			updateMixers(player1, player2);
		environment?.renderer.render(environment.scene, environment.camera);
		if (localLoop)
			requestAnimationFrame(localGameLoop);
	}
}


export { displayMainMenu }