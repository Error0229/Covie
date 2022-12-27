<script setup>
// import yahoo from './components/yahoo.vue'
// import imdb from './components/imdb.vue'
// import rottentomatoes from './components/rotten_tomatoes.vue'
import { RouterView } from 'vue-router';
</script>

<template>
  <main>
    
    <router-link :to="'/yahooresult'" class="header">yahoo</router-link>
    <router-link :to="'/imdbresult'" class="header">imdb</router-link>
    <router-link :to="'/rottentomatoesresult'" class="header">rotten_tomatoes</router-link>
    <!-- <div>Yahoo result
      <yahoo />
    </div>
    <div>Imdb result
      <imdb />
    </div>
    <div>Rotten tomatoes result
      <rottentomatoes />
    </div> -->
    <RouterView></RouterView> 
  </main>
</template>

<style scoped>
/* header {
  line-height: 1.5;
} */
.header{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  position: sticky;
  /* margin: 0 auto;
  padding: 0 1rem;
  max-width: 1024px;
  width: 100%;
  height: 100%; */
}
/* .logo {
  display: block;
  margin: 0 auto 2rem;
} */

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
