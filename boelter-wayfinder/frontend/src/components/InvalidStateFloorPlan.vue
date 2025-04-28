<template>
    <div class="error-container">
        <div>
            <img class="error-icon" src="@/assets/error-state.svg" />
        </div>
        <div>
            Specify a different starting point / destination for directions.
        </div>
    </div>
</template>
  
<style>
    .error-icon {
        width: 45%;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    .error-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center; /* optional: if you want to center vertically too */
        text-align: center; /* centers the text inside the div */
    }
</style>