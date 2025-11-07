<template>
  <section class="news-section fix section-padding">
    <div class="container">
      <div class="section-title-area">
        <SectionTitle :subtitle="subtitle" :title="title" />
      </div>
      <div class="row">
                <AnimatedElement
          v-for="(post, index) in posts"
          :key="post.id"
          class="col-xl-6"
          animation="fade-in-up"
          :delay="`${0.3 + index * 0.2}s`"
        >
          <BlogCard
            :title="post.title"
            :excerpt="post.excerpt"
            :image="post.image"
            :date="post.date"
            :link="`/blog/${post.slug}`"
          />
        </AnimatedElement>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { BlogPost } from '~/types'

interface Props {
  title: string
  subtitle?: string
  posts: BlogPost[]
}

defineProps<Props>()
</script>

<style scoped>
/* Blog section styles are handled by the main template CSS */
</style>
