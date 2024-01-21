<script>
	// export let name;
	import { onMount } from 'svelte';
	let data;
	let food1 = 'pizza';
	let food2 = 'cake';
	
	async function getFoods() {
		console.log('getFoods')
		try {
			// const serverDomain = process.env.NODE_ENV === 'development'
			// ? 'http://localhost:5000'
			// : ''; // Replace '' with your hosted domain
			const response = await fetch(`/api/getFoods`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			data = await response.json();
			food1 = data.food1.name;
			food2 = data.food2.name;
			console.log(data);
			}
		catch (err) {
			console.log(err);
		}
	}

	async function food1Win() {
		updateFoods(food1, food2)
	}

	async function food2Win() {
		updateFoods(food2, food1)
	}

	async function updateFoods(winner, loser) {
		try {
			const response = await fetch(`/api/updateFoods`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({winner, loser})
			});

			data = await response.json();
			getFoods();
			}
		catch (err) {
			console.log(err);
		
		}
	}
	onMount(() => {
		getFoods();
	});
</script>

<main>
	
	<h1>30 Minute Food Compare</h1>
	<foods>
		<div>
			<button on:click={food1Win}> 
				<img src={'static/' + food1 + '.jpg'} alt={food1}>
			</button>
			<h2>{food1}</h2>
		</div>
		<div>
			<button on:click={food2Win}> 
				<img src={'static/' + food2 + '.jpg'} alt={food2}>
			</button>
			<h2>{food2}</h2>
		</div>
	</foods>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
		align-items: center;
	}
	
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	img {
		width: 200px;
		height: auto;
	}

	foods {
		display: flex;
		gap: 10%;
		justify-content: center;
		align-items: center;
		flex-direction: row;
	}

</style>