<template>
  <div class="multi-floor-container">
    <!-- Compass Icon -->
    <v-btn icon class="elevation-0 compass-button">
      <img src="@/assets/compass.svg" class="compass-icon"/>
    </v-btn>

    <!-- floor sidebar -->
    <!-- <div class="sidebar">
      <v-btn 
        icon
        v-for="(floor, index) in floors"
        :key="index"
        class="floor-button elevation-1"
        :color="activeFloor === floor ? '#48AEE2' : '#f1f5f8'"
        @click="activeFloor = floor"
      >
        {{ floor }}
      </v-btn>
    </div> -->

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
        {{ floor }}
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
</template>


<script setup>
import { ref, watch, computed } from 'vue'
import JSZip from 'jszip'
import axios from 'axios'
import roomMapping from '@/data/rooms.json'
import { useRouter } from 'vue-router';
const router = useRouter();
const imageSources = ref({})
const floors = ref([])
const activeFloor = ref(null)

const props = defineProps({
  start: String,
  destination: String,
})

// function goToCompass() { // access to orientation of the device required
//   router.push({
//     name: 'Compass',
//     query: {
//       start: props.start,
//       destination: props.destination,
//     },
//   })
// }

watch(() => [props.start, props.destination], fetchPath, { immediate: true })

async function fetchPath() {
  const startDot = roomMapping[props.start]
  var destDot

  // special destination handling: find the nearest restroom
  var startLevel = startDot[0]
  if (props.destination == "Restroom (W)") {
    var destLevel = startLevel
    if (startLevel == 1) {
      destLevel = 2
    }
    destDot = roomMapping["Restroom (Women, "+destLevel+"F)"]
  } else if (props.destination == "Restroom (M)") {
    var destLevel = startLevel
    if (startLevel == 1) {
      destLevel = 2
    }
    destDot = roomMapping["Restroom (Men, "+destLevel+"F)"]
  } else if (props.destination == "Restroom (All Gender)") {
    // gender inclusive restroom on floor 5, 6, 8
    var destLevel = startLevel
    if (startLevel <= 5 ) {
      destLevel = 5
    } else if (startLevel == 7 || startLevel == 9) {
      destLevel = 8
    }
    destDot = roomMapping["Restroom (Gender Inclusive, "+destLevel+"F)"]
  } else {
    // normal case
    destDot = roomMapping[props.destination]
  }

  if (!startDot || !destDot || startDot === destDot) return


  const res = await axios.post('https://boelterwayfinderbackend.onrender.com/api/path', {
    // const res = await axios.post('http://192.168.1.96:5000/api/path', {  
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
      const floor = filename.split('-')[0]
      newImageSources[floor] = url
      newFloors.push(floor)
    }
  }
  imageSources.value = newImageSources
  floors.value = newFloors
  activeFloor.value = newFloors[0]  // Set the first floor as active
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
  /* margin: 20px; */
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
</style>
