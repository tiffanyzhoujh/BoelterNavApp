<template>
  <!-- desktop view -->
  <v-container v-if="mdAndUp">
    <div class="multi-floor-container">
      <!-- floor sidebar (hidden if only one floor exists) -->
      <div class="sidebar">
        <v-btn icon class="elevation-0">
          <img src="@/assets/compass.svg" class="compass-icon"/>
        </v-btn>
        <v-btn 
          icon
          v-for="(floor, index) in floors"
          :key="index"
          class="elevation-1"
          :color="activeFloor === floor ? '#48AEE2' : '#f1f5f8'"
          @click="activeFloor = floor"
        >
          {{ floor.split('-')[0] }}
        </v-btn>
      </div>

      <div class="floorplans">
        <img
          v-if="activeFloor && imageSources[activeFloor]"
          :src="imageSources[activeFloor]"
          class="floorplan-image-web"
        />
      </div>
    </div>
  </v-container>

  <!-- mobile view -->
   <v-container v-else>
    <div class="multi-floor-container">
      <!-- Compass Icon -->
      <v-btn icon class="elevation-0 compass-button">
        <img src="@/assets/compass.svg" class="compass-icon"/>
      </v-btn>

      <!-- Floor Sidebar (Hidden if only one floor exists) -->
      <div v-if="floors.length > 1" class="sidebar">
        <v-btn 
          icon
          v-for="(floor, index) in floors"
          :key="index"
          class="floor-button elevation-1"
          :color="activeFloor === floor ? '#48AEE2' : '#f1f5f8'"
          @click="activeFloor = floor"
        >
          {{ floor.split('-')[0] }}
        </v-btn>
      </div>

      <div class="floorplans">
        <img
          v-if="activeFloor && imageSources[activeFloor]"
          :src="imageSources[activeFloor]"
          class="floorplan-image"
        />
      </div>
    </div>
  </v-container>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import JSZip from 'jszip'
import axios from 'axios'
import roomMapping from '@/data/rooms.json'
import { useRoute } from 'vue-router';
import { useDisplay } from 'vuetify'
const { mdAndUp } = useDisplay() // > 960px

const route = useRoute()
const imageSources = ref({})
const floors = ref([])
const activeFloor = ref(null)

// get query params
const start = ref('')
const destination = ref('')

onMounted(() => {
  start.value = route.query.start || ''
  destination.value = route.query.destination || ''

  if (start.value && destination.value) {
    fetchPath()
  }
})

watch(() => route.fullPath, () => {
  start.value = route.query.start || ''
  destination.value = route.query.destination || ''
  if (start.value && destination.value) {
    fetchPath()
  }
})

async function fetchPath() {
  const startDot = roomMapping[start.value]
  var destDot

  // special destination handling: find the nearest restroom
  var startLevel = startDot[0]
  if (destination.value == "Nearest Restroom (W)" || 
    destination.value == "Nearest Restroom (M)" || 
    destination.value == "Nearest Restroom (Gender Inclusive)") {
    destDot = destination.value
  } else {
    // normal case
    destDot = roomMapping[destination.value]
  }

  if (!startDot || !destDot || startDot === destDot) return

  // const res = await axios.post('https://boelterwayfinderbackend.onrender.com/api/path', {
  const res = await axios.post('http://172.20.10.2:5000/api/path', {  
    start: startDot,
    dest: destDot
  }, { responseType: 'blob' }) 
  // result is a zip of floorplan pictures
  const zip = await JSZip.loadAsync(res.data)
  const newImageSources = []
  const newFloors = []
  for (const filename of Object.keys(zip.files)) {
    const file = zip.files[filename]

    if (!file.dir && filename.endsWith('.png')) {
      const blob = await file.async('blob')
      const url = URL.createObjectURL(blob)
      const [floor, index] = filename.split('-')
      const key = `${floor}-${index}`
      newImageSources[key] = url
      newFloors.push(key)

    }
  }
  imageSources.value = newImageSources
  floors.value = newFloors
  activeFloor.value = newFloors[0]  // set the first floor as active
}
</script>

<style scoped>
.multi-floor-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.floor-block {
  border: 1px solid #ccc;
}

.svg-wrapper {
  display: inline-block;
}

.floor-image {
  width: 100%;
  display: block;
}

.floorplan-image {
  width: 100%;
}

.compass-button {
  position: absolute;
  right: 20px;
  width: 40px;
  z-index: 1000;
  opacity: 0.9;
}

.compass-icon {
  width: 30px;
}

.sidebar {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-right: 20px;
  min-width: 100px;
  /* opacity: 0.9; */
}

.floorplan-image-web {
  height: 600px;
}

</style>
