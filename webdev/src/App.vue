<script setup>
import yahoo from './components/yahoo.vue'
import imdb from './components/imdb.vue'
import rottentomatoes from './components/rotten_tomatoes.vue'
</script>

<template>

  <main>
    <div>Yahoo result
      <yahoo />
    </div>
    <div>Imdb result
      <imdb />
    </div>
    <div>Rotten tomatoes result
      <rottentomatoes />
    </div>
  </main>
</template>

<!-- <style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

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
</style> -->
