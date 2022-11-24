<script>
	import { goto } from '$app/navigation';
	let mainMenu = 'none';
	let userMenu = 'none';
	const toggleMainMenu = () => {
		mainMenu = mainMenu === 'none' ? 'block' : 'none';
	};
	const toggleUserMenu = () => {
		userMenu = userMenu == 'none' ? 'block' : 'none';
	};
	let user = {};
</script>

<nav class="nav-blue-bg">
	<div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
		<div class="relative flex items-center justify-between h-16">
			<div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
				<!-- Mobile menu button-->
				<button
					on:click={toggleMainMenu}
					type="button"
					class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
					aria-controls="mobile-menu"
					aria-expanded="false"
				>
					<span class="sr-only">Open main menu</span>
					<svg
						class="block h-6 w-6"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h16M4 18h16"
						/>
					</svg>

					<svg
						class="hidden h-6 w-6"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>
			<div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                <div class="flex-shrink-0 flex items-center mt-10">
                    
					<img
						on:click={() => goto('/')}
						class="cursor-pointer block lg:hidden h-20 w-auto"
						src="/logo.png"
						alt="logo"
					/>
					<img
						on:click={() => goto('/')}
						class="hidden lg:block h-20 w-auto cursor-pointer"
						src="/logo.png"
						alt="logo"
					/>
				</div>
                <div>
                    <div class="hidden sm:block sm:ml-6 mt-14">
                        <div class="flex space-x-4">
                            <a
							href="/dashboard"
							class="cream-msg text-white px-3 py-2 rounded-md text-lg font-medium"
							aria-current="page">Dashboard</a
                            >
                            
                            <a
							href="/signup"
							class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-lg font-medium"
							>SignUp</a
                            >
                            <a
							href="/signin"
							class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-lg font-medium"
							>SignIn</a
                            >
                        </div>
                    </div>
                </div>
                </div>
                <div
				class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0 mt-9"
			>
				<button
                type="button"
                class="bg-gray-800 p-1 rounded-full text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
				>
                <span class="sr-only">View notifications</span>
                <!-- Heroicon name: outline/bell -->
                <svg
                class="h-6 w-6"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
						/>
					</svg>
				</button>

				<!-- Profile dropdown -->
				<div class="ml-3 relative">
					<div>
						<button
							type="button"
							class="bg-gray-800 flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
							id="user-menu-button"
							aria-expanded="false"
							aria-haspopup="true"
						>
							<span class="sr-only">Open user menu</span>
							<img
								on:click={toggleUserMenu}
								class="h-8 w-8 rounded-full border-2 border-yellow-500"
								src={user.photo}
								alt=""
							/>
						</button>
					</div>

					<div
						style="display: {userMenu};"
						class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
						role="menu"
						aria-orientation="vertical"
						aria-labelledby="user-menu-button"
						tabindex="-1"
					>
						<button
							class="block px-4 py-2 text-sm text-gray-700"
							role="menuitem"
							tabindex="-1"
							id="user-menu-item-0">Your Profile</button
						>
						<button
							class="block px-4 py-2 text-sm text-gray-700"
							role="menuitem"
							tabindex="-1"
							id="user-menu-item-1">Settings</button
						>
						<button
							on:click={() => {
								localStorage.removeItem('access_token');
								window.location.reload();
								goto('/');
							}}
							class="block px-4 py-2 text-sm text-gray-700"
							role="menuitem"
							tabindex="-1"
							id="user-menu-item-2">Sign out</button
						>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Mobile menu, show/hide based on menu state. -->
	<div style="display: {mainMenu};" id="mobile-menu" class="bg-rural-blue">
		<div class="px-2 pt-2 pb-3 space-y-1">
			<!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
			<a
				href="/dashboard"
				class="cream-msg text-white block px-3 py-2 rounded-md text-base font-medium"
				aria-current="page">Dashboard</a
			>
			<a
				href="/signup"
				class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
				>SignUp</a
			>
			<a
				href="/signin"
				class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
				>SignIn</a
			>
		</div>
	</div>
</nav>

