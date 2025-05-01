<template>
    <v-btn icon @click="goBack">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <v-btn @click="enableCompass">Enable Compass</v-btn>

    <div class="compass-container">
      <img
        id="compass"
        src="@/assets/compass-needle.svg"
        class="compass-needle"
        :style="{ transform: `rotate(${-heading}deg)` }"
        alt="Compass Needle"
      />
      <div class="heading-display">{{ headingDisplay }}</div>
    </div>

    <!-- debug -->
    <div class="debug-box">
      alpha: {{ rawAlpha }}<br />
      compass heading: {{ headingDisplay }}<br />
      permission: {{ permissionStatus }}
    </div>

</template>
  
<script setup>
import { onMounted, ref, computed} from 'vue'
import { useRouter, useRoute } from 'vue-router'

// nav-back button
const router = useRouter()
const route = useRoute()
function goBack() {
  router.push({
    name: 'Navigation',
    query: {
      start: route.query.start,
      destination: route.query.destination,
    },
  })
}

// compass

// Reactive state
const heading = ref(0)
const rawAlpha = ref(null)
const permissionStatus = ref('pending')

const headingDisplay = computed(() => `${heading.value.toFixed(0)}°`)

function handleOrientation(event) {
  rawAlpha.value = event.alpha

  let angle = event.alpha
  if (typeof event.webkitCompassHeading !== 'undefined') {
    angle = event.webkitCompassHeading
  }

  if (angle != null) {
    heading.value = angle
  }
}

function enableCompass() {
  if (typeof DeviceOrientationEvent?.requestPermission === 'function') {
    permissionStatus.value = 'requesting'
    DeviceOrientationEvent.requestPermission()
      .then((state) => {
        permissionStatus.value = state
        if (state === 'granted') {
          window.addEventListener('deviceorientation', handleOrientation, true)
        }
      })
      .catch(() => {
        permissionStatus.value = 'denied'
      })
  } else {
    permissionStatus.value = 'granted'
    window.addEventListener('deviceorientation', handleOrientation, true)
  }
}

onMounted(() => {
  // Only auto-start on Android; iOS needs button
  if (typeof DeviceOrientationEvent?.requestPermission !== 'function') {
    enableCompass()
  }
})
</script>

<style scoped>
  .fullscreen {
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .compass-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  #compass {
    width: 200px;
    height: 200px;
    transition: transform 0.2s ease-out;
    transform-origin: center center;
  }
  </style>
  