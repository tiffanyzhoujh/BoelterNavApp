<template>
  <div>
    <p>Rendering path from {{ start }} to {{ destination }}</p>
  </div>
  <div class="multi-floor-container">
    <div
      v-for="(floor, index) in floorsInPath"
      :key="floor"
      class="floor-block"
    >
      <div class="svg-wrapper">
        <img
          :src="getSvgPath(floor)"
          class="floor-image"
          @load="() => onImgLoad(index)"
          :ref="el => setImgRef(el, index)"
        >
        <canvas :ref="el => setCanvasRef(el, index)" class="floor-canvas" />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, computed, nextTick } from 'vue'
  import axios from 'axios'
  import roomMapping from '@/data/rooms.json'

  const props = defineProps({
    start: String,
    destination: String,
  })
  const pathDots = ref([])
  const canvasRefs = ref([])
  const imgRefs = ref([])

  watch(() => [props.start, props.destination], fetchPath, { immediate: true })

  async function fetchPath() {
    const startDot = roomMapping[props.start]
    const destDot = roomMapping[props.destination]
    if (!startDot || !destDot || startDot === destDot) return
    const res = await axios.post('http://localhost:5000/api/path', {
      start: startDot,
      dest: destDot,
    })
    pathDots.value = res.data.path
    console.log(pathDots.value)
  }

  const floorsInPath = computed(() =>
    [...new Set(pathDots.value.map(p => p.floor))]
  )

  // Canvas ref management
  function setCanvasRef(el, index) {
    if (el) canvasRefs.value[index] = el
  }
  function setImgRef(el, index) {
    if (el) imgRefs.value[index] = el
  }

  // Get SVG file path
  const getSvgPath = floor =>
    new URL(`../assets/floorplans/floor-${floor}.svg`, import.meta.url).href

  // SVG loaded → match canvas size + draw
  async function onImgLoad(index) {
    console.log("onImgLoad", index)
    await nextTick()

    const canvas = canvasRefs.value[index]
    const img = imgRefs.value[index]
    if (!canvas || !img) return

    canvas.width = img.naturalWidth
    canvas.height = img.naturalHeight
    canvas.style.width = img.width + 'px'
    canvas.style.height = img.height + 'px'

    console.log('canvas size:', canvas.width, canvas.height)
    console.log('image size:', img.naturalWidth, img.naturalHeight)

    const floor = floorsInPath.value[index]
    drawPathOnCanvas(floor, canvas)
  }




// Draw dots and path
function drawPathOnCanvas(floor, canvas) {
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const points = pathDots.value.filter(p => p.floor === floor)
  console.log(`🧭 Drawing on ${floor} → ${points.length} points`, points)
  if (points.length < 1) return
  // Are the coordinates inside the canvas?
  points.forEach(p => {
    if (p.x > canvas.width || p.y > canvas.height) {
      console.warn(`⚠️ Point ${p.name} is outside canvas: (${p.x}, ${p.y})`)
    }
  })

  // Get scale based on how image was resized
  const img = imgRefs.value[floorsInPath.value.indexOf(floor)]
  const scaleX = canvas.width / img.naturalWidth
  const scaleY = canvas.height / img.naturalHeight
  points.forEach(p => {
    if (p.x * scaleX > canvas.width || p.y * scaleY > canvas.height) {
      console.warn(`⚠️ Point ${p.name} is still outside canvas after scaling`)
    }
    else {
      console.warn('no longer outside canvas')
    }
  })

  // Draw path
  ctx.beginPath()
  // points.forEach(({ x, y }, i) => {
  //   i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
  // })
  points.forEach(({ x, y }, i) => {
    const scaledX = x * scaleX
    const scaledY = y * scaleY
    i === 0 ? ctx.moveTo(scaledX, scaledY) : ctx.lineTo(scaledX, scaledY)
  })
  ctx.strokeStyle = 'red'
  ctx.lineWidth = 3
  ctx.stroke()

  // Draw start + end
  const drawDot = (x, y, color) => {
    ctx.beginPath()
    // ctx.arc(x, y, 6, 0, 2 * Math.PI)
    ctx.arc(x * scaleX, y * scaleY, 6, 0, 2 * Math.PI)
    ctx.fillStyle = color
    ctx.fill()
  }
  drawDot(points[0].x, points[0].y, 'orange') // start
  drawDot(points.at(-1).x, points.at(-1).y, 'blue') // end
}

</script>


<style scoped>
.multi-floor-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.floor-block {
  position: relative;
  border: 1px solid #ccc;
}

.svg-wrapper {
  position: relative;
  display: inline-block;
}

.floor-canvas {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  width: auto;
  height: auto;
}

.floor-image {
  width: auto;
  height: auto;
  display: block;
}
</style>