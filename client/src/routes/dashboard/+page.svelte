<script>
	import Nav from '../../components/nav.svelte';
	import DashboardSideBar from '../../components/dashboardSideBar.svelte';
	import Student from '../../components/student.svelte';
	import currentUser from '$lib/stores/user';
</script>

<div class="sticky top-0 w-full z-40 bg-rural-blue h-28">
	<Nav />
</div>
<div class="flex flex-no-wrap">
	<div class="fixed z-30 bg-rural-blue">
		<DashboardSideBar />
	</div>
	<div
		style="min-height: 88vh;"
		class="md:ml-64 xl:ml-96 container items-center flex flex-col py-2 sm:py-10 md:w-4/5 w-11/12 px-6 overflow--y-scroll "
	>
    <div class="w-full">
        <form>   
            <label for="default-search" class="mb-2 text-sm font-medium sr-only dark:text-gray-300">Search</label>
            <div class="relative">
                <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                    <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
                <input type="search" id="default-search" class="block p-4 pl-10 w-full text-sm  bg-gray-50 rounded-lg border border-gray-200" placeholder="Search Student" required>
                <button type="submit" class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
            </div>
        </form>
    </div>
    <div class="mx-auto mt-10">
<div class="sm:px-6 2xl:container">
				<div class="grid gap-6 xl:grid-cols-3 lg:grid-cols-2">
					<div>
						<Student/>
					</div>
                    <div>
						<Student/>
					</div>
                    <div>
						<Student/>
					</div>
                    <div>
						<Student/>
					</div>
                    <div>
						<Student/>
					</div>
                    <div>
						<Student/>
					</div>
                    <div>
						<Student/>
					</div>
				</div>
			</div> 
    </div>

	</div>
</div>

<svelte:head>
	<title>Dashboard</title>
</svelte:head>

