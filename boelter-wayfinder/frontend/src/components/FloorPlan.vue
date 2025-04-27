<template>
  <div class="multi-floor-container">
    <div
      v-for="floor in floorsInPath"
      :key="floor"
      class="floor-block"
    >
      <h3 class="floor-label">Floor {{ floor }}</h3> <!-- 👈 Label here -->

      <div class="svg-wrapper">
        <img
          :src="getSvgPath(floor)"
          class="floor-image"
          :alt="`Floorplan for ${floor}`"
        >
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, computed } from 'vue'
import axios from 'axios'
import roomMapping from '@/data/rooms.json'

const props = defineProps({
  start: String,
  destination: String,
})

const pathDots = ref([])

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
    destdot = roomMapping["Restroom (Women, "+destLevel+"F)"]
  } else if (props.destination == "Restroom (M)") {
    var destLevel = startLevel
    if (startLevel == 1) {
      destLevel = 2
    }
    destdot = roomMapping["Restroom (Men, "+destLevel+"F)"]
  } else if (props.destination == "Restroom (All Gender)") {
    // gender inclusive restroom on floor 5, 6, 8
    var destLevel = startLevel
    if (startLevel <= 5 ) {
      destLevel = 5
    } else if (startLevel == 7 || startLevel == 9) {
      destLevel = 8
    }
    destdot = roomMapping["Restroom (Gender Inclusive, "+destLevel+"F)"]
  } else {
    // normal case
    destDot = roomMapping[props.destination]
  }

  if (!startDot || !destDot || startDot === destDot) return

  const res = await axios.post('http://localhost:5000/api/path', {
    start: startDot,
    dest: destDot,
  })

  pathDots.value = res.data.path
  console.log('Path dots with coords:', pathDots.value)
}

const floorsInPath = computed(() =>
  [...new Set(pathDots.value.map(p => p.floor))]
)

const getSvgPath = floor =>
  new URL(`../assets/floorplans/floor-${floor}.svg`, import.meta.url).href
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
</style>
