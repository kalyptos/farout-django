<template>
  <section class="about-section fix section-padding">
    <div class="container">
      <div v-if="variant === 'video'" class="about-wrapper-2">
        <div class="section-title-area">
          <SectionTitle :subtitle="subtitle" :title="title" />
          <div data-animation="fade-in-up">
            <p class="mb-4">{{ description }}</p>
            <BaseButton v-if="ctaText" :to="ctaLink" variant="theme-btn">
              {{ ctaText }}
            </BaseButton>
          </div>
        </div>
        <div class="row">
          <div data-animation="fade-in-up">
            <div class="about-video-image">
              <NuxtImg :src="videoImage" alt="about" />
              <a
                v-if="videoUrl"
                @click="showVideo = true"
                class="video-text ripple"
              >
                Play <i class="fa-solid fa-play"></i>
              </a>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="abour-right-items">
              <div
                v-for="(item, index) in contentBoxes"
                :key="index"
                data-animation="fade-in-up"
              >
                <h3>{{ item.title }}</h3>
                <p>{{ item.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
        <div class="section-title-area">
          <SectionTitle :subtitle="subtitle" :title="title" />
          <p data-animation="fade-in-up">{{ description }}</p>
        </div>
        <div class="about-wrapper">
          <div class="row justify-content-between align-items-center">
            <div class="col-lg-7">
              <div class="about-image-items">
                <div class="row g-4 align-items-center">
                  <div data-animation="fade-in-up">
                    <div v-if="supportContent" class="support-content">
                      <h3>{{ supportContent.title }}</h3>
                      <div class="text-area">
                        <p v-html="sanitizedSupportDescription"></p>
                        <NuxtLink :to="supportContent.link" class="icon">
                          <i class="fa-sharp fa-solid fa-arrow-right"></i>
                        </NuxtLink>
                      </div>
                    </div>
                    <div class="about-image">
                      <NuxtImg :src="images[0]" alt="about" />
                    </div>
                  </div>
                  <div data-animation="fade-in-up">
                    <div class="about-image-2">
                      <div class="about-image style-2">
                        <NuxtImg :src="images[1]" alt="about" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-5">
              <div class="about-content">
                <div
                  v-for="(item, index) in contentBoxes"
                  :key="index"
                  data-animation="fade-in-up"
                >
                  <div class="icon">
                    <i :class="item.icon"></i>
                    <div class="line-bar">
                      <NuxtImg src="/assets/img/about/line.png" alt="line" />
                    </div>
                  </div>
                  <div class="content">
                    <h3>{{ item.title }}</h3>
                    <p>{{ item.description }}</p>
                  </div>
                </div>
                                <AnimatedElement animation="fade-in-up" :delay="'.5s'">
                  <BaseButton
                    v-if="ctaText"
                    :to="ctaLink"
                    variant="theme-btn"
                  >
                    {{ ctaText }}
                  </BaseButton>
                </AnimatedElement>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <VueFinalModal v-model="showVideo" :esc-to-close="true">
      <div class="video-container">
        <iframe
          :src="videoUrl"
          style="border: none;"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </VueFinalModal>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { VueFinalModal } from 'vue-final-modal'
import DOMPurify from 'isomorphic-dompurify'

interface ContentBox {
  title: string
  description: string
  icon?: string
}

interface SupportContent {
  title: string
  description: string
  link: string
}

interface Props {
  title: string
  subtitle?: string
  description: string
  variant?: 'default' | 'video'
  videoImage?: string
  videoUrl?: string
  images?: string[]
  contentBoxes: ContentBox[]
  supportContent?: SupportContent
  ctaText?: string
  ctaLink?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  images: () => [],
  ctaLink: '/about'
})

const showVideo = ref(false)

// SECURITY: Sanitize support content description to prevent XSS attacks (SSR-safe with isomorphic-dompurify)
const sanitizedSupportDescription = computed(() => {
  if (!props.supportContent?.description) return ''
  return DOMPurify.sanitize(props.supportContent.description, {
    ALLOWED_TAGS: ['br', 'span', 'strong', 'em', 'b', 'i', 'p'],
    ALLOWED_ATTR: ['class'],
    ALLOW_DATA_ATTR: false
  })
})
</script>

<style scoped>
.video-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80vw;
  height: 80vh;
  background-color: black;
}

.video-container iframe {
  width: 100%;
  height: 100%;
}
</style>
