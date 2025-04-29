<template>
  <div class="multi-floor-container">
    <div class="floorplans">
      <div v-for="(imgSrc, index) in imageSources" :key="index" class="floorplan-block">
        <img :src="imgSrc" class="floorplan-image" />
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, computed } from 'vue'
import JSZip from 'jszip'
import axios from 'axios'
import roomMapping from '@/data/rooms.json'


const imageSources = ref([])

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

  console.log(startDot)
  console.log(destDot)

  if (!startDot || !destDot || startDot === destDot) return


  const res = await axios.post('http://192.168.1.96:5000/api/path', {
    start: startDot,
    dest: destDot
  }, { responseType: 'blob' }) 
  // result is a zip of floorplan pictures
  const zip = await JSZip.loadAsync(res.data)
  const newImageSources = []
  for (const filename of Object.keys(zip.files)) {
    const file = zip.files[filename]

    if (!file.dir && filename.endsWith('.png')) {
      const blob = await file.async('blob')
      const url = URL.createObjectURL(blob)
      newImageSources.push(url)
    }
  }
  imageSources.value = newImageSources
  console.log("Extracted images:", imageSources.value)
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

img {
  width: 100%;
}
</style>
