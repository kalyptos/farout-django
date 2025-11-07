<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="Our Members"
      subtitle="Meet the Team"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Members Grid Section -->
    <section class="members-section section-padding">
      <div class="container">
        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <SectionTitle
            title="Member Roster"
            subtitle="Our Dedicated Team"
            centered
          />
        </AnimatedElement>

        <div class="row g-4 mt-5">
          <AnimatedElement
            v-for="(member, index) in members"
            :key="member.id"
            animation="fade-in-up"
            :delay="`${0.2 + index * 0.1}s`"
            class="col-lg-4 col-md-6"
          >
            <div class="member-card">
              <div class="member-image">
                <NuxtImg :src="member.avatar" :alt="member.name" />
                <div class="member-overlay">
                  <NuxtLink :to="`/members/${member.slug}`" class="view-profile">
                    View Profile
                    <i class="fa-solid fa-arrow-right"></i>
                  </NuxtLink>
                </div>
              </div>
              <div class="member-info">
                <h3>{{ member.name }}</h3>
                <p class="rank" v-if="member.rank">{{ member.rank }}</p>
                <p class="role">{{ member.role }}</p>
                <p class="description">{{ member.description }}</p>
                <div v-if="member.activities" class="activities">
                  <span
                    v-for="activity in member.activities"
                    :key="activity"
                    class="activity-badge"
                  >
                    {{ activity }}
                  </span>
                </div>
              </div>
            </div>
          </AnimatedElement>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <LetsTalkSection />
  </div>
</template>

<script setup lang="ts">
import { members } from '~/data/members'

useHead({
  title: 'Members - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Meet the talented members of FarOut, from fleet commanders to specialized division leaders.'
    }
  ]
})

const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Members' }
]
</script>

<style scoped lang="scss">
.members-section {
  padding: 100px 0;
}

.member-card {
  background: var(--bg-card);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-10px);
    border-color: var(--color-accent-1);
    box-shadow: 0 15px 40px rgba(17, 171, 233, 0.3);

    .member-overlay {
      opacity: 1;
    }
  }
}

.member-image {
  position: relative;
  overflow: hidden;
  aspect-ratio: 1/1;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.member-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(10, 14, 39, 0.95) 100%);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 2rem;
  opacity: 0;
  transition: opacity 0.3s ease;

  .view-profile {
    background: var(--color-accent-1);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;

    &:hover {
      background: var(--color-accent-2);
      transform: translateX(5px);
    }

    i {
      transition: transform 0.3s ease;
    }

    &:hover i {
      transform: translateX(3px);
    }
  }
}

.member-info {
  padding: 1.5rem;

  h3 {
    color: var(--text-primary);
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
  }

  .rank {
    color: var(--color-accent-2);
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.25rem;
  }

  .role {
    color: var(--color-accent-1);
    font-weight: 500;
    margin-bottom: 0.75rem;
  }

  .description {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .activities {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;

    .activity-badge {
      background: rgba(17, 171, 233, 0.2);
      color: var(--color-accent-1);
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.85rem;
      border: 1px solid rgba(17, 171, 233, 0.3);
    }
  }
}
</style>
