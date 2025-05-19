<template>
  <!-- desktop view -->
    <v-container v-if="mdAndUp" class="fill-height d-flex flex-column justify-center align-center text-center web-container">
        <!-- title -->
        <div class="title-web">
            <img src="@/assets/logo.svg" class="logo-web"/>
            <div>
                <h1 class="mt-8 ml-4 font-weight-bold title-text-web">Boelter Wayfinder</h1>
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

  <!-- mobile view -->
    <v-container v-else class="fill-height d-flex flex-column justify-center align-center text-center">
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
</template>
  
<script setup>
  import { ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import rooms from '@/data/rooms.json'
  import '@mdi/font/css/materialdesignicons.css'
  import { useDisplay } from 'vuetify'
  const { mdAndUp } = useDisplay() // > 960px
  
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
    'Restroom (Gender Inclusive)', 
    '5440',
    'SEAS Cafe'
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

.web-container {
  margin-top: 200px;
  width: 1000px;
}
.title-web {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 50px;
}
.logo-web {
  width: 80px;
}
.title-text-web {
  font-size: 50px;
}

</style>