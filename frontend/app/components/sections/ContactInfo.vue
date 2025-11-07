<template>
  <section class="contact-info-section fix section-padding">
    <div class="container">
      <div class="row g-4">
        <div
          v-for="(box, index) in contactBoxes"
          :key="index"
          class="col-xl-4 col-lg-6 col-md-6"
          data-aos="fade-up"
          :data-aos-delay="(index + 1) * 200"
        >
          <div class="contact-box-items">
            <div class="icon">
              <i :class="`fa-solid ${box.icon}`"></i>
            </div>
            <div class="content">
              <h3>{{ box.title }}</h3>
              <p v-if="box.link">
                <a :href="box.link">{{ box.content }}</a>
              </p>
              <p v-else>{{ box.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { contactBoxes } from '~/data/contact'
</script>

<style lang="scss" scoped>
.contact-info-section {
  padding: 60px 0;
  background-color: var(--background-primary);
}

.contact-box-items {
  background-color: var(--background-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.3s ease;

  &:hover {
    border-color: var(--color-primary);
    transform: translateY(-5px);
  }

  .icon {
    font-size: 48px;
    color: var(--color-primary);
    margin-bottom: 20px;
    transition: color 0.3s ease;
  }

  &:hover .icon {
    color: var(--color-secondary);
  }

  .content {
    h3 {
      font-size: 20px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 10px;
    }

    p {
      font-size: 16px;
      color: var(--text-secondary);
      margin: 0;

      a {
        color: var(--text-secondary);
        text-decoration: none;
        transition: color 0.3s ease;

        &:hover {
          color: var(--color-primary);
        }
      }
    }
  }
}
</style>
