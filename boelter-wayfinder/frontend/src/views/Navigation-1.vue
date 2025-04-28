<template>
  <!-- navigator -->
  <v-container class="nav">
    <v-row class="btn-col">
      <!-- icons -->
      <v-col cols="auto" class="d-flex flex-column justify-center no-col-padding no-bot-padding">
        <v-btn icon @click="router.push('/')" class="elevation-0">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-btn icon @click="swapInputs"  class="elevation-0 no-margin swap-btn" >
          <v-icon>mdi-swap-vertical</v-icon>
        </v-btn>
      </v-col>

      <v-col class="no-bot-padding no-left-padding">
        <!-- start input -->
        <v-autocomplete
          v-model="start"
          :items="roomOptions"
          item-title="label"
          item-value="value"
          label="Start"
          outlined
          dense
          class="input-field"
          density="comfortable"
          lable="comfortable"
        >
          <template #prepend-inner>
            <img src="@/assets/circle-orange.svg" alt="Start Icon" style="width: 20px; height: 20px;" />
          </template>
        </v-autocomplete>

      <!-- destination input -->
        <v-autocomplete
          v-model="destination"
          :items="roomOptions"
          item-title="label"
          item-value="value"
          label="Destination"
          outlined
          dense
          density="comfortable"
          lable="comfortable"
        >
          <template #prepend-inner>
            <img src="@/assets/pin-blue.svg" alt="Destination Icon" style="width: 20px; height: 20px;" />
          </template>
        </v-autocomplete>
      </v-col>
    </v-row>


    <v-divider class="my-4" />

    <!-- Conditional rendering of result -->
    <FloorPlan
      v-if="start && destination && start !== destination"
      :start="start"
      :destination="destination"
    />
    <InvalidStateFloorPlan v-else-if="start && destination && start === destination"/>
    <NullStateFloorPlan v-else/>
  </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import FloorPlan from '../components/FloorPlan.vue'
  import NullStateFloorPlan from '../components/NullStateFloorPlan.vue'
  import InvalidStateFloorPlan from '../components/InvalidStateFloorPlan.vue'
  import rooms from '@/data/rooms.json'
  import '@mdi/font/css/materialdesignicons.css'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const logo = new URL('@/assets/logo.svg', import.meta.url).href
  const route = useRoute()
  const destination = ref('')
  const start = ref('')
  const roomOptions = Object.keys(rooms).map(key => ({
    label: key,
    value: key
  }))

  const swapInputs = () => {
    const temp = start.value
    start.value = destination.value
    destination.value = temp
  }
  
  
  onMounted(() => {
    destination.value = route.query.destination || ''
  })
</script>  

<style scoped>
.page {
  margin-left: 5px;
  margin-right: 5px;
}
.input-field {
  margin-bottom: -10px;
}
.no-col-padding {
  padding-left: 0 !important;
  padding-right: 0 !important;
}
.no-bot-padding {
  padding-bottom: 0 !important;
}
.no-left-padding {
  padding-left: 0 !important;
}
</style>