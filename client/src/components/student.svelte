<script>
	import { onMount } from "svelte";
    let edit = "hidden";
    let view = "";

    let name = "Daniel Yatali";
    let studentID = "816024289";
    let degree = "Computer Science Special";

    let updateName = "";
    let updateStudentID = "";
    let updateDegree = "";


    const editHandler = () => {
        if (edit == "hidden") {
            edit = "";
            view = "hidden";
            updateName = name;
            updateStudentID = studentID;
            updateDegree = degree;
        } else {
            edit = "hidden";
            view = "";
        }
    }
    const saveHandler = () => {
        editHandler();
        name = updateName;
        studentID = updateStudentID;
        degree = updateDegree;

    //Todo
    //Take data and make put request to update student
    };
</script>




<div class="main">
   <!--card-->
   <div class="relative card bg-white flex flex-col items-center justify-center p-4 shadow-lg rounded-2xl w-64">
      <!--profile-image-->
      <div class="absolute top-0 right-0 p-4 cursor-pointer {view}" on:click={editHandler}>
         <svg class="h-8 w-8 text-gray-500"  fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
         </svg>
      </div>
      <div class="absolute top-0 right-0 p-4 cursor-pointer {edit}" on:click={editHandler}>
<svg class="h-8 w-8 text-gray-500"  fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
</svg>

      </div>
      <div class="image rounded-full p-2 shadow-2xl">
         <div class="profile mx-auto rounded-full w-24 text-blue-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24" viewBox="0 0 20 20" fill="currentColor">
               <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
         </div>
      </div>
      <!-- Start View -->
      <div class="{view} text-center">
         <div class="text-gray-800 text-2xl font-medium mt-4">
            <p>{name}</p>
         </div>
         <div class=" text-gray-500">
            <p>{studentID}</p>
         </div>
         <div class=" text-gray-700 mt-4">
            <p>{degree}</p>
         </div>
         <div class="w-full mt-8">
            <button class="bg-blue-500 py-2 px-4 hover:bg-blue-600 text-white w-full font-semibold rounded-lg shadow-lg">Karma 7</button>
         </div>
      </div>
    <!-- End View -->
      <!-- Start Edit -->
      <div class="{edit} mt-5">
             <form>
                    <div class="mb-3">
                        <input
                    type="text"
                    placeholder="Student ID"
                    bind:value="{updateStudentID}"
                    class="
                    w-full
                    rounded-md
                    border
                    bordder-[#E9EDF4]
                    py-2
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
                <div class="mb-3">
                    <input
                    type="text"
                    placeholder="Name"
                    bind:value="{updateName}"
                    class="
                    w-full
                    rounded-md
                    border
                    bordder-[#E9EDF4]
                    py-2
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
                 <div class="mb-3">
                        <input
                        bind:value="{updateDegree}"
                    type="text"
                    placeholder="Degree"
                    class="
                    w-full
                    rounded-md
                    border
                    bordder-[#E9EDF4]
                    py-2
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
                 <div class="w-full mt-2">
            <button class="bg-blue-500 py-2 px-4 hover:bg-blue-600 text-white w-full font-semibold rounded-lg shadow-lg" on:click|preventDefault={saveHandler}>Save</button>
         </div>
              </form>
      </div>
   </div>
</div>