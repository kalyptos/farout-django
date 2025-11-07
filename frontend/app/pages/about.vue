<template>
  <div>
    <!-- Page Header / Breadcrumb -->
    <PageHeader
      title="About Us"
      subtitle="Our Story"
      :breadcrumbs="breadcrumbs"
    />

    <!-- About Section -->
    <AboutSection
      :title="aboutData.title"
      :subtitle="aboutData.subtitle"
      :description="aboutData.description"
      :videoImage="aboutData.videoImage"
      :videoUrl="aboutData.videoUrl"
      :images="aboutImages"
    />

    <!-- Stats / Counter Section -->
    <CounterSection :items="aboutData.stats" />

    <!-- Mission & Vision Section -->
    <section class="mission-section section-padding">
      <div class="container">
        <div class="row g-4">
          <AnimatedElement animation="fade-in-up" :delay="'.3s'" class="col-lg-6">
            <div class="mission-content">
              <h2>Our Mission</h2>
              <p>{{ aboutData.mission }}</p>
            </div>
          </AnimatedElement>
          <AnimatedElement animation="fade-in-up" :delay="'.5s'" class="col-lg-6">
            <div class="vision-content">
              <h2>Our Vision</h2>
              <p>{{ aboutData.vision }}</p>
            </div>
          </AnimatedElement>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section class="values-section section-padding bg-cover">
      <div class="container">
        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <SectionTitle
            title="Our Values"
            subtitle="What Drives Us"
            centered
          />
        </AnimatedElement>

        <div class="row g-4 mt-5">
          <AnimatedElement
            v-for="(value, index) in aboutData.values"
            :key="index"
            animation="fade-in-up"
            :delay="`${0.3 + index * 0.2}s`"
            class="col-lg-3 col-md-6"
          >
            <div class="value-card">
              <h3>{{ value.title }}</h3>
              <p>{{ value.description }}</p>
            </div>
          </AnimatedElement>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <TeamSection
      title="Meet Our Leadership"
      subtitle="The Team"
      :teamMembers="teamMembers"
    />

    <!-- CTA Section -->
    <LetsTalkSection />
  </div>
</template>

<script setup lang="ts">
import { aboutContent } from '~/data/about'
import { members } from '~/data/members'

// Set page meta
useHead({
  title: 'About Us - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Learn about FarOut, a premier Star Citizen organization dedicated to excellence across all gameplay pillars.'
    }
  ]
})

// Breadcrumbs
const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'About Us' }
]

// About data
const aboutData = aboutContent

// About images for the section
const aboutImages = [
  '/assets/img/about/01.jpg',
  '/assets/img/about/02.jpg'
]

// Get top team members for display
const teamMembers = members.slice(0, 4).map(member => ({
  name: member.name,
  role: member.role,
  image: member.avatar,
  slug: `/members/${member.slug}`
}))
</script>

<style scoped lang="scss">
.mission-section,
.values-section {
  padding: 100px 0;
}

.mission-content,
.vision-content {
  h2 {
    color: var(--color-accent-1);
    margin-bottom: 1.5rem;
    font-size: 2rem;
  }

  p {
    color: var(--text-secondary);
    line-height: 1.8;
    font-size: 1.1rem;
  }
}

.value-card {
  background: var(--bg-card);
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  height: 100%;

  &:hover {
    border-color: var(--color-accent-1);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(17, 171, 233, 0.2);
  }

  h3 {
    color: var(--color-accent-1);
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
  }
}
</style>
