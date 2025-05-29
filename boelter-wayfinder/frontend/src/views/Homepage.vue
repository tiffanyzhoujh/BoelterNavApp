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
         <div class="search-web">
          <v-select
            v-model="selectedCategory"
            :items="categoryOptions"
            item-title="label"
            item-value="value"
            label="Destination Type"
            class="filter-web"
          ></v-select>
          <v-autocomplete
            v-model="destination"
            :items="destinationOptions"
            item-title="label"
            item-value="value"
            prepend-inner-icon="mdi-magnify"
            placeholder="Where would you like to go?"
            outlined
            dense
            class="search-bar"
          />
         </div>
      
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
         <div class="mobile-input">
          <v-autocomplete
            v-model="destination"
            :items="destinationOptions"
            item-title="label"
            item-value="value"
            prepend-inner-icon="mdi-magnify"
            menu-icon=""
            placeholder="Where would you like to go?"
            outlined
            dense
            hide-details
          />
        </div>
        <!-- filter -->
        <div>
          <v-btn 
            class="elevation-0 pa-2 ml-3"
            prepend-icon="mdi-filter"
            dense
            @click="dialog = true"
          >
          {{ filterLabel }}
          </v-btn>
        </div>
        
        <!-- dialog for filter selection -->
        <v-dialog v-model="dialog" max-width="300">
          <v-card>
            <v-card-title class="text-h6">Filter Destinations</v-card-title>
            <v-card-text>
              <v-radio-group v-model="selectedCategory" column mandatory>
                <v-radio label="No Filter" value="none" />
                <v-radio label="Restrooms" value="restroom" />
                <v-radio label="Exits" value="exit" />
                <v-radio label="Elevators" value="elevator" />
              </v-radio-group>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn text @click="dialog = false">Close</v-btn>
            </v-card-actions> 
          </v-card>
        </v-dialog>

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
  import { ref, watch, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import rooms from '@/data/rooms.json'
  import '@mdi/font/css/materialdesignicons.css'
  import { useDisplay } from 'vuetify'
  const { mdAndUp } = useDisplay() // > 960px
  const logo = new URL('@/assets/logo.svg', import.meta.url).href
  const router = useRouter()

  // filter field
  const dialog = ref(false)
  const selectedCategory = ref('none')
  const filterLabel = computed(() => {
    switch (selectedCategory.value) {
        case 'restroom': return 'Restrooms'
        case 'exit': return 'Exits'
        case 'elevator': return 'Elevators'
        default: return 'No Filter'
      }
  })
  const categoryOptions = [
    {label:'Any', value: 'none'},
    {label:'Restrooms', value: 'restroom'},
    {label:'Exits', value: 'exit'},
    {label:'Elevators', value: 'elevator'}]


  // input field 
  const destination = ref(null)
  const destinationOptions = computed(() => {
    return Object.entries(rooms)
      .filter(([name, info]) => {
        // no filter applied, return all
        if (selectedCategory.value === 'none') return true
        // match the type
        return info.type === selectedCategory.value
      })
      .map(([name]) => ({
        label: name,
        value: name
      }))
  })

  // suggestion field
  const suggestions = [
    'Engineering Library', 
    'Nearest Restroom (Gender Inclusive)', 
    'Nearest Restroom (W)', 
    'Nearest Restroom (M)',
    '8500', 
    '8251',
    '5440',
    '3400',
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

.mobile-input{
  width:100%;
  display: flex;
  flex-direction: row;
  align-items:center;
}
.search-web{
  width: 100%;
  display: flex;
  flex-direction: row;
}
.filter-web{
  width: 30%;
}

</style>