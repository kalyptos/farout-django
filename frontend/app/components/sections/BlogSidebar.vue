<template>
  <div class="main-sidebar">
    <!-- Search Widget -->
    <div class="single-sidebar-widget">
      <div class="wid-title">
        <h3>Search</h3>
      </div>
      <div class="search-widget">
        <form @submit.prevent="handleSearch">
          <input type="text" v-model="searchQuery" placeholder="Search here">
          <button type="submit"><i class="fa-solid fa-magnifying-glass"></i></button>
        </form>
      </div>
    </div>

    <!-- Top Category Widget -->
    <div class="single-sidebar-widget">
      <div class="wid-title">
        <h3>Top Category</h3>
      </div>
      <div class="news-widget-categories">
        <ul>
          <li v-for="category in categories" :key="category.name" :class="{ active: category.active }">
            <NuxtLink :to="`/blog?category=${category.slug}`">{{ category.name }}</NuxtLink>
            <span>({{ String(category.count).padStart(2, '0') }})</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Recent Post Widget -->
    <div class="single-sidebar-widget">
      <div class="wid-title">
        <h3>Recent Post</h3>
      </div>
      <div class="recent-post-area">
        <div v-for="post in recentPosts" :key="post.slug" class="recent-items">
          <div class="recent-thumb">
            <img :src="post.image" :alt="post.title">
          </div>
          <div class="recent-content">
            <span>{{ post.date }}</span>
            <h6>
              <NuxtLink :to="`/blog/${post.slug}`">{{ post.title }}</NuxtLink>
            </h6>
          </div>
        </div>
      </div>
    </div>

    <!-- Popular Tag Widget -->
    <div class="single-sidebar-widget">
      <div class="wid-title">
        <h3>Popular Tag</h3>
      </div>
      <div class="news-widget-categories">
        <div class="tagcloud">
          <NuxtLink v-for="tag in tags" :key="tag" :to="`/blog?tag=${tag.toLowerCase()}`">{{ tag }}</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    navigateTo(`/blog?search=${encodeURIComponent(searchQuery.value)}`)
  }
}

// Placeholder data - can be replaced with API calls later
const categories = ref([
  { name: 'Organization News', slug: 'organization', count: 5, active: false },
  { name: 'Fleet Updates', slug: 'fleet', count: 3, active: false },
  { name: 'Events', slug: 'events', count: 7, active: true },
  { name: 'Member Spotlights', slug: 'members', count: 4, active: false },
  { name: 'Game Updates', slug: 'game', count: 2, active: false }
])

const recentPosts = ref([
  {
    slug: 'recent-post-1',
    title: 'Latest Organization Updates',
    date: 'Nov 1, 2025',
    image: '/assets/img/news/pp3.jpg'
  },
  {
    slug: 'recent-post-2',
    title: 'New Fleet Additions',
    date: 'Oct 28, 2025',
    image: '/assets/img/news/pp4.jpg'
  },
  {
    slug: 'recent-post-3',
    title: 'Upcoming Events',
    date: 'Oct 25, 2025',
    image: '/assets/img/news/pp5.jpg'
  }
])

const tags = ref([
  'Star Citizen',
  'Updates',
  'Events',
  'Fleet',
  'Community'
])
</script>

<style scoped>
/* Sidebar styles are handled by main template CSS */
</style>
