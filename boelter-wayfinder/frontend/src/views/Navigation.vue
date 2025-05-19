<template>
  <!-- desktop view -->
    <v-container v-if="mdAndUp" class="nav-web fill-height d-flex flex-column justify-center align-center">
      <div class="fixed-header">
        <!-- header -->
        <div class="title-web" @click="router.push('/')">
          <img src="@/assets/logo.svg" class="logo-web"/>
          <div>
              <h1 class="mt-4 ml-4 font-weight-bold title-text-web">Boelter Wayfinder</h1>
          </div>
        </div>
        <!-- input field -->
        <v-row>
          <v-autocomplete
            v-model="start"
            :items="roomOptions"
            item-title="label"
            item-value="value"
            label="Start"
            outlined
            dense
            density="comfortable"
            lable="comfortable"
            :width="400"
          >
            <template #prepend-inner>
              <img src="@/assets/circle-orange.svg" alt="Start Icon" style="width: 20px; height: 20px;" />
            </template>
          </v-autocomplete>

        <v-btn icon @click="swapInputs"  class="elevation-2 ml-4 mr-4">
          <v-icon>mdi-swap-horizontal</v-icon>
        </v-btn>

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
          :width="400"
        >
          <template #prepend-inner>
            <img src="@/assets/pin-blue.svg" alt="Destination Icon" style="width: 20px; height: 20px;" />
          </template>
        </v-autocomplete>
      </v-row>

      <v-divider class="my-4" />
      
    </div>

      <div class="scrollable-content">
        <!-- Conditional rendering of result -->
        <FloorPlan
          v-if="start && destination && start !== destination"
          :start="start"
          :destination="destination"
        />
        <InvalidStateFloorPlan v-else-if="start && destination && start === destination"/>
        <NullStateFloorPlan v-else/>
      </div>
    </v-container>


  <!-- mobile view -->
    <v-container v-else class="nav">

      <div class="fixed-header">
        <v-row class="input-field">
            <v-autocomplete
              v-model="start"
              :items="roomOptions"
              item-title="label"
              item-value="value"
              label="Start"
              outlined
              dense
              density="comfortable"
              lable="comfortable"
            >
              <template #prepend-inner>
                <img src="@/assets/circle-orange.svg" alt="Start Icon" style="width: 20px; height: 20px;" />
              </template>
            </v-autocomplete>

            <v-btn icon @click="router.push('/')" class="elevation-0">
              <v-icon>mdi-close</v-icon>
            </v-btn>
        </v-row>

        <v-row class="input-field">
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
            <v-btn icon @click="swapInputs"  class="elevation-0" >
              <v-icon>mdi-swap-vertical</v-icon>
            </v-btn>
        </v-row>
        <v-divider class="my-4" />
      </div>

      <div class="scrollable-content">
        <!-- Conditional rendering of result -->
        <FloorPlan
          v-if="start && destination && start !== destination"
          :start="start"
          :destination="destination"
        />
        <InvalidStateFloorPlan v-else-if="start && destination && start === destination"/>
        <NullStateFloorPlan v-else/>
      </div>
    </v-container>



</template>
    
<script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import FloorPlan from '../components/FloorPlan.vue'
  import NullStateFloorPlan from '../components/NullStateFloorPlan.vue'
  import InvalidStateFloorPlan from '../components/InvalidStateFloorPlan.vue'
  import rooms from '@/data/rooms.json'
  import '@mdi/font/css/materialdesignicons.css'
  import { useRouter } from 'vue-router'
  import { useDisplay } from 'vuetify'
  const { mdAndUp } = useDisplay() // > 960px

  const router = useRouter()
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
    start.value = route.query.start || ''
    destination.value = route.query.destination || ''
  })

  watch(
    () => [route.query.start, route.query.destination],
    ([newStart, newDest]) => {
      start.value = newStart || ''
      destination.value = newDest || ''
    }
  )

  watch([start, destination], ([newStart, newDestination]) => {
    router.replace({
      path: '/route',
      query: {
        start: newStart,
        destination: newDestination
      }
    })
  })
</script>  

<style scoped>
.input-field {
  margin-bottom: -10px;
  padding-left: 12px;
  margin-top: 12px;
}
.fixed-header {
  flex-shrink: 0;
  background-color: white; /* keep header visible */
  z-index: 1;
  max-height: 40vh;
}
.scrollable-content {
  flex-grow: 1;
  overflow-y: auto;
  padding-top: 12px;
}
.nav {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.nav-web {
  margin-top: 10px;
}
.title-web {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 50px;
  cursor: pointer;
}
.logo-web {
  width: 50px;
}
.title-text-web {
  font-size: 24px;
}
.input-web {
  width: 20px;
}
</style>