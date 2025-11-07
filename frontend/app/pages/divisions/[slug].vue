<template>
  <div v-if="division">
    <!-- Page Header -->
    <PageHeader
      :title="division.name"
      :subtitle="division.category"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Division Detail Section -->
    <section class="division-detail-section section-padding">
      <div class="container">
        <div class="row g-5">
          <!-- Division Image -->
          <div class="col-lg-6">
            <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <div class="division-image">
                <NuxtImg :src="division.image" :alt="division.name" />
              </div>
            </AnimatedElement>
          </div>

          <!-- Division Info -->
          <div class="col-lg-6">
            <AnimatedElement animation="fade-in-up" :delay="'.5s'">
              <div class="division-info">
                <h2>{{ division.name }}</h2>
                <p class="category">{{ division.category }}</p>
                <p class="description">{{ division.description }}</p>
                <p v-if="division.longDescription" class="long-description">{{ division.longDescription }}</p>

                <div class="division-stats">
                  <div v-if="division.commander" class="stat-item">
                    <i class="fa-solid fa-user-crown"></i>
                    <div>
                      <span class="label">Commander</span>
                      <span class="value">{{ division.commander }}</span>
                    </div>
                  </div>

                  <div v-if="division.memberCount" class="stat-item">
                    <i class="fa-solid fa-users"></i>
                    <div>
                      <span class="label">Members</span>
                      <span class="value">{{ division.memberCount }}</span>
                    </div>
                  </div>

                  <div v-if="division.established" class="stat-item">
                    <i class="fa-solid fa-calendar-star"></i>
                    <div>
                      <span class="label">Established</span>
                      <span class="value">{{ division.established }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </AnimatedElement>
          </div>
        </div>

        <!-- Primary Ships -->
        <div v-if="division.primaryShips" class="row mt-5">
          <div class="col-12">
            <AnimatedElement animation="fade-in-up" :delay="'.7s'">
              <div class="ships-section">
                <h3>Primary Ships</h3>
                <div class="ships-grid">
                  <div
                    v-for="ship in division.primaryShips"
                    :key="ship"
                    class="ship-card"
                  >
                    <i class="fa-solid fa-rocket"></i>
                    <span>{{ ship }}</span>
                  </div>
                </div>
              </div>
            </AnimatedElement>
          </div>
        </div>

        <!-- Activities -->
        <div v-if="division.activities" class="row mt-4">
          <div class="col-12">
            <AnimatedElement animation="fade-in-up" :delay="'.9s'">
              <div class="activities-section">
                <h3>Primary Activities</h3>
                <div class="activities-list">
                  <span
                    v-for="activity in division.activities"
                    :key="activity"
                    class="activity-badge"
                  >
                    {{ activity }}
                  </span>
                </div>
              </div>
            </AnimatedElement>
          </div>
        </div>
      </div>
    </section>

    <!-- Other Divisions Section -->
    <section class="related-divisions section-padding bg-cover">
      <div class="container">
        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <SectionTitle
            title="Other Divisions"
            subtitle="Explore More"
            centered
          />
        </AnimatedElement>

        <div class="row g-4 mt-5">
          <AnimatedElement
            v-for="(otherDivision, index) in otherDivisions"
            :key="otherDivision.id"
            animation="fade-in-up"
            :delay="`${0.3 + index * 0.2}s`"
            class="col-lg-4 col-md-6"
          >
            <PortfolioCard
              :title="otherDivision.name"
              :category="otherDivision.category"
              :description="otherDivision.description"
              :image="otherDivision.image"
              :hoverImage="otherDivision.hoverImage"
              :slug="`/divisions/${otherDivision.slug}`"
            />
          </AnimatedElement>
        </div>
      </div>
    </section>
  </div>

  <!-- 404 Not Found -->
  <div v-else class="error-section">
    <div class="container text-center">
      <h1>Division Not Found</h1>
      <p>The division you're looking for doesn't exist.</p>
      <NuxtLink to="/divisions" class="theme-btn">Back to Divisions</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { divisions, getDivisionBySlug } from '~/data/divisions'

const route = useRoute()
const slug = route.params.slug as string

// Get division by slug
const division = getDivisionBySlug(slug)

// Get other divisions (excluding current)
const otherDivisions = divisions.filter(d => d.slug !== slug).slice(0, 3)

// Set page meta
useHead({
  title: division ? `${division.name} - Divisions` : 'Division Not Found',
  meta: [
    {
      name: 'description',
      content: division ? division.description : 'Division not found'
    }
  ]
})

// Breadcrumbs
const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Divisions', path: '/divisions' },
  { label: division?.name || 'Unknown' }
]
</script>

<style scoped lang="scss">
.division-detail-section {
  padding: 100px 0;
}

.division-image {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);

  img {
    width: 100%;
    height: auto;
    display: block;
  }
}

.division-info {
  h2 {
    color: var(--text-primary);
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .category {
    color: var(--color-accent-1);
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
  }

  .description {
    color: var(--text-secondary);
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.5rem;
  }

  .long-description {
    color: var(--text-secondary);
    line-height: 1.8;
    margin-bottom: 2rem;
  }
}

.division-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: var(--bg-card);
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);

  .stat-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;

    i {
      color: var(--color-accent-1);
      font-size: 1.5rem;
      width: 30px;
    }

    div {
      display: flex;
      flex-direction: column;

      .label {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
      }

      .value {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 500;
      }
    }
  }
}

.ships-section,
.activities-section {
  background: var(--bg-card);
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);

  h3 {
    color: var(--color-accent-1);
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
}

.ships-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

.ship-card {
  background: rgba(17, 171, 233, 0.1);
  border: 1px solid rgba(17, 171, 233, 0.3);
  border-radius: 8px;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(17, 171, 233, 0.2);
    transform: translateY(-3px);
  }

  i {
    color: var(--color-accent-1);
    font-size: 2rem;
    margin-bottom: 0.75rem;
    display: block;
  }

  span {
    color: var(--text-primary);
    font-weight: 500;
    display: block;
  }
}

.activities-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;

  .activity-badge {
    background: rgba(242, 201, 76, 0.2);
    color: var(--color-accent-2);
    padding: 0.75rem 1.5rem;
    border-radius: 20px;
    font-weight: 500;
    border: 1px solid rgba(242, 201, 76, 0.4);
    transition: all 0.3s ease;

    &:hover {
      background: rgba(242, 201, 76, 0.3);
      transform: scale(1.05);
    }
  }
}

.related-divisions {
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
