   <script>
    import {env} from '$lib/env.js';
    import { goto } from '$app/navigation';
    import currentUser from '$lib/stores/user.js';
    let username = '';
    let password = '';

    const signin = (async () => {
				try {
					const rawResponse = await fetch(env.API_URL + '/auth', {
						method: 'POST',
						headers: {
							Accept: 'application/json',
							'Content-Type': 'application/json'
						},
						body: JSON.stringify({username, password})
					});
					const response = await rawResponse.json();
          if (response.access_token) {
              let access_token = response.access_token; 
              localStorage.setItem('access_token', access_token);
              currentUser.set({username, access_token});
              goto('/dashboard');
          }
				} catch (error) {
					console.error(error);
				}
			});
   </script>
   <!-- ====== Banner Section Start -->
    <div
      class="
        relative
        z-10
        pt-[120px]
        md:pt-[130px]
        lg:pt-[160px]
        pb-[100px]
        bg-primary
        overflow-hidden
      "
    >
      <div class="container">
        <div class="flex flex-wrap items-center -mx-4">
          <div class="w-full px-4">
            <div class="text-center">
              <h1 class="font-semibold text-white text-4xl">Log In Page</h1>
            </div>
          </div>
        </div>
      </div>
      <div>
        <span class="absolute top-0 left-0 z-[-1]">
          <svg
            width="495"
            height="470"
            viewBox="0 0 495 470"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="55"
              cy="442"
              r="138"
              stroke="white"
              stroke-opacity="0.04"
              stroke-width="50"
            />
            <circle
              cx="446"
              r="39"
              stroke="white"
              stroke-opacity="0.04"
              stroke-width="20"
            />
            <path
              d="M245.406 137.609L233.985 94.9852L276.609 106.406L245.406 137.609Z"
              stroke="white"
              stroke-opacity="0.08"
              stroke-width="12"
            />
          </svg>
        </span>
        <span class="absolute top-0 right-0 z-[-1]">
          <svg
            width="493"
            height="470"
            viewBox="0 0 493 470"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="462"
              cy="5"
              r="138"
              stroke="white"
              stroke-opacity="0.04"
              stroke-width="50"
            />
            <circle
              cx="49"
              cy="470"
              r="39"
              stroke="white"
              stroke-opacity="0.04"
              stroke-width="20"
            />
            <path
              d="M222.393 226.701L272.808 213.192L259.299 263.607L222.393 226.701Z"
              stroke="white"
              stroke-opacity="0.06"
              stroke-width="13"
            />
          </svg>
        </span>
      </div>
    </div>
    <!-- ====== Banner Section End -->

    <!-- ====== Forms Section Start -->
    <section class="bg-[#F4F7FF] py-14 lg:py-20">
      <div class="container">
        <div class="flex flex-wrap -mx-4">
          <div class="w-full px-4">
            <div
              class="
                max-w-[525px]
                mx-auto
                text-center
                bg-white
                rounded-lg
                relative
                overflow-hidden
                py-14
                px-8
                sm:px-12
                md:px-[60px]
              "
            >
              <div class="mb-10 text-center">
                <a
                  href="/"
                  class="inline-block max-w-[160px] mx-auto"
                >
                  <img src="/logo.png" alt="logo" />
                </a>
              </div>
              <form>
                <div class="mb-6">
                  <input
                    type="text"
                    placeholder="Username"
                    bind:value={username}
                    class="
                      w-full
                      rounded-md
                      border
                      bordder-[#E9EDF4]
                      py-3
                      px-5
                      bg-[#FCFDFE]
                      text-base text-body-color
                      placeholder-[#ACB6BE]
                      outline-none
                      focus-visible:shadow-none
                      focus:border-primary
                    "
                  />
                </div>
                <div class="mb-6">
                  <input
                    type="password"
                    placeholder="Password"
                    bind:value={password}
                    class="
                      w-full
                      rounded-md
                      border
                      bordder-[#E9EDF4]
                      py-3
                      px-5
                      bg-[#FCFDFE]
                      text-base text-body-color
                      placeholder-[#ACB6BE]
                      outline-none
                      focus-visible:shadow-none
                      focus:border-primary
                    "
                  />
                </div>
                <div class="mb-10">
                  <input
                    type="submit"
                    on:click|preventDefault={signin}
                    value="Sign In"
                    class="
                      w-full
                      rounded-md
                      border
                      bordder-primary
                      py-3
                      px-5
                      bg-primary
                      text-base text-white
                      cursor-pointer
                      hover:shadow-md
                    "
                  />
                </div>
              </form>
           
              <p class="text-base text-[#adadad]">
                Not a member yet?
                <a href="/signup" class="text-primary hover:underline">
                  Sign Up
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

<svelte:head>
	<title>Login</title>
</svelte:head>

