<template>
  <div class="page-container">
    <v-container class="fill-height d-flex flex-column justify-center align-center text-center">
    <!-- title -->
    <div class="title">
      <v-img :src="logo" width="50" />
      <div class="title-text">
        <h2 class="mt-4 font-weight-bold">Boelter Wayfinder</h2>
      </div>
    </div>

    <!-- search bar -->
    <v-autocomplete
      v-model="destination"
      :items="destinationOptions"
      item-title="label"
      item-value="value"
      prepend-inner-icon="mdi-magnify"
      placeholder="Where do you want to go?"
      outlined
      dense
      class="search-bar"
    />
    <!-- suggestions -->
    <div class="mt-4 text-left w-100">
      <div class="subtitle">Suggested Destinations</div>
      <v-chip-group
        class="d-flex flex-wrap"
        column="false"
      >
        <v-chip
          v-for="item in suggestions"
          :key="item"
          class="ma-1"
          @click="selectDestination(item)"
          color="grey-lighten-2"
        >
          {{ item }}
        </v-chip>
      </v-chip-group>

    </div>
  </v-container>
  </div>
</template>
  
<script setup>
  import { ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import rooms from '@/data/rooms.json'
  import '@mdi/font/css/materialdesignicons.css'
  
  const logo = new URL('@/assets/logo.svg', import.meta.url).href

  const destination = ref(null)
  const destinationOptions = Object.keys(rooms).map(key => ({
    label: key,
    value: key
  }))

  const router = useRouter()
  const suggestions = [
    'Engineering Library', 
    '8500', 
    '8251',
    '3400',
    'Restroom (W)', 
    'Restroom (M)',
    'Restroom (All Gender)', 
  ]
  
  const selectDestination = (dest) => {
    destination.value = dest
  }
  
  watch(destination, (newVal) => {
    if (newVal && router.currentRoute.value.name !== 'Navigation') {
      router.push({ name: 'Navigation', query: { destination: newVal } })
    }
  })

</script>

<style scoped>
.page-container {
  width: 90%;
}
.title {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 30px;
  margin-top: 40%;
}
.search-bar {
  width: 100%;
  padding-left: 5px;
}
.subtitle{
  color: gray;
  margin-left: 5px;
}

</style>