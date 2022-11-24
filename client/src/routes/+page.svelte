<script>
    import Nav from '../components/nav.svelte';
	import {env} from '$lib/env.js';
</script>

<div class="bg-rural-blue h-28">
    <Nav />
</div>
<div class="w-full h-full flex flex-col items-center">
    <div class="h-52"></div>
    <div>
        Student Conduct Tracker
		{env.API_URL}
    </div>
</div>

<svelte:head>
	<title>Home</title>
	<link rel="icon" href="https://i.imgur.com/0CUwW1S.jpeg" />
	<style>
		body {
			background-color: #f4f4f3;
		}
	</style>
</svelte:head>