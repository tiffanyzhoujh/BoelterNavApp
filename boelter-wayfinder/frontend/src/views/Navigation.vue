<template>
    <!-- navigator -->
    <v-container class="nav">

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
</style>