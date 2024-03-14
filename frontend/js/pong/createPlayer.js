import * as THREE from 'three';
import { Player } from "./Class/Player.js";
import { Paddle } from './Class/Paddle.js';
import { colors } from './varGlobal.js';

function createSpotLight(left, color, mesh, environment) {
	var light = new THREE.SpotLight(color, 200, 0, Math.PI / 4, 0.1);
	var light2 = new THREE.PointLight(color, 50);
	
	console.log(left);
	light.position.set(left, .5, 1).unproject(environment.camera);
	if (left < 0)
		light2.position.set(left - .4, .5, .5).unproject(environment.camera);
	else
		light2.position.set(left + .4, .5, .5).unproject(environment.camera);
	//environment.scene.add(light);
	environment.scene.add(light2);
	return ([light, light2]);
}


async function createPaddle(left, top, depth, color, environment) {
	const paddleGeometry = new THREE.BoxGeometry(0.2, 2, 1);
	const material = new THREE.MeshToonMaterial({ color: color });
	const mesh = new THREE.Mesh( paddleGeometry, material);
	
	mesh.position.set(left, top, depth).unproject(environment.camera);
	mesh.rotation.set(0, 0, 0);
	mesh.updateMatrix();
	environment.camera.updateProjectionMatrix();
	return (new Paddle(mesh));
}

async function createPlayer(left, top, depth, character, environment, name) {
	let color = colors.get(character);
	if (!color)
		color = "rgb(255, 255, 255)";

	const paddle = await createPaddle(left, top, depth, color, environment);
	paddle.mesh.name = "paddle_" + name;
	return (
		new Player(
			name,
			paddle,
			createSpotLight(left, color, depth, environment),
			environment.characters.get(character).clone()
	));
}

export { createPlayer, createPaddle };