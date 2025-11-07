<template>
  <div v-if="member">
    <!-- Page Header -->
    <PageHeader
      :title="member.name"
      :subtitle="member.role"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Member Detail Section -->
    <section class="member-detail-section section-padding">
      <div class="container">
        <div class="row g-5">
          <!-- Member Image & Info -->
          <div class="col-lg-4">
            <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <div class="member-profile-card">
                <div class="profile-image">
                  <NuxtImg :src="member.avatar" :alt="member.name" />
                </div>
                <div class="profile-details">
                  <h2>{{ member.name }}</h2>
                  <p class="handle" v-if="member.handle">"{{ member.handle }}"</p>
                  <p class="rank" v-if="member.rank">{{ member.rank }}</p>
                  <p class="role">{{ member.role }}</p>

                  <div v-if="member.mainShip" class="detail-item">
                    <i class="fa-solid fa-rocket"></i>
                    <span>{{ member.mainShip }}</span>
                  </div>

                  <div v-if="member.joinDate" class="detail-item">
                    <i class="fa-solid fa-calendar"></i>
                    <span>Joined: {{ member.joinDate }}</span>
                  </div>

                  <div v-if="member.contactInfo?.discord" class="detail-item">
                    <i class="fab fa-discord"></i>
                    <span>{{ member.contactInfo.discord }}</span>
                  </div>
                </div>
              </div>
            </AnimatedElement>
          </div>

          <!-- Member Bio & Activities -->
          <div class="col-lg-8">
            <AnimatedElement animation="fade-in-up" :delay="'.5s'">
              <div class="member-bio">
                <h3>About</h3>
                <p>{{ member.description }}</p>
                <p v-if="member.bio">{{ member.bio }}</p>
              </div>
            </AnimatedElement>

            <AnimatedElement v-if="member.activities" animation="fade-in-up" :delay="'.7s'">
              <div class="member-activities mt-4">
                <h3>Specializations</h3>
                <div class="activities-grid">
                  <div
                    v-for="activity in member.activities"
                    :key="activity"
                    class="activity-card"
                  >
                    <i class="fa-solid fa-star"></i>
                    <span>{{ activity }}</span>
                  </div>
                </div>
              </div>
            </AnimatedElement>
          </div>
        </div>
      </div>
    </section>

    <!-- Other Members Section -->
    <section class="related-members section-padding bg-cover">
      <div class="container">
        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <SectionTitle
            title="Other Members"
            subtitle="Meet the Team"
            centered
          />
        </AnimatedElement>

        <div class="row g-4 mt-5">
          <AnimatedElement
            v-for="(otherMember, index) in otherMembers"
            :key="otherMember.id"
            animation="fade-in-up"
            :delay="`${0.3 + index * 0.2}s`"
            class="col-lg-3 col-md-6"
          >
            <TeamCard
              :name="otherMember.name"
              :role="otherMember.role"
              :image="otherMember.avatar"
              :slug="`/members/${otherMember.slug}`"
            />
          </AnimatedElement>
        </div>
      </div>
    </section>
  </div>

  <!-- 404 Not Found -->
  <div v-else class="error-section">
    <div class="container text-center">
      <h1>Member Not Found</h1>
      <p>The member you're looking for doesn't exist.</p>
      <NuxtLink to="/members" class="theme-btn">Back to Members</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { members, getMemberBySlug } from '~/data/members'

const route = useRoute()
const slug = route.params.slug as string

// Get member by slug
const member = getMemberBySlug(slug)

// Get other members (excluding current)
const otherMembers = members.filter(m => m.slug !== slug).slice(0, 4)

// Set page meta
useHead({
  title: member ? `${member.name} - Members` : 'Member Not Found',
  meta: [
    {
      name: 'description',
      content: member ? member.description : 'Member not found'
    }
  ]
})

// Breadcrumbs
const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Members', path: '/members' },
  { label: member?.name || 'Unknown' }
]
</script>

<style scoped lang="scss">
.member-detail-section {
  padding: 100px 0;
}

.member-profile-card {
  background: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  position: sticky;
  top: 100px;
}

.profile-image {
  width: 100%;
  aspect-ratio: 1/1;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.profile-details {
  padding: 2rem;

  h2 {
    color: var(--text-primary);
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }

  .handle {
    color: var(--color-accent-1);
    font-style: italic;
    margin-bottom: 0.5rem;
  }

  .rank {
    color: var(--color-accent-2);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
  }

  .role {
    color: var(--color-accent-1);
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  .detail-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 0;
    border-top: 1px solid var(--border-light);
    color: var(--text-secondary);

    i {
      color: var(--color-accent-1);
      width: 20px;
    }
  }
}

.member-bio,
.member-activities {
  background: var(--bg-card);
  border-radius: 8px;
  padding: 2rem;
  border: 1px solid var(--border-color);

  h3 {
    color: var(--color-accent-1);
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  p {
    color: var(--text-secondary);
    line-height: 1.8;
    font-size: 1.05rem;
    margin-bottom: 1rem;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.activity-card {
  background: rgba(17, 171, 233, 0.1);
  border: 1px solid rgba(17, 171, 233, 0.3);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(17, 171, 233, 0.2);
    transform: translateY(-3px);
  }

  i {
    color: var(--color-accent-1);
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    display: block;
  }

  span {
    color: var(--text-primary);
    font-weight: 500;
  }
}

.related-members {
  padding: 100px 0;
}

.error-section {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;

  h1 {
    color: var(--color-accent-1);
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  p {
    color: var(--text-secondary);
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }
}
</style>
